"""
Authentication Module
Handles user registration, login, and session management
"""
import sqlite3
import hashlib
import os
from datetime import datetime
from typing import Optional, Dict
import secrets


class AuthManager:
    def __init__(self, db_path: str = 'data/users.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """Create database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize users database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                profile_picture TEXT
            )
        ''')
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # User settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                default_speed REAL DEFAULT 1.0,
                auto_quiz BOOLEAN DEFAULT 1,
                theme TEXT DEFAULT 'dark',
                notifications BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, email: str, password: str, full_name: str = None) -> bool:
        """Register a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, full_name))
            
            user_id = cursor.lastrowid
            
            # Create default settings
            cursor.execute('''
                INSERT INTO user_settings (user_id)
                VALUES (?)
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def login_user(self, username: str, password: str) -> Optional[Dict]:
        """Login user and return user data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        
        cursor.execute('''
            SELECT id, username, email, full_name, profile_picture
            FROM users
            WHERE username = ? AND password_hash = ? AND is_active = 1
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        
        if user:
            user_id = user[0]
            
            # Update last login
            cursor.execute('''
                UPDATE users
                SET last_login = ?
                WHERE id = ?
            ''', (datetime.now(), user_id))
            
            conn.commit()
            conn.close()
            
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'full_name': user[3],
                'profile_picture': user[4]
            }
        
        conn.close()
        return None
    
    def get_user_settings(self, user_id: int) -> Dict:
        """Get user settings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT default_speed, auto_quiz, theme, notifications
            FROM user_settings
            WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'default_speed': result[0],
                'auto_quiz': result[1],
                'theme': result[2],
                'notifications': result[3]
            }
        return {
            'default_speed': 1.0,
            'auto_quiz': True,
            'theme': 'dark',
            'notifications': True
        }
    
    def update_user_settings(self, user_id: int, settings: Dict):
        """Update user settings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_settings
            SET default_speed = ?, auto_quiz = ?, theme = ?, notifications = ?
            WHERE user_id = ?
        ''', (settings.get('default_speed', 1.0),
              settings.get('auto_quiz', True),
              settings.get('theme', 'dark'),
              settings.get('notifications', True),
              user_id))
        
        conn.commit()
        conn.close()
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get user statistics"""
        from database import Database
        db = Database(user_id=user_id)  # Create user-specific database instance
        
        # Get videos completed
        videos_completed = len(db.get_completed_videos())
        
        # Get playlists
        playlists = db.get_playlist_progress()
        total_playlists = len(playlists) if playlists else 0
        
        # Get quiz stats
        quiz_stats = db.get_quiz_stats()
        
        return {
            'videos_completed': videos_completed,
            'total_playlists': total_playlists,
            'quiz_accuracy': quiz_stats.get('accuracy', 0),
            'total_quizzes': quiz_stats.get('total_attempts', 0)
        }
