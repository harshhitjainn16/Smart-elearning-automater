"""
Enhanced Streamlit Dashboard with Authentication
Professional UI for Smart E-Learning Automator
"""
import streamlit as st
import pandas as pd
from database import Database
from auth import AuthManager
from datetime import datetime
import time
import threading
from main import run_automation
from report_generator import generate_user_report
from analytics import Analytics
import os
import plotly.express as px
import plotly.graph_objects as go


# Must be first Streamlit command
st.set_page_config(
    page_title="Smart E-Learning Automator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize auth manager
auth = AuthManager()

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Get theme from session state
current_theme = st.session_state.get('theme', 'dark')

# Custom CSS for beautiful UI with dynamic theme support
if current_theme == 'light':
    st.markdown("""
    <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Light theme adjustments */
        [data-testid="stAppViewContainer"] {
            background-color: #f5f5f5;
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Force dark text on light background */
        .main .block-container {
            color: #262730;
        }
        
        /* All text elements in light theme */
        p, span, div, h1, h2, h3, h4, h5, h6, label, li {
            color: #262730 !important;
        }
        
        /* But buttons should have white text */
        button p, button span, button div, button label {
            color: white !important;
        }
        
        /* Streamlit specific text elements */
        [data-testid="stMarkdownContainer"] p {
            color: #262730 !important;
        }
        
        /* Exception for buttons inside markdown */
        button [data-testid="stMarkdownContainer"] p {
            color: white !important;
        }
        
        [data-testid="stText"] {
            color: #262730 !important;
        }
        
        .stMarkdown {
            color: #262730 !important;
        }
        
        /* Input labels */
        [data-testid="stWidgetLabel"] {
            color: #262730 !important;
        }
        
        /* Metric labels and values */
        [data-testid="stMetricLabel"] {
            color: #262730 !important;
        }
        
        [data-testid="stMetricValue"] {
            color: #262730 !important;
        }
        
        [data-testid="stMetricDelta"] {
            color: #262730 !important;
        }
        
        /* Caption text */
        .stCaptionContainer, [data-testid="stCaptionContainer"] {
            color: #555 !important;
        }
        
        /* Login Page Styling */
        .login-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 50px 20px;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .login-title {
            font-size: 3rem;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .login-subtitle {
            font-size: 1.2rem;
            color: #555 !important;
        }
        
        /* Dashboard Styling */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            color: white;
        }
        
        .main-header * {
            color: white !important;
        }
        
        .welcome-text {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 10px;
            color: white !important;
        }
        
        .subtitle-text {
            font-size: 1.1rem;
            opacity: 0.9;
            color: white !important;
        }
        
        /* Metric Cards */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 10px 0;
        }
        
        .metric-card * {
            color: white !important;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            color: white !important;
        }
        
        .metric-label {
            font-size: 1rem;
            opacity: 0.9;
            margin-top: 5px;
            color: white !important;
        }
        
        /* Button Styling */
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            height: 3em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            font-weight: bold;
            border: none;
            transition: all 0.3s;
        }
        
        .stButton>button p {
            color: white !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        /* Form submit button - specifically target Save Settings */
        button[kind="formSubmit"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }
        
        button[kind="formSubmit"] p {
            color: white !important;
        }
        
        button[kind="formSubmit"] span {
            color: white !important;
        }
        
        button[kind="formSubmit"] div {
            color: white !important;
        }
        
        /* Target form buttons more specifically */
        form button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }
        
        form button * {
            color: white !important;
        }
        
        /* All button text and children */
        button {
            color: white !important;
        }
        
        button p, button span, button div {
            color: white !important;
        }
        
        /* Button icons */
        button svg {
            fill: white !important;
            color: white !important;
        }
        
        /* Streamlit specific button data attributes */
        [data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }
        
        [data-testid="stFormSubmitButton"] button * {
            color: white !important;
        }
        
        /* Info boxes */
        .info-box {
            padding: 20px;
            border-radius: 10px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            margin: 10px 0;
        }
        
        .info-box * {
            color: white !important;
        }
        
        .success-box {
            padding: 20px;
            border-radius: 10px;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            margin: 10px 0;
        }
        
        .success-box * {
            color: white !important;
        }
        
        /* Profile Picture */
        .profile-pic {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            color: white !important;
            font-weight: bold;
            margin: 0 auto 20px;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 10px 20px;
            background-color: rgba(102, 126, 234, 0.15);
            color: #262730 !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
        }
        
        /* Dataframe and table text */
        [data-testid="stDataFrame"] {
            color: #262730 !important;
        }
        
        /* Expander text */
        [data-testid="stExpander"] summary {
            color: #262730 !important;
        }
        
        /* Form labels */
        .stTextInput label, .stSelectbox label, .stNumberInput label, 
        .stCheckbox label, .stSlider label {
            color: #262730 !important;
        }
        
        /* Selectbox dropdown text */
        [data-baseweb="select"] {
            background-color: white !important;
        }
        
        [data-baseweb="select"] > div {
            background-color: white !important;
            color: #262730 !important;
        }
        
        /* Dropdown arrow icon */
        [data-baseweb="select"] svg {
            color: #262730 !important;
            fill: #262730 !important;
        }
        
        /* Dropdown menu items */
        [role="listbox"] {
            background-color: white !important;
        }
        
        [role="option"] {
            color: #262730 !important;
            background-color: white !important;
        }
        
        [role="option"]:hover {
            background-color: #f0f0f0 !important;
        }
        
        /* Input fields */
        input, textarea, select {
            background-color: white !important;
            color: #262730 !important;
        }
        
        /* Checkbox text */
        .stCheckbox > label > div {
            color: #262730 !important;
        }
        
        /* Form submit button text visibility */
        [data-testid="baseButton-secondary"] {
            background-color: #667eea !important;
            color: white !important;
        }
        
        /* Info, success, warning, error boxes */
        .stAlert {
            color: #262730 !important;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Login Page Styling */
        .login-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 50px 20px;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .login-title {
            font-size: 3rem;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .login-subtitle {
            font-size: 1.2rem;
            color: #888;
        }
        
        /* Dashboard Styling */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            color: white;
        }
        
        .welcome-text {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .subtitle-text {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        /* Metric Cards */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 10px 0;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
        }
        
        .metric-label {
            font-size: 1rem;
            opacity: 0.9;
            margin-top: 5px;
        }
        
        /* Button Styling */
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            height: 3em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: bold;
            border: none;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Info boxes */
        .info-box {
            padding: 20px;
            border-radius: 10px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            margin: 10px 0;
        }
        
        .success-box {
            padding: 20px;
            border-radius: 10px;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            margin: 10px 0;
        }
        
        /* Profile Picture */
        .profile-pic {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            color: white;
            font-weight: bold;
            margin: 0 auto 20px;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 10px 20px;
            background-color: rgba(102, 126, 234, 0.1);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)


def login_page():
    """Login and Registration Page"""
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown('''
    <div class="login-header">
        <div class="login-title">🎓 Smart E-Learning Automator</div>
        <div class="login-subtitle">Automate your learning journey with AI-powered tools</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Login/Register tabs
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.markdown("### Welcome Back!")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submit:
                if username and password:
                    user = auth.login_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        # Load user's theme preference
                        user_settings = auth.get_user_settings(user['id'])
                        st.session_state.theme = user_settings.get('theme', 'dark')
                        st.success(f"✅ Welcome back, {user['full_name'] or user['username']}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please enter both username and password")
    
    with tab2:
        st.markdown("### Create Your Account")
        with st.form("register_form"):
            full_name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email", placeholder="john@example.com")
            username = st.text_input("Username", placeholder="Choose a username")
            password = st.text_input("Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
            
            submit = st.form_submit_button("✨ Create Account", use_container_width=True)
            
            if submit:
                if not all([full_name, email, username, password, confirm_password]):
                    st.warning("⚠️ Please fill in all fields")
                elif password != confirm_password:
                    st.error("❌ Passwords do not match")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    if auth.register_user(username, email, password, full_name):
                        st.success("✅ Account created successfully! Please login.")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("❌ Username or email already exists")
    
    # Features section
    st.markdown("---")
    st.markdown("### ✨ Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🤖 Auto-Playback**")
        st.caption("Automated video watching")
    with col2:
        st.markdown("**⚡ Speed Control**")
        st.caption("0.5x to 2.0x speeds")
    with col3:
        st.markdown("**📊 Progress Tracking**")
        st.caption("Track your learning")
    
    st.markdown('</div>', unsafe_allow_html=True)


def dashboard_page():
    """Main Dashboard Page"""
    user = st.session_state.user
    db = Database(user_id=user['id'])  # User-specific database
    
    # Load user's theme preference
    settings = auth.get_user_settings(user['id'])
    if 'theme' not in st.session_state or st.session_state.theme != settings['theme']:
        st.session_state.theme = settings['theme']
    
    # Header
    st.markdown(f'''
    <div class="main-header">
        <div class="welcome-text">Welcome back, {user['full_name'] or user['username']}! 👋</div>
        <div class="subtitle-text">Let's continue your learning journey</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar - User Profile & Controls
    with st.sidebar:
        # Profile section
        initials = user['full_name'][0].upper() if user['full_name'] else user['username'][0].upper()
        st.markdown(f'<div class="profile-pic">{initials}</div>', unsafe_allow_html=True)
        st.markdown(f"### {user['full_name'] or user['username']}")
        st.caption(f"@{user['username']}")
        
        st.markdown("---")
        
        # Get user settings
        settings = auth.get_user_settings(user['id'])
        
        st.markdown("### ⚙️ Automation Settings")
        
        # Important notice about browser location
        st.info("""
        ℹ️ **Important:** The browser automation runs on the **server** (where this dashboard is hosted).  
        If you're accessing from another device, the Chrome browser will open on the server computer, not on your device.  
        You'll see progress updates here in real-time.
        """)
        
        platform = st.selectbox(
            "Platform",
            ["youtube", "coursera", "udemy", "moodle"],
            help="Select your learning platform"
        )
        
        playlist_url = st.text_input(
            "📺 Playlist/Course URL",
            placeholder="Paste your playlist URL here"
        )
        
        playback_speed = st.select_slider(
            "⚡ Playback Speed",
            options=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0],
            value=settings['default_speed'],
            format_func=lambda x: f"{x}x"
        )
        
        auto_quiz = st.checkbox("🤖 Auto-solve Quizzes", value=settings['auto_quiz'])
        video_limit = st.number_input("🎯 Video Limit (0 = unlimited)", min_value=0, value=0)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Start", use_container_width=True):
                if playlist_url:
                    st.success("✅ Automation started!")
                    # Run automation in background with user_id
                    def run_in_thread():
                        try:
                            run_automation(platform, playlist_url, None, auto_quiz, 
                                         video_limit if video_limit > 0 else None, 
                                         playback_speed, user_id=user['id'])
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    
                    thread = threading.Thread(target=run_in_thread, daemon=True)
                    thread.start()
                else:
                    st.warning("⚠️ Please enter a URL")
        
        with col2:
            if st.button("💾 Save Settings", use_container_width=True):
                auth.update_user_settings(user['id'], {
                    'default_speed': playback_speed,
                    'auto_quiz': auto_quiz
                })
                st.success("✅ Settings saved!")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    # Main content
    # Statistics Cards
    stats = auth.get_user_stats(user['id'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{stats['videos_completed']}</div>
            <div class="metric-label">📹 Videos Watched</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{stats['total_playlists']}</div>
            <div class="metric-label">📚 Playlists</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{stats['quiz_accuracy']}%</div>
            <div class="metric-label">🎯 Quiz Accuracy</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{stats['total_quizzes']}</div>
            <div class="metric-label">📝 Quizzes Solved</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Dashboard", 
        "📚 Playlist Progress", 
        "📝 Quiz History",
        "📈 Analytics",
        "🤖 AI Summaries",
        "📓 My Notes",
        "⚙️ Settings"
    ])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📈 Recent Activity")
            logs = db.get_recent_logs(limit=10)
            
            if logs:
                for log in logs:
                    status_emoji = {
                        'success': '✅',
                        'error': '❌',
                        'warning': '⚠️',
                        'info': 'ℹ️'
                    }.get(log['status'], 'ℹ️')
                    
                    st.markdown(f"{status_emoji} **{log['action_type']}** - {log['message']}")
                    st.caption(log['timestamp'])
                    st.markdown("---")
            else:
                st.info("No activity yet. Start your first automation!")
        
        with col2:
            st.markdown("### 🎯 Quick Actions")
            
            if st.button("🔄 Refresh Data", key="refresh_data_btn", use_container_width=True):
                # Clear all caches
                st.cache_data.clear()
                st.cache_resource.clear()
                # Immediately rerun without showing message (message would prevent rerun)
                st.rerun()
            
            if st.button("📄 Download PDF Report", key="download_pdf_btn", use_container_width=True):
                try:
                    with st.spinner("Generating PDF report..."):
                        # Ensure user data is available
                        if not user or 'id' not in user or 'username' not in user:
                            st.error("❌ User session error. Please logout and login again.")
                        else:
                            # Generate PDF report
                            pdf_path = generate_user_report(
                                user_id=user.get('id'),
                                username=user.get('username', 'User')
                            )
                            
                            # Read the PDF file
                            with open(pdf_path, 'rb') as pdf_file:
                                pdf_data = pdf_file.read()
                            
                            # Provide download button
                            st.success("✅ Report generated successfully!")
                            st.download_button(
                                label="📥 Download Report",
                                data=pdf_data,
                                file_name=f"learning_report_{user.get('username', 'user')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        
                except Exception as e:
                    st.error(f"❌ Error generating report: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
                    st.info("💡 Make sure reportlab is installed: pip install reportlab")
            
            if st.button("📊 View Full Stats", key="view_stats_btn", use_container_width=True):
                # Show detailed statistics modal
                st.markdown("---")
                st.markdown("### 📊 Detailed Statistics")
                
                # Get all videos
                completed_videos = db.get_completed_videos()
                quiz_stats = db.get_quiz_stats()
                recent_logs = db.get_recent_logs(limit=50)
                playlists = db.get_playlist_progress()
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Total Videos", len(completed_videos))
                with col_b:
                    st.metric("Total Quizzes", quiz_stats['total_attempts'])
                with col_c:
                    total_playlist_videos = sum([p['total_videos_watched'] for p in playlists])
                    st.metric("Playlist Videos", total_playlist_videos)
                
                st.markdown("#### 📹 Recently Completed Videos")
                if completed_videos:
                    video_df = pd.DataFrame(completed_videos[:10])
                    # Check which columns exist and display accordingly
                    display_cols = []
                    if 'title' in video_df.columns:
                        display_cols.append('title')
                    if 'watched_at' in video_df.columns:
                        display_cols.append('watched_at')
                    elif 'completed_at' in video_df.columns:
                        display_cols.append('completed_at')
                    
                    if display_cols:
                        st.dataframe(video_df[display_cols], use_container_width=True)
                    else:
                        st.dataframe(video_df, use_container_width=True)
                else:
                    st.info("No videos completed yet")
                
                st.markdown("#### 📝 Quiz Performance")
                st.write(f"Accuracy: {quiz_stats['accuracy']:.1f}%")
                st.write(f"Total Attempts: {quiz_stats['total_attempts']}")
                st.write(f"Correct Answers: {quiz_stats['correct_answers']}")
                
                st.markdown("---")
            
            if st.button("📖 Tutorial", key="tutorial_btn", use_container_width=True):
                st.markdown("---")
                st.markdown("### 📖 Quick Tutorial")
                st.markdown("""
                **Getting Started:**
                1. Paste a YouTube playlist URL in the input box above
                2. Set your preferred playback speed (1.0x - 2.0x)
                3. Click "🚀 Start Automation"
                4. The browser will open and start playing videos
                
                **Controls:**
                - ⏸️ **Manual Pause**: Click pause button anytime - automation waits
                - ⏩ **Speed Control**: Set speed before starting - persists for all videos
                - 📊 **Real-time Progress**: Dashboard updates immediately after each video
                
                **Features:**
                - ✅ Auto-skip ads
                - ✅ Auto-advance to next video
                - ✅ Progress tracking
                - ✅ Multi-user support
                
                **Tips:**
                - Use 2.0x speed for long playlists
                - Check "Playlist Progress" tab to track multiple playlists
                - Refresh data to see latest progress
                """)
                st.markdown("---")
            
            st.markdown("### 💡 Pro Tips")
            st.markdown("""
            - Use **2.0x speed** for long playlists
            - Enable **auto-quiz** to save time
            - Check **Playlist Progress** tab for tracking
            - Press **Ctrl+C** to stop automation
            """)
    
    with tab2:
        st.markdown("### 📚 Playlist Progress Tracking")
        
        playlists = db.get_playlist_progress()
        
        if playlists:
            for playlist in playlists:
                with st.expander(f"📺 {playlist['playlist_url'][:60]}... ({playlist['total_videos_watched']} videos)", expanded=False):
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric("Videos Watched", playlist['total_videos_watched'])
                    
                    with col_b:
                        status = "✅ Complete" if playlist['is_complete'] else "⏳ In Progress"
                        st.info(status)
                    
                    with col_c:
                        if playlist['last_watched_at']:
                            st.caption(f"Last: {playlist['last_watched_at']}")
                    
                    # Progress bar
                    if playlist['total_videos_watched'] > 0:
                        st.progress(min(playlist['total_videos_watched'] / 100, 1.0))
        else:
            st.markdown('''
            <div class="info-box">
                <h3>🚀 Start Your First Playlist!</h3>
                <p>Paste a YouTube playlist URL in the sidebar and click "Start" to begin tracking your progress.</p>
            </div>
            ''', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 📝 Quiz Performance")
        
        quiz_stats = db.get_quiz_stats(platform)
        
        if quiz_stats['total_attempts'] > 0:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Attempts", quiz_stats['total_attempts'])
            with col2:
                st.metric("Correct Answers", quiz_stats['correct_answers'])
            with col3:
                st.metric("Accuracy", f"{quiz_stats['accuracy']}%")
            
            st.markdown("---")
            
            # Recent quizzes
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT question_text, user_answer, is_correct, attempted_at
                FROM quizzes
                ORDER BY attempted_at DESC
                LIMIT 10
            ''')
            
            quizzes = cursor.fetchall()
            conn.close()
            
            if quizzes:
                for quiz in quizzes:
                    status = "✅" if quiz[2] else "❌"
                    st.markdown(f"{status} **Q:** {quiz[0][:100]}...")
                    st.caption(f"Your answer: {quiz[1]} | {quiz[3]}")
                    st.markdown("---")
        else:
            st.info("No quiz attempts yet. Enable auto-quiz in settings!")
    
    with tab4:
        st.markdown("### 📈 Advanced Analytics")
        
        analytics = Analytics(user_id=user['id'])
        
        # Productivity Score
        col1, col2, col3 = st.columns(3)
        
        with col1:
            score = analytics.get_productivity_score()
            st.metric(
                "🎯 Productivity Score",
                f"{score}/100",
                delta="+5" if score > 50 else None
            )
        
        with col2:
            streak = analytics.get_learning_streak()
            st.metric(
                "🔥 Current Streak",
                f"{streak['current_streak']} days",
                delta=f"Best: {streak['longest_streak']}"
            )
        
        with col3:
            comparison = analytics.get_comparison_stats()
            st.metric(
                "📊 This Week",
                f"{comparison['this_week']} videos",
                delta=f"{comparison['change_percent']:+.1f}%" if comparison['last_week'] > 0 else None,
                delta_color="normal"
            )
        
        st.markdown("---")
        
        # Learning Insights
        st.markdown("### 💡 Your Learning Insights")
        insights = analytics.get_learning_insights()
        
        cols = st.columns(len(insights))
        for idx, insight in enumerate(insights):
            with cols[idx]:
                st.info(insight)
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Platform Distribution")
            platform_dist = analytics.get_platform_distribution()
            
            if platform_dist:
                fig = px.pie(
                    values=list(platform_dist.values()),
                    names=list(platform_dist.keys()),
                    title="Videos by Platform",
                    color_discrete_sequence=px.colors.sequential.Purples_r
                )
                fig.update_layout(showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data yet. Start watching videos!")
        
        with col2:
            st.markdown("### ⏰ Activity by Hour")
            time_dist = analytics.get_time_distribution()
            
            hours = list(range(24))
            counts = [time_dist.get(str(h), 0) for h in hours]
            
            if sum(counts) > 0:
                fig = go.Figure(data=[
                    go.Bar(
                        x=hours,
                        y=counts,
                        marker_color='rgb(102, 126, 234)'
                    )
                ])
                fig.update_layout(
                    title="Your Most Active Hours",
                    xaxis_title="Hour of Day",
                    yaxis_title="Activity Count",
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No activity data yet")
        
        st.markdown("---")
        
        # Daily Activity Chart
        st.markdown("### 📅 30-Day Activity Trend")
        daily_activity = analytics.get_daily_activity(days=30)
        
        if daily_activity:
            df = pd.DataFrame([
                {'Date': date, **stats}
                for date, stats in daily_activity.items()
            ]).sort_values('Date')
            
            fig = px.line(
                df,
                x='Date',
                y='total_actions',
                title="Your Learning Activity Over Time",
                markers=True
            )
            fig.update_traces(line_color='rgb(118, 75, 162)', line_width=3)
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Total Actions",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Start learning to see your activity trends!")
        
        # Weekly Summary
        st.markdown("---")
        st.markdown("### 📆 This Week's Summary")
        
        weekly = analytics.get_weekly_summary()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Videos Watched", weekly['videos_watched'])
        with col2:
            st.metric("Total Actions", weekly['total_actions'])
        with col3:
            st.metric("Week Starting", weekly['week_start'])
    
    with tab5:
        st.markdown("### 🤖 AI Video Summaries")
        
        # Import video summarizer
        from video_summarizer import VideoSummarizer
        summarizer = VideoSummarizer()
        
        # Get all summaries
        all_summaries = summarizer.get_all_summaries()
        
        if all_summaries:
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Summaries", len(all_summaries))
            with col2:
                platforms = set(s.get('platform', 'unknown') for s in all_summaries.values())
                st.metric("Platforms", len(platforms))
            with col3:
                total_duration = sum(s.get('duration_minutes', 0) for s in all_summaries.values())
                st.metric("Total Duration", f"{total_duration} min")
            with col4:
                avg_difficulty = sum(1 if s.get('difficulty') == 'Beginner' else 2 if s.get('difficulty') == 'Intermediate' else 3 for s in all_summaries.values()) / len(all_summaries)
                difficulty_label = "Beginner" if avg_difficulty < 1.5 else "Intermediate" if avg_difficulty < 2.5 else "Advanced"
                st.metric("Avg Difficulty", difficulty_label)
            
            st.markdown("---")
            
            # Search and filters
            col_search, col_platform, col_difficulty = st.columns([2, 1, 1])
            with col_search:
                search_query = st.text_input("🔍 Search summaries", placeholder="Search by title or topic...")
            with col_platform:
                platform_filter = st.selectbox("Platform", ["All"] + sorted(list(platforms)))
            with col_difficulty:
                difficulty_filter = st.selectbox("Difficulty", ["All", "Beginner", "Intermediate", "Advanced"])
            
            # Filter summaries
            filtered_summaries = []
            for url, summary in all_summaries.items():
                # Apply filters
                if platform_filter != "All" and summary.get('platform') != platform_filter:
                    continue
                if difficulty_filter != "All" and summary.get('difficulty') != difficulty_filter:
                    continue
                if search_query and search_query.lower() not in summary.get('quick_summary', '').lower() and search_query.lower() not in summary.get('topics_covered', []):
                    continue
                
                filtered_summaries.append((url, summary))
            
            st.markdown(f"### 📚 Showing {len(filtered_summaries)} summaries")
            
            # Display summaries
            for url, summary in sorted(filtered_summaries, key=lambda x: x[1].get('timestamp', ''), reverse=True)[:20]:
                with st.expander(f"📹 {summary.get('platform', 'Unknown').upper()} - {summary.get('quick_summary', 'No summary')[:80]}...", expanded=False):
                    col_info, col_meta = st.columns([3, 1])
                    
                    with col_info:
                        st.markdown(f"**Quick Summary:**")
                        st.info(summary.get('quick_summary', 'No summary available'))
                        
                        if summary.get('key_takeaways'):
                            st.markdown("**Key Takeaways:**")
                            for i, takeaway in enumerate(summary.get('key_takeaways', [])[:5], 1):
                                st.markdown(f"{i}. {takeaway}")
                        
                        if summary.get('topics_covered'):
                            st.markdown("**Topics Covered:**")
                            topics_text = ", ".join([f"`{topic}`" for topic in summary.get('topics_covered', [])])
                            st.markdown(topics_text)
                    
                    with col_meta:
                        st.markdown(f"**Platform:** {summary.get('platform', 'Unknown')}")
                        st.markdown(f"**Duration:** {summary.get('duration_minutes', 0)} min")
                        st.markdown(f"**Difficulty:** {summary.get('difficulty', 'Intermediate')}")
                        if summary.get('timestamp'):
                            date = datetime.fromisoformat(summary['timestamp']).strftime('%b %d, %Y')
                            st.markdown(f"**Date:** {date}")
                        st.markdown(f"**Method:** {summary.get('method', 'local').replace('_', ' ').title()}")
                    
                    # Quiz questions
                    if summary.get('quiz_questions'):
                        st.markdown("---")
                        st.markdown("**📝 Quiz Questions:**")
                        for i, q in enumerate(summary.get('quiz_questions', []), 1):
                            st.markdown(f"**Q{i}:** {q.get('question', '')}")
                            if q.get('hint'):
                                st.caption(f"💡 Hint: {q['hint']}")
        else:
            st.markdown('''
            <div class="info-box">
                <h3>🚀 No Summaries Yet!</h3>
                <p>AI summaries will appear here automatically after you complete videos with the Chrome extension.</p>
                <p><strong>How to get summaries:</strong></p>
                <ol>
                    <li>Install the Chrome extension</li>
                    <li>Start automation on any video</li>
                    <li>Complete watching the video</li>
                    <li>AI summary will be generated automatically!</li>
                </ol>
            </div>
            ''', unsafe_allow_html=True)
    
    with tab6:
        st.markdown("### 📓 My Timestamped Notes")
        
        # Import note manager
        from note_manager import NoteManager
        note_manager = NoteManager()
        
        # Get all notes
        all_notes = note_manager.get_notes()
        
        if all_notes:
            # Note statistics
            stats = note_manager.get_statistics()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Notes", stats['total_notes'])
            with col2:
                st.metric("Videos", stats['total_videos'])
            with col3:
                st.metric("Avg per Video", stats['average_notes_per_video'])
            with col4:
                st.metric("Total Tags", stats['total_tags'])
            
            st.markdown("---")
            
            # Search and filters
            col_search, col_platform, col_tag = st.columns([2, 1, 1])
            with col_search:
                note_search = st.text_input("🔍 Search notes", placeholder="Search by content, title, or tags...")
            with col_platform:
                note_platforms = list(stats['platforms'].keys())
                platform_note_filter = st.selectbox("Platform Filter", ["All"] + note_platforms)
            with col_tag:
                if stats['tags']:
                    tag_filter = st.selectbox("Tag Filter", ["All"] + stats['tags'])
                else:
                    tag_filter = "All"
            
            # Apply filters
            filtered_notes = all_notes
            
            if note_search:
                filtered_notes = note_manager.search_notes(note_search)
            
            if platform_note_filter != "All":
                filtered_notes = [n for n in filtered_notes if n.get('platform') == platform_note_filter]
            
            if tag_filter != "All":
                filtered_notes = [n for n in filtered_notes if tag_filter in n.get('tags', [])]
            
            st.markdown(f"### 📝 Showing {len(filtered_notes)} notes")
            
            # Export button
            if st.button("📤 Export All Notes to Markdown", use_container_width=True):
                markdown_export = note_manager.export_notes(format='markdown')
                st.download_button(
                    label="⬇️ Download Notes.md",
                    data=markdown_export,
                    file_name=f"video_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            st.markdown("---")
            
            # Group notes by video
            notes_by_video = {}
            for note in filtered_notes[:50]:  # Show max 50 notes
                video_url = note.get('video_url', 'Unknown')
                if video_url not in notes_by_video:
                    notes_by_video[video_url] = []
                notes_by_video[video_url].append(note)
            
            # Display notes grouped by video
            for video_url, video_notes in notes_by_video.items():
                video_title = video_notes[0].get('video_title', 'Untitled Video')
                platform = video_notes[0].get('platform', 'unknown')
                
                with st.expander(f"📹 {platform.upper()} - {video_title} ({len(video_notes)} notes)", expanded=False):
                    for note in sorted(video_notes, key=lambda x: x.get('timestamp', 0)):
                        col_time, col_content = st.columns([1, 4])
                        
                        with col_time:
                            st.markdown(f"**⏱️ {note.get('formatted_time', '00:00')}**")
                            if note.get('tags'):
                                for tag in note['tags']:
                                    st.markdown(f"`{tag}`")
                        
                        with col_content:
                            st.markdown(f"{note.get('note_text', 'No content')}")
                            created_date = datetime.fromisoformat(note['created_at']).strftime('%b %d, %Y %H:%M')
                            st.caption(f"📅 {created_date}")
                        
                        st.markdown("---")
        else:
            st.markdown('''
            <div class="info-box">
                <h3>📝 No Notes Yet!</h3>
                <p>Your timestamped notes will appear here after you take them in the Chrome extension.</p>
                <p><strong>How to take notes:</strong></p>
                <ol>
                    <li>Install the Chrome extension</li>
                    <li>While watching any video, press <strong>Ctrl+Shift+N</strong></li>
                    <li>Enter your note and optional tags</li>
                    <li>Click Save - note will sync here automatically!</li>
                </ol>
                <p><strong>💡 Pro Tip:</strong> Click timestamps in notes to jump to that exact moment in the video!</p>
            </div>
            ''', unsafe_allow_html=True)
    
    with tab7:
        st.markdown("### ⚙️ User Settings")
        
        with st.form("settings_form"):
            st.markdown("#### Preferences")
            
            col1, col2 = st.columns(2)
            
            with col1:
                default_speed = st.select_slider(
                    "Default Playback Speed",
                    options=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0],
                    value=settings['default_speed']
                )
                
                auto_quiz_setting = st.checkbox(
                    "Auto-solve Quizzes",
                    value=settings['auto_quiz']
                )
            
            with col2:
                notifications = st.checkbox(
                    "Enable Notifications",
                    value=settings['notifications']
                )
                
                theme = st.selectbox(
                    "Theme",
                    ["dark", "light"],
                    index=0 if settings['theme'] == 'dark' else 1
                )
            
            if st.form_submit_button("💾 Save Settings", use_container_width=True):
                # Check if theme changed
                theme_changed = settings['theme'] != theme
                
                # Update settings in database
                auth.update_user_settings(user['id'], {
                    'default_speed': default_speed,
                    'auto_quiz': auto_quiz_setting,
                    'notifications': notifications,
                    'theme': theme
                })
                
                # Update session state
                st.session_state.theme = theme
                
                st.success("✅ Settings updated successfully!")
                
                # If theme changed, reload the page to apply changes
                if theme_changed:
                    st.info("🔄 Reloading to apply theme changes...")
                    time.sleep(1)
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### 🔄 Extension Data Sync")
        st.markdown("""
        Sync your AI summaries and notes between the Chrome extension and dashboard.
        
        **Note:** Currently, data is stored separately in:
        - **Extension**: Chrome local storage
        - **Dashboard**: Local database files
        
        Use the sync feature to keep them in sync!
        """)
        
        col_sync1, col_sync2 = st.columns(2)
        
        with col_sync1:
            st.markdown("#### 📥 Import from Extension")
            st.markdown("Paste JSON data from Chrome extension to import summaries and notes.")
            
            summaries_json_text = st.text_area(
                "Paste Summaries JSON (from chrome.storage)",
                height=100,
                placeholder='{"https://youtube.com/...": {...}}'
            )
            
            notes_json_text = st.text_area(
                "Paste Notes JSON (from chrome.storage)",
                height=100,
                placeholder='{"https://youtube.com/...": [{...}]}'
            )
            
            if st.button("📥 Import Data", use_container_width=True):
                try:
                    from extension_sync import import_from_extension_json
                    import json
                    
                    summaries_data = json.loads(summaries_json_text) if summaries_json_text.strip() else None
                    notes_data = json.loads(notes_json_text) if notes_json_text.strip() else None
                    
                    stats = import_from_extension_json(summaries_data, notes_data)
                    
                    st.success(f"✅ Imported {stats['summaries']} summaries and {stats['notes']} notes!")
                    time.sleep(2)
                    st.rerun()
                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON format. Please check your input.")
                except Exception as e:
                    st.error(f"❌ Error importing data: {str(e)}")
        
        with col_sync2:
            st.markdown("#### 📤 Export to Extension")
            st.markdown("Export dashboard data to paste into Chrome extension.")
            
            if st.button("📤 Generate Export Package", use_container_width=True):
                try:
                    from extension_sync import export_for_extension
                    import json
                    
                    export_data = export_for_extension()
                    
                    st.success("✅ Export package generated!")
                    
                    st.markdown("**Copy this JSON:**")
                    st.code(json.dumps(export_data, indent=2), language='json')
                    
                    st.download_button(
                        label="⬇️ Download Export Package",
                        data=json.dumps(export_data, indent=2),
                        file_name=f"extension_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ Error generating export: {str(e)}")
        
        st.markdown("---")
        st.markdown("""
        **💡 How to Sync:**
        1. **From Extension to Dashboard**: Open Chrome DevTools (F12) → Console → Type `chrome.storage.local.get(['videoSummaries', 'videoNotes'], console.log)` → Copy JSON → Paste above
        2. **From Dashboard to Extension**: Click "Generate Export Package" → Copy JSON → Open extension popup → Paste in sync area
        """)


# Main app logic
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        dashboard_page()


if __name__ == "__main__":
    main()
