"""
Configuration file for Smart E-Learning Automator
"""
import os
import platform
import getpass
from dotenv import load_dotenv

load_dotenv()

# Get unique identifier for this machine/user
MACHINE_ID = f"{platform.node()}_{getpass.getuser()}".replace(" ", "_")

# Platform Configurations
PLATFORMS = {
    'youtube': {
        'base_url': 'https://www.youtube.com',
        'selectors': {
            'video_player': 'video.html5-main-video',
            'next_button': 'a.ytp-next-button',
            'play_button': 'button.ytp-play-button',
            'ad_skip': 'button.ytp-ad-skip-button'
        }
    },
    'coursera': {
        'base_url': 'https://www.coursera.org',
        'selectors': {
            'video_player': 'video',
            'next_button': 'button[data-test="next-button"]',
            'quiz_container': 'div[data-test="quiz-question"]',
            'submit_button': 'button[type="submit"]'
        }
    },
    'udemy': {
        'base_url': 'https://www.udemy.com',
        'selectors': {
            'video_player': 'video.vp-center',
            'next_button': 'button[data-purpose="next-item"]',
            'quiz_option': 'label.mc-quiz-question--answer-label',
            'submit_button': 'button[data-purpose="submit-quiz"]'
        }
    },
    'moodle': {
        'base_url': '',  # User-configurable
        'selectors': {
            'video_player': 'video',
            'next_button': 'a.next-activity-link',
            'quiz_container': 'div.que',
            'submit_button': 'input[type="submit"]'
        }
    }
}

# Database Configuration - Unique per machine/user to prevent cross-device conflicts
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', f'learning_progress_{MACHINE_ID}.db')

# API Configuration
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 8000))
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Automation Settings
DEFAULT_WAIT_TIME = 5  # seconds
VIDEO_CHECK_INTERVAL = 2  # seconds
MAX_RETRIES = 3
DEFAULT_PLAYBACK_SPEED = 1.0  # 1x normal speed (options: 1.0, 1.25, 1.5, 2.0)
AVAILABLE_SPEEDS = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]

# ML Model Configuration
ML_MODEL_NAME = 'distilbert-base-cased-distilled-squad'
CONFIDENCE_THRESHOLD = 0.7

# Security Settings
ENCRYPT_CREDENTIALS = True
CREDENTIAL_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', '.credentials.enc')

# Logging - Unique per machine/user
LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', f'automation_{MACHINE_ID}.log')
