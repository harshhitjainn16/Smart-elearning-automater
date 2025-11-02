"""
Note Manager for Smart E-Learning Automator
Handles timestamped notes for videos across all platforms
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any


class NoteManager:
    """Manages timestamped notes for educational videos"""
    
    def __init__(self, storage_dir: str = "data/notes"):
        """
        Initialize NoteManager
        
        Args:
            storage_dir: Directory to store notes JSON file
        """
        self.storage_dir = storage_dir
        self.notes_file = os.path.join(storage_dir, "video_notes.json")
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
        
        # Load existing notes or initialize empty dict
        self.notes = self._load_notes()
    
    def _load_notes(self) -> Dict[str, List[Dict]]:
        """Load notes from JSON file"""
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading notes: {e}")
                return {}
        return {}
    
    def _save_notes(self):
        """Save notes to JSON file"""
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving notes: {e}")
    
    def add_note(
        self,
        video_url: str,
        timestamp: int,
        note_text: str,
        video_title: str = "",
        platform: str = "",
        tags: List[str] = None
    ) -> Dict[str, Any]:
        """
        Add a timestamped note to a video
        
        Args:
            video_url: URL of the video
            timestamp: Time in seconds when note was taken
            note_text: The actual note content
            video_title: Title of the video (optional)
            platform: Platform name (youtube, udemy, etc.)
            tags: Optional tags for categorization
        
        Returns:
            The created note object
        """
        # Initialize video notes list if doesn't exist
        if video_url not in self.notes:
            self.notes[video_url] = []
        
        # Create note object
        note = {
            "id": self._generate_note_id(),
            "timestamp": timestamp,
            "formatted_time": self._format_timestamp(timestamp),
            "note_text": note_text,
            "video_title": video_title,
            "platform": platform,
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Add note and sort by timestamp
        self.notes[video_url].append(note)
        self.notes[video_url].sort(key=lambda x: x["timestamp"])
        
        # Save to file
        self._save_notes()
        
        return note
    
    def get_notes(
        self,
        video_url: Optional[str] = None,
        platform: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get notes with optional filters
        
        Args:
            video_url: Filter by specific video URL
            platform: Filter by platform
            tags: Filter by tags (returns notes with any of the tags)
        
        Returns:
            List of notes matching filters
        """
        if video_url:
            # Get notes for specific video
            notes = self.notes.get(video_url, [])
        else:
            # Get all notes
            notes = []
            for video_notes in self.notes.values():
                notes.extend(video_notes)
        
        # Apply filters
        if platform:
            notes = [n for n in notes if n.get("platform") == platform]
        
        if tags:
            notes = [n for n in notes if any(tag in n.get("tags", []) for tag in tags)]
        
        # Sort by created date (newest first)
        notes.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return notes
    
    def update_note(
        self,
        video_url: str,
        note_id: str,
        note_text: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Update an existing note
        
        Args:
            video_url: URL of the video
            note_id: ID of the note to update
            note_text: New note text (if provided)
            tags: New tags (if provided)
        
        Returns:
            Updated note or None if not found
        """
        if video_url not in self.notes:
            return None
        
        for note in self.notes[video_url]:
            if note["id"] == note_id:
                if note_text is not None:
                    note["note_text"] = note_text
                if tags is not None:
                    note["tags"] = tags
                note["updated_at"] = datetime.now().isoformat()
                
                self._save_notes()
                return note
        
        return None
    
    def delete_note(self, video_url: str, note_id: str) -> bool:
        """
        Delete a note
        
        Args:
            video_url: URL of the video
            note_id: ID of the note to delete
        
        Returns:
            True if deleted, False if not found
        """
        if video_url not in self.notes:
            return False
        
        original_length = len(self.notes[video_url])
        self.notes[video_url] = [
            n for n in self.notes[video_url] if n["id"] != note_id
        ]
        
        if len(self.notes[video_url]) < original_length:
            # Remove video key if no notes left
            if not self.notes[video_url]:
                del self.notes[video_url]
            
            self._save_notes()
            return True
        
        return False
    
    def search_notes(self, query: str) -> List[Dict[str, Any]]:
        """
        Search notes by text content
        
        Args:
            query: Search query (case-insensitive)
        
        Returns:
            List of notes containing the query
        """
        query_lower = query.lower()
        results = []
        
        for video_url, video_notes in self.notes.items():
            for note in video_notes:
                # Search in note text, video title, and tags
                searchable_text = " ".join([
                    note.get("note_text", ""),
                    note.get("video_title", ""),
                    " ".join(note.get("tags", []))
                ]).lower()
                
                if query_lower in searchable_text:
                    results.append({**note, "video_url": video_url})
        
        # Sort by relevance (created date)
        results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about notes
        
        Returns:
            Dictionary with note statistics
        """
        total_notes = sum(len(notes) for notes in self.notes.values())
        total_videos = len(self.notes)
        
        # Count by platform
        platform_counts = {}
        all_tags = set()
        
        for video_notes in self.notes.values():
            for note in video_notes:
                platform = note.get("platform", "unknown")
                platform_counts[platform] = platform_counts.get(platform, 0) + 1
                all_tags.update(note.get("tags", []))
        
        return {
            "total_notes": total_notes,
            "total_videos": total_videos,
            "average_notes_per_video": round(total_notes / total_videos, 2) if total_videos > 0 else 0,
            "platforms": platform_counts,
            "total_tags": len(all_tags),
            "tags": sorted(list(all_tags))
        }
    
    def export_notes(
        self,
        format: str = "markdown",
        video_url: Optional[str] = None
    ) -> str:
        """
        Export notes to various formats
        
        Args:
            format: Export format ('markdown', 'text', 'json')
            video_url: Optional video URL to export specific video notes
        
        Returns:
            Formatted string of notes
        """
        notes = self.get_notes(video_url=video_url)
        
        if format == "json":
            return json.dumps(notes, indent=2, ensure_ascii=False)
        
        elif format == "markdown":
            output = "# Video Notes\n\n"
            
            # Group by video
            videos = {}
            for note in notes:
                url = note.get("video_url", "Unknown")
                if url not in videos:
                    videos[url] = []
                videos[url].append(note)
            
            for url, video_notes in videos.items():
                if video_notes:
                    title = video_notes[0].get("video_title", "Untitled Video")
                    platform = video_notes[0].get("platform", "unknown")
                    
                    output += f"## {title}\n"
                    output += f"**Platform:** {platform.title()}\n"
                    output += f"**URL:** {url}\n\n"
                    
                    for note in video_notes:
                        output += f"### [{note['formatted_time']}] {note.get('note_text', '')}\n"
                        if note.get("tags"):
                            output += f"*Tags: {', '.join(note['tags'])}*\n"
                        output += "\n"
                    
                    output += "---\n\n"
            
            return output
        
        else:  # text format
            output = "VIDEO NOTES\n" + "=" * 50 + "\n\n"
            
            for note in notes:
                output += f"[{note['formatted_time']}] {note.get('note_text', '')}\n"
                output += f"Video: {note.get('video_title', 'Unknown')}\n"
                output += f"Platform: {note.get('platform', 'unknown')}\n"
                if note.get("tags"):
                    output += f"Tags: {', '.join(note['tags'])}\n"
                output += f"Created: {note.get('created_at', '')}\n"
                output += "-" * 50 + "\n\n"
            
            return output
    
    def _generate_note_id(self) -> str:
        """Generate unique note ID"""
        return f"note_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    def _format_timestamp(self, seconds: int) -> str:
        """
        Format seconds to HH:MM:SS or MM:SS
        
        Args:
            seconds: Time in seconds
        
        Returns:
            Formatted time string
        """
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"


# Example usage and testing
if __name__ == "__main__":
    # Initialize manager
    manager = NoteManager()
    
    # Add some test notes
    note1 = manager.add_note(
        video_url="https://www.youtube.com/watch?v=test123",
        timestamp=125,
        note_text="Important concept about recursion explained clearly",
        video_title="Introduction to Python Programming",
        platform="youtube",
        tags=["important", "recursion", "python"]
    )
    print(f"Added note: {note1}")
    
    note2 = manager.add_note(
        video_url="https://www.youtube.com/watch?v=test123",
        timestamp=450,
        note_text="Good example of using list comprehensions",
        video_title="Introduction to Python Programming",
        platform="youtube",
        tags=["example", "python"]
    )
    print(f"Added note: {note2}")
    
    # Get all notes for video
    video_notes = manager.get_notes("https://www.youtube.com/watch?v=test123")
    print(f"\nNotes for video: {len(video_notes)} notes")
    
    # Search notes
    results = manager.search_notes("recursion")
    print(f"\nSearch results for 'recursion': {len(results)} notes")
    
    # Get statistics
    stats = manager.get_statistics()
    print(f"\nStatistics: {stats}")
    
    # Export to markdown
    markdown = manager.export_notes(format="markdown")
    print(f"\nMarkdown export:\n{markdown[:200]}...")
