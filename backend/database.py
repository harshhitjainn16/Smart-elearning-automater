"""
Database operations for Smart E-Learning Automator
Stores progress, quiz answers, and activity logs
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os
from config import DATABASE_PATH


class Database:
    def __init__(self, db_path: str = DATABASE_PATH, user_id: int = None):
        # If user_id provided, create user-specific database
        if user_id:
            db_dir = os.path.dirname(db_path)
            db_name = f'learning_progress_user_{user_id}.db'
            self.db_path = os.path.join(db_dir, db_name)
        else:
            self.db_path = db_path
        
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.user_id = user_id
        self.init_database()
    
    def get_connection(self):
        """Create a database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Videos table (user-specific if user_id is set)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                platform TEXT NOT NULL,
                video_url TEXT NOT NULL,
                title TEXT,
                playlist_id TEXT,
                duration INTEGER,
                watched_at TIMESTAMP,
                completed BOOLEAN DEFAULT 0,
                watch_time INTEGER DEFAULT 0,
                UNIQUE(user_id, video_url)
            )
        ''')
        
        # Quizzes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                platform TEXT NOT NULL,
                quiz_id TEXT,
                question_text TEXT NOT NULL,
                options TEXT,
                correct_answer TEXT,
                user_answer TEXT,
                is_correct BOOLEAN,
                confidence_score REAL,
                attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Activity logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                action_type TEXT NOT NULL,
                message TEXT,
                status TEXT,
                details TEXT
            )
        ''')
        
        # Playlist progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlist_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                playlist_url TEXT NOT NULL,
                total_videos_watched INTEGER DEFAULT 0,
                last_watched_at TIMESTAMP,
                last_video_url TEXT,
                is_complete BOOLEAN DEFAULT 0,
                UNIQUE(user_id, playlist_url)
            )
        ''')
        
        # Quiz answer cache
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_hash TEXT UNIQUE NOT NULL,
                question_text TEXT,
                cached_answer TEXT,
                success_rate REAL DEFAULT 1.0,
                times_used INTEGER DEFAULT 0,
                last_used TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_video(self, platform: str, video_url: str, title: str = None, 
                  playlist_id: str = None, duration: int = None):
        """Add a video to tracking"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO videos 
                (user_id, platform, video_url, title, playlist_id, duration)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.user_id, platform, video_url, title, playlist_id, duration))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def mark_video_completed(self, video_url: str):
        """Mark a video as completed"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        where_clause = 'WHERE video_url = ?'
        params = [datetime.now(), video_url]
        
        if self.user_id:
            where_clause += ' AND user_id = ?'
            params.append(self.user_id)
        
        cursor.execute(f'''
            UPDATE videos 
            SET completed = 1, watched_at = ?
            {where_clause}
        ''', params)
        
        conn.commit()
        conn.close()
    
    def get_completed_videos(self, platform: str = None) -> List[Dict]:
        """Get all completed videos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        where_clauses = ['completed = 1']
        params = []
        
        if self.user_id:
            where_clauses.append('user_id = ?')
            params.append(self.user_id)
        
        if platform:
            where_clauses.append('platform = ?')
            params.append(platform)
        
        where_str = ' AND '.join(where_clauses)
        
        cursor.execute(f'SELECT * FROM videos WHERE {where_str}', params)
        
        columns = [desc[0] for desc in cursor.description]
        videos = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return videos
    
    def save_quiz_attempt(self, platform: str, question_text: str, options: List[str],
                          user_answer: str, correct_answer: str = None, 
                          is_correct: bool = None, confidence: float = None):
        """Save quiz attempt"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO quizzes 
            (user_id, platform, question_text, options, user_answer, correct_answer, is_correct, confidence_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.user_id, platform, question_text, json.dumps(options), user_answer, correct_answer, is_correct, confidence))
        
        conn.commit()
        conn.close()
    
    def get_quiz_stats(self, platform: str = None) -> Dict:
        """Get quiz statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        where_clauses = []
        params = []
        
        if self.user_id:
            where_clauses.append('user_id = ?')
            params.append(self.user_id)
        
        if platform:
            where_clauses.append('platform = ?')
            params.append(platform)
        
        where_str = ' AND '.join(where_clauses) if where_clauses else '1=1'
        
        cursor.execute(f'''
            SELECT 
                COUNT(*) as total_attempts,
                SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct_answers,
                SUM(CASE WHEN is_correct = 0 THEN 1 ELSE 0 END) as wrong_answers,
                AVG(confidence_score) as avg_confidence
            FROM quizzes WHERE {where_str}
        ''', params)
        
        result = cursor.fetchone()
        conn.close()
        
        if result[0] > 0:
            accuracy = (result[1] / result[0]) * 100 if result[0] > 0 else 0
            return {
                'total_attempts': result[0],
                'correct_answers': result[1] or 0,
                'wrong_answers': result[2] or 0,
                'accuracy': round(accuracy, 2),
                'avg_confidence': round(result[3] or 0, 2)
            }
        return {'total_attempts': 0, 'correct_answers': 0, 'wrong_answers': 0, 'accuracy': 0, 'avg_confidence': 0}
    
    def add_log(self, action_type: str, message: str, status: str = 'info', details: str = None):
        """Add activity log"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO activity_logs (user_id, action_type, message, status, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.user_id, action_type, message, status, details))
        
        conn.commit()
        conn.close()
    
    def get_recent_logs(self, limit: int = 50) -> List[Dict]:
        """Get recent activity logs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        where_clause = ''
        params = []
        
        if self.user_id:
            where_clause = 'WHERE user_id = ?'
            params.append(self.user_id)
        
        cursor.execute(f'''
            SELECT * FROM activity_logs 
            {where_clause}
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', params + [limit])
        
        columns = [desc[0] for desc in cursor.description]
        logs = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return logs
    
    def cache_quiz_answer(self, question_text: str, answer: str):
        """Cache a quiz answer for future use"""
        import hashlib
        question_hash = hashlib.md5(question_text.encode()).hexdigest()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO quiz_cache 
            (question_hash, question_text, cached_answer, last_used)
            VALUES (?, ?, ?, ?)
        ''', (question_hash, question_text, answer, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_cached_answer(self, question_text: str) -> Optional[str]:
        """Get cached answer for a question"""
        import hashlib
        question_hash = hashlib.md5(question_text.encode()).hexdigest()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT cached_answer FROM quiz_cache 
            WHERE question_hash = ?
        ''', (question_hash,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def increment_video_count(self, playlist_url: str, count: int):
        """Update playlist progress - increment video count"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO playlist_progress (user_id, playlist_url, total_videos_watched, last_watched_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, playlist_url) 
            DO UPDATE SET 
                total_videos_watched = ?,
                last_watched_at = ?
        ''', (self.user_id, playlist_url, count, datetime.now(), count, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def update_playlist_progress(self, playlist_url: str, videos_watched: int, is_complete: bool = False):
        """Update playlist progress with final count"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO playlist_progress 
            (user_id, playlist_url, total_videos_watched, last_watched_at, is_complete)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, playlist_url) 
            DO UPDATE SET 
                total_videos_watched = ?,
                last_watched_at = ?,
                is_complete = ?
        ''', (self.user_id, playlist_url, videos_watched, datetime.now(), is_complete, 
              videos_watched, datetime.now(), is_complete))
        
        conn.commit()
        conn.close()
    
    def get_playlist_progress(self, playlist_url: str = None) -> Dict:
        """Get progress for a specific playlist or all playlists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if playlist_url:
            where_clause = 'WHERE playlist_url = ?'
            params = [playlist_url]
            
            if self.user_id:
                where_clause += ' AND user_id = ?'
                params.append(self.user_id)
            
            cursor.execute(f'SELECT * FROM playlist_progress {where_clause}', params)
            result = cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in cursor.description]
                progress = dict(zip(columns, result))
                conn.close()
                return progress
            else:
                conn.close()
                return None
        else:
            where_clause = ''
            params = []
            
            if self.user_id:
                where_clause = 'WHERE user_id = ?'
                params.append(self.user_id)
            
            cursor.execute(f'SELECT * FROM playlist_progress {where_clause} ORDER BY last_watched_at DESC', params)
            columns = [desc[0] for desc in cursor.description]
            progress = [dict(zip(columns, row)) for row in cursor.fetchall()]
            conn.close()
            return progress
