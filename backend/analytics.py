"""
Advanced Analytics Module
Provides detailed insights and visualizations for learning progress
"""
from database import Database
from datetime import datetime, timedelta
from typing import Dict, List
import json


class Analytics:
    """Advanced analytics for learning progress"""
    
    def __init__(self, user_id: int = None):
        self.user_id = user_id
        self.db = Database(user_id=user_id)
    
    def get_daily_activity(self, days: int = 30) -> Dict:
        """Get daily activity for the last N days"""
        logs = self.db.get_recent_logs(limit=1000)
        
        # Group by date
        activity_by_date = {}
        for log in logs:
            try:
                timestamp = datetime.fromisoformat(log['timestamp'])
                date_key = timestamp.strftime('%Y-%m-%d')
                if date_key not in activity_by_date:
                    activity_by_date[date_key] = {
                        'videos': 0,
                        'quizzes': 0,
                        'total_actions': 0
                    }
                
                activity_by_date[date_key]['total_actions'] += 1
                
                if 'video' in log['action_type'].lower():
                    activity_by_date[date_key]['videos'] += 1
                elif 'quiz' in log['action_type'].lower():
                    activity_by_date[date_key]['quizzes'] += 1
            except:
                pass
        
        return activity_by_date
    
    def get_learning_streak(self) -> Dict:
        """Calculate current learning streak"""
        logs = self.db.get_recent_logs(limit=1000)
        
        if not logs:
            return {'current_streak': 0, 'longest_streak': 0, 'last_activity': None}
        
        # Get unique dates with activity
        active_dates = set()
        for log in logs:
            try:
                timestamp = datetime.fromisoformat(log['timestamp'])
                active_dates.add(timestamp.date())
            except:
                pass
        
        if not active_dates:
            return {'current_streak': 0, 'longest_streak': 0, 'last_activity': None}
        
        sorted_dates = sorted(active_dates, reverse=True)
        
        # Calculate current streak
        current_streak = 0
        today = datetime.now().date()
        
        for i, date in enumerate(sorted_dates):
            if i == 0:
                if date == today or date == today - timedelta(days=1):
                    current_streak = 1
                else:
                    break
            else:
                expected_date = sorted_dates[i-1] - timedelta(days=1)
                if date == expected_date:
                    current_streak += 1
                else:
                    break
        
        # Calculate longest streak
        longest_streak = 1
        temp_streak = 1
        prev_date = None
        
        for date in sorted(active_dates):
            if prev_date:
                if date == prev_date + timedelta(days=1):
                    temp_streak += 1
                    longest_streak = max(longest_streak, temp_streak)
                else:
                    temp_streak = 1
            prev_date = date
        
        return {
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'last_activity': sorted_dates[0].isoformat() if sorted_dates else None
        }
    
    def get_platform_distribution(self) -> Dict:
        """Get distribution of videos by platform"""
        videos = self.db.get_completed_videos()
        
        platforms = {}
        for video in videos:
            platform = video.get('platform', 'Unknown')
            platforms[platform] = platforms.get(platform, 0) + 1
        
        return platforms
    
    def get_time_distribution(self) -> Dict:
        """Get activity distribution by hour of day"""
        logs = self.db.get_recent_logs(limit=1000)
        
        hours = {str(h): 0 for h in range(24)}
        
        for log in logs:
            try:
                timestamp = datetime.fromisoformat(log['timestamp'])
                hour = str(timestamp.hour)
                hours[hour] += 1
            except:
                pass
        
        return hours
    
    def get_weekly_summary(self) -> Dict:
        """Get this week's learning summary"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        
        logs = self.db.get_recent_logs(limit=1000)
        videos = self.db.get_completed_videos()
        
        # Filter this week's data
        this_week_videos = 0
        this_week_actions = 0
        
        for video in videos:
            try:
                watched_at = datetime.fromisoformat(video.get('watched_at', ''))
                if watched_at >= week_start:
                    this_week_videos += 1
            except:
                pass
        
        for log in logs:
            try:
                timestamp = datetime.fromisoformat(log['timestamp'])
                if timestamp >= week_start:
                    this_week_actions += 1
            except:
                pass
        
        return {
            'videos_watched': this_week_videos,
            'total_actions': this_week_actions,
            'week_start': week_start.strftime('%Y-%m-%d')
        }
    
    def get_productivity_score(self) -> int:
        """Calculate productivity score (0-100)"""
        videos = self.db.get_completed_videos()
        quiz_stats = self.db.get_quiz_stats()
        streak = self.get_learning_streak()
        weekly = self.get_weekly_summary()
        
        score = 0
        
        # Videos completed (max 40 points)
        score += min(len(videos), 40)
        
        # Quiz accuracy (max 30 points)
        score += min(int(quiz_stats.get('accuracy', 0) * 0.3), 30)
        
        # Learning streak (max 20 points)
        score += min(streak['current_streak'] * 2, 20)
        
        # Weekly activity (max 10 points)
        score += min(weekly['videos_watched'], 10)
        
        return min(score, 100)
    
    def get_learning_insights(self) -> List[str]:
        """Generate personalized learning insights"""
        insights = []
        
        videos = self.db.get_completed_videos()
        quiz_stats = self.db.get_quiz_stats()
        streak = self.get_learning_streak()
        weekly = self.get_weekly_summary()
        
        # Streak insights
        if streak['current_streak'] >= 7:
            insights.append(f"🔥 Amazing! You're on a {streak['current_streak']}-day streak!")
        elif streak['current_streak'] > 0:
            insights.append(f"💪 Keep it up! {streak['current_streak']}-day streak going!")
        else:
            insights.append("📅 Start a learning streak today!")
        
        # Quiz insights
        if quiz_stats.get('total_attempts', 0) > 0:
            accuracy = quiz_stats.get('accuracy', 0)
            if accuracy >= 90:
                insights.append(f"🌟 Excellent quiz performance: {accuracy:.1f}% accuracy!")
            elif accuracy >= 70:
                insights.append(f"👍 Good quiz scores: {accuracy:.1f}% accuracy")
            else:
                insights.append(f"📚 Practice more: {accuracy:.1f}% quiz accuracy")
        
        # Video insights
        if len(videos) >= 50:
            insights.append(f"🎓 Impressive! {len(videos)} videos completed!")
        elif len(videos) >= 20:
            insights.append(f"📺 Great progress: {len(videos)} videos done!")
        elif len(videos) > 0:
            insights.append(f"🚀 Getting started: {len(videos)} videos completed")
        
        # Weekly insights
        if weekly['videos_watched'] >= 10:
            insights.append(f"⚡ Productive week: {weekly['videos_watched']} videos!")
        
        # Motivational insights
        if len(insights) < 3:
            insights.append("💡 Consistency is key to mastery!")
            insights.append("🎯 Set a goal and track your progress!")
        
        return insights[:5]  # Return top 5 insights
    
    def get_comparison_stats(self) -> Dict:
        """Compare current week vs last week"""
        today = datetime.now()
        
        # This week
        this_week_start = today - timedelta(days=today.weekday())
        
        # Last week
        last_week_start = this_week_start - timedelta(days=7)
        last_week_end = this_week_start
        
        videos = self.db.get_completed_videos()
        
        this_week_count = 0
        last_week_count = 0
        
        for video in videos:
            try:
                watched_at = datetime.fromisoformat(video.get('watched_at', ''))
                if watched_at >= this_week_start:
                    this_week_count += 1
                elif last_week_start <= watched_at < last_week_end:
                    last_week_count += 1
            except:
                pass
        
        # Calculate percentage change
        if last_week_count > 0:
            change = ((this_week_count - last_week_count) / last_week_count) * 100
        else:
            change = 100 if this_week_count > 0 else 0
        
        return {
            'this_week': this_week_count,
            'last_week': last_week_count,
            'change_percent': round(change, 1),
            'trending_up': change > 0
        }
