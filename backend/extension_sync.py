"""
Chrome Extension Data Sync
Allows syncing summaries from Chrome extension to dashboard
"""

import json
import os
from datetime import datetime
from video_summarizer import VideoSummarizer


class ExtensionDataSync:
    """Sync data between Chrome extension and dashboard"""
    
    def __init__(self):
        self.summarizer = VideoSummarizer()
        
        # Default Chrome extension storage paths (Windows)
        # Chrome stores extension data in: AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings
        # But we'll use a simpler approach - manual JSON export/import
        self.sync_folder = os.path.join(os.path.dirname(__file__), '..', 'data', 'sync')
        os.makedirs(self.sync_folder, exist_ok=True)
    
    def import_summaries_from_json(self, json_data):
        """
        Import summaries from Chrome extension JSON
        
        Args:
            json_data: Dictionary of summaries from Chrome storage
        
        Returns:
            Number of summaries imported
        """
        count = 0
        
        for video_url, summary_data in json_data.items():
            # Save summary using video summarizer
            summary = {
                'quick_summary': summary_data.get('quick_summary', ''),
                'key_takeaways': summary_data.get('key_takeaways', []),
                'topics_covered': summary_data.get('topics_covered', []),
                'action_items': summary_data.get('action_items', []),
                'difficulty': summary_data.get('difficulty', 'Intermediate'),
                'quiz_questions': summary_data.get('quiz_questions', []),
                'timestamp': summary_data.get('timestamp', datetime.now().isoformat()),
                'method': summary_data.get('method', 'local_analysis'),
                'duration_minutes': summary_data.get('duration_minutes', 0),
                'platform': summary_data.get('platform', 'unknown')
            }
            
            self.summarizer._save_summary(video_url, summary)
            count += 1
        
        return count
    

    
    def export_summaries_for_extension(self):
        """
        Export summaries in format compatible with Chrome extension
        
        Returns:
            JSON-compatible dictionary
        """
        summaries = self.summarizer.get_all_summaries()
        return summaries
    

    
    def save_sync_package(self):
        """
        Save a complete sync package for manual transfer
        
        Returns:
            Path to sync package file
        """
        package = {
            'exported_at': datetime.now().isoformat(),
            'summaries': self.export_summaries_for_extension()
        }
        
        filepath = os.path.join(self.sync_folder, f'sync_package_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(package, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_sync_package(self, filepath):
        """
        Load data from a sync package
        
        Args:
            filepath: Path to sync package JSON file
        
        Returns:
            Dictionary with import counts
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            package = json.load(f)
        
        summaries_count = 0
        
        if 'summaries' in package:
            summaries_count = self.import_summaries_from_json(package['summaries'])
        
        return {
            'summaries_imported': summaries_count,
            'exported_at': package.get('exported_at', 'Unknown')
        }


# Helper functions for easy use
def import_from_extension_json(summaries_json=None):
    """
    Quick import function
    
    Args:
        summaries_json: Dictionary of summaries
    
    Returns:
        Import statistics
    """
    sync = ExtensionDataSync()
    
    stats = {
        'summaries': 0
    }
    
    if summaries_json:
        stats['summaries'] = sync.import_summaries_from_json(summaries_json)
    
    return stats


def export_for_extension():
    """
    Quick export function
    
    Returns:
        Dictionary with summaries
    """
    sync = ExtensionDataSync()
    
    return {
        'summaries': sync.export_summaries_for_extension()
    }


if __name__ == "__main__":
    # Test sync
    sync = ExtensionDataSync()
    
    # Create a sync package
    package_path = sync.save_sync_package()
    print(f"Sync package saved to: {package_path}")
    
    # Show statistics
    from video_summarizer import VideoSummarizer
    
    summarizer = VideoSummarizer()
    
    all_summaries = summarizer.get_all_summaries()
    
    print(f"\nCurrent data:")
    print(f"  Summaries: {len(all_summaries)}")
