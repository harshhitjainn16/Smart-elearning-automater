"""
Streamlit Dashboard for Smart E-Learning Automator
Real-time monitoring and control
"""
import streamlit as st
import pandas as pd
from database import Database
from datetime import datetime
import time
import threading
from main import run_automation


# Page config
st.set_page_config(
    page_title="Smart E-Learning Automator",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS to hide warnings and improve UI
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Suppress browser console warnings */
    .stAlert {display: none;}
    
    /* Improve button styling */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #00d4ff;
        color: black;
        font-weight: bold;
    }
    
    /* Improve metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Suppress warnings in browser console
st.markdown("""
<script>
    // Suppress Popper.js warnings
    const originalWarn = console.warn;
    console.warn = function(...args) {
        if (args[0] && typeof args[0] === 'string' && 
            (args[0].includes('preventOverflow') || 
             args[0].includes('Popper') ||
             args[0].includes('modifier'))) {
            return;
        }
        originalWarn.apply(console, args);
    };
</script>
""", unsafe_allow_html=True)

# Initialize database
db = Database()

# Title
st.title("🎓 Smart E-Learning Automator Dashboard")
st.markdown("---")

# Sidebar - Controls
st.sidebar.header("⚙️ Automation Controls")

platform = st.sidebar.selectbox(
    "Platform",
    ["youtube", "coursera", "udemy", "moodle"]
)

playlist_url = st.sidebar.text_input("Playlist/Course URL")

with st.sidebar.expander("🔐 Login Credentials (Optional)"):
    username = st.text_input("Username/Email")
    password = st.text_input("Password", type="password")

auto_quiz = st.sidebar.checkbox("Auto-solve Quizzes", value=True)
video_limit = st.sidebar.number_input("Video Limit (0 = unlimited)", min_value=0, value=0)

playback_speed = st.sidebar.selectbox(
    "⚡ Playback Speed",
    options=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0],
    index=2,  # Default to 1.0x
    format_func=lambda x: f"{x}x {'(Normal)' if x == 1.0 else '(Faster)' if x > 1.0 else '(Slower)'}"
)

start_button = st.sidebar.button("▶️ Start Automation", type="primary")

if start_button and playlist_url:
    credentials = None
    if username and password:
        credentials = {'username': username, 'password': password}
    
    limit = None if video_limit == 0 else video_limit
    
    # Run automation in background thread
    def run_in_thread():
        try:
            run_automation(platform, playlist_url, credentials, auto_quiz, limit, playback_speed)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    thread = threading.Thread(target=run_in_thread, daemon=True)
    thread.start()
    st.sidebar.success("✅ Automation started!")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

# Main dashboard
col1, col2, col3, col4 = st.columns(4)

# Get stats
completed_videos = len(db.get_completed_videos(platform))
quiz_stats = db.get_quiz_stats(platform)
playlist_progress_list = db.get_playlist_progress()
total_playlists = len(playlist_progress_list) if playlist_progress_list else 0

with col1:
    st.metric("📹 Videos Completed", completed_videos)

with col2:
    st.metric("📝 Quizzes Attempted", quiz_stats['total_attempts'])

with col3:
    st.metric("✅ Quiz Accuracy", f"{quiz_stats['accuracy']}%")

with col4:
    st.metric("📚 Playlists Tracked", total_playlists)

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Activity Logs", "📹 Completed Videos", "📝 Quiz History", "📚 Playlist Progress"])

with tab1:
    st.subheader("Recent Activity")
    logs = db.get_recent_logs(limit=20)
    
    if logs:
        df_logs = pd.DataFrame(logs)
        
        # Color code by status
        def color_status(val):
            colors = {
                'success': 'background-color: #d4edda',
                'error': 'background-color: #f8d7da',
                'warning': 'background-color: #fff3cd',
                'info': 'background-color: #d1ecf1'
            }
            return colors.get(val, '')
        
        st.dataframe(
            df_logs[['timestamp', 'action_type', 'message', 'status']].style.map(
                color_status, subset=['status']
            ),
            width='stretch',
            height=400
        )
    else:
        st.info("No activity logs yet. Start automation to see logs.")

with tab2:
    st.subheader("Completed Videos")
    videos = db.get_completed_videos(platform)
    
    if videos:
        df_videos = pd.DataFrame(videos)
        st.dataframe(
            df_videos[['platform', 'title', 'watched_at', 'video_url']],
            width='stretch',
            height=400
        )
    else:
        st.info("No completed videos yet.")

with tab3:
    st.subheader("Quiz Attempts")
    
    # Get quiz data
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT question_text, user_answer, is_correct, confidence_score, attempted_at
        FROM quizzes
        ORDER BY attempted_at DESC
        LIMIT 50
    ''')
    
    quiz_data = cursor.fetchall()
    conn.close()
    
    if quiz_data:
        df_quiz = pd.DataFrame(
            quiz_data,
            columns=['Question', 'Answer', 'Correct', 'Confidence', 'Time']
        )
        
        # Format
        df_quiz['Correct'] = df_quiz['Correct'].apply(lambda x: '✅' if x else '❌')
        df_quiz['Confidence'] = df_quiz['Confidence'].apply(lambda x: f"{x*100:.1f}%" if x else "N/A")
        
        st.dataframe(df_quiz, width='stretch', height=400)
        
        # Show performance stats instead of chart
        st.subheader("Quiz Performance Overview")
        conn = db.get_connection()
        trend_df = pd.read_sql_query('''
            SELECT 
                DATE(attempted_at) as date,
                COUNT(*) as total,
                SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct
            FROM quizzes
            GROUP BY DATE(attempted_at)
            ORDER BY date
        ''', conn)
        conn.close()
        
        if not trend_df.empty:
            trend_df['accuracy'] = (trend_df['correct'] / trend_df['total'] * 100).round(2)
            # Display as table instead of chart to avoid compatibility issues
            st.dataframe(trend_df[['date', 'total', 'correct', 'accuracy']], use_container_width=True)
    else:
        st.info("No quiz attempts yet.")

with tab4:
    st.subheader("Playlist Progress Tracking")
    
    playlists = db.get_playlist_progress()
    
    if playlists:
        st.success(f"📚 Tracking {len(playlists)} playlist(s)")
        
        for playlist in playlists:
            with st.expander(f"📺 {playlist['playlist_url'][:80]}... - {playlist['total_videos_watched']} videos watched", expanded=True):
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric("Videos Watched", playlist['total_videos_watched'])
                
                with col_b:
                    status = "✅ Complete" if playlist['is_complete'] else "⏳ In Progress"
                    st.info(status)
                
                with col_c:
                    last_watched = playlist['last_watched_at']
                    if last_watched:
                        st.caption(f"Last watched: {last_watched}")
                
                if playlist['last_video_url']:
                    st.caption(f"🔗 Last video: {playlist['last_video_url']}")
        
        # Show progress table instead of chart (to avoid altair compatibility issues)
        st.subheader("Progress Overview")
        df_playlists = pd.DataFrame(playlists)
        
        # Create a simple table view
        progress_table = df_playlists[['playlist_url', 'total_videos_watched', 'is_complete']].copy()
        progress_table.columns = ['Playlist URL', 'Videos Watched', 'Complete']
        progress_table['Complete'] = progress_table['Complete'].apply(lambda x: '✅' if x else '⏳')
        st.dataframe(progress_table, use_container_width=True)
    else:
        st.info("No playlist progress tracked yet. Start automating a playlist to see progress here!")
        st.markdown("""
        ### 💡 How it works:
        1. Paste a YouTube playlist URL in the sidebar
        2. Click "Start Automation"
        3. Progress will be automatically tracked here
        4. You can see how many videos you've watched from each playlist
        """)


# Footer
st.markdown("---")
st.caption("💡 Click 'Refresh Data' in the sidebar to update manually")
