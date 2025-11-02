"""
Main entry point for Smart E-Learning Automator
"""
import argparse
import logging
from video_automator import VideoAutomator
from quiz_solver import QuizSolver
from database import Database
import time


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def run_automation(platform: str, playlist_url: str, credentials: dict = None, 
                   auto_quiz: bool = True, video_limit: int = None, playback_speed: float = 1.0,
                   user_id: int = None):
    """
    Run the complete automation
    
    Args:
        platform: Learning platform (youtube, coursera, udemy, moodle)
        playlist_url: URL of the playlist/course
        credentials: Login credentials (if required)
        auto_quiz: Whether to automatically solve quizzes
        video_limit: Maximum number of videos to watch (None = all)
        playback_speed: Video speed (0.5x to 2.0x, default 1.0x)
        user_id: User ID for multi-user support (creates user-specific database)
    """
    db = Database(user_id=user_id)  # Create user-specific database
    video_automator = None
    
    try:
        logger.info(f"Starting automation for {platform} at {playback_speed}x speed (user_id: {user_id})")
        db.add_log('automation_start', f'Starting automation for {platform} at {playback_speed}x speed', 'info')
        
        # Initialize video automator with user_id
        video_automator = VideoAutomator(platform=platform, headless=False, 
                                        playback_speed=playback_speed, user_id=user_id)
        video_automator.init_driver()
        
        # Login if credentials provided
        if credentials:
            video_automator.login(credentials)
        
        # Navigate to playlist
        video_automator.navigate_to_playlist(playlist_url)
        
        # Initialize quiz solver if needed
        quiz_solver = None
        if auto_quiz:
            quiz_solver = QuizSolver(platform=platform, driver=video_automator.driver)
        
        # Use the enhanced automate_playlist function
        # This handles all error recovery, progress tracking, and autoplay issues
        video_automator.automate_playlist(
            playlist_url=playlist_url,
            video_limit=video_limit,
            playback_speed=playback_speed
        )
        
        logger.info("✅ Automation complete!")
        db.add_log('automation_complete', f'Playlist automation finished', 'success')
        
        # Show stats
        stats = db.get_quiz_stats(platform)
        logger.info(f"Quiz Stats: {stats}")
        
    except Exception as e:
        logger.error(f"Automation error: {str(e)}")
        db.add_log('automation_error', str(e), 'error')
        raise
    
    finally:
        if video_automator:
            video_automator.close()


def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(description='Smart E-Learning Automator')
    
    parser.add_argument('--platform', required=True, 
                       choices=['youtube', 'coursera', 'udemy', 'moodle'],
                       help='Learning platform')
    
    parser.add_argument('--url', required=True, 
                       help='Playlist/Course URL')
    
    parser.add_argument('--username', 
                       help='Login username/email')
    
    parser.add_argument('--password', 
                       help='Login password')
    
    parser.add_argument('--no-quiz', action='store_true',
                       help='Disable automatic quiz solving')
    
    parser.add_argument('--limit', type=int,
                       help='Maximum number of videos to watch')
    
    parser.add_argument('--speed', type=float, default=1.0,
                       choices=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0],
                       help='Video playback speed (0.5x to 2.0x, default: 1.0x)')
    
    parser.add_argument('--dashboard', action='store_true',
                       help='Launch Streamlit dashboard instead')
    
    args = parser.parse_args()
    
    if args.dashboard:
        logger.info("Launching dashboard...")
        import subprocess
        subprocess.run(['streamlit', 'run', 'dashboard.py'])
        return
    
    # Prepare credentials
    credentials = None
    if args.username and args.password:
        credentials = {
            'username': args.username,
            'password': args.password
        }
    
    # Run automation
    run_automation(
        platform=args.platform,
        playlist_url=args.url,
        credentials=credentials,
        auto_quiz=not args.no_quiz,
        video_limit=args.limit,
        playback_speed=args.speed
    )


if __name__ == '__main__':
    main()
