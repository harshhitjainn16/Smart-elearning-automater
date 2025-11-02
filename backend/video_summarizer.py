"""
Video Summarization Module
Automatically generates AI-powered summaries of completed videos
"""
import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional

class VideoSummarizer:
    """
    AI-powered video summarization using multiple providers:
    1. OpenAI GPT-4 (if API key available)
    2. Local summarization (fallback)
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        self.summaries_file = 'data/video_summaries.json'
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs('data', exist_ok=True)
        if not os.path.exists(self.summaries_file):
            with open(self.summaries_file, 'w') as f:
                json.dump({}, f)
    
    def summarize_video(self, video_data: Dict) -> Dict:
        """
        Generate comprehensive summary of a video
        
        Args:
            video_data: Dict containing video information
                - title: Video title
                - platform: Platform name (youtube, udemy, etc.)
                - url: Video URL
                - duration: Video duration in seconds
                - transcript: Video transcript (optional)
                
        Returns:
            Dict containing:
                - quick_summary: 3-sentence overview
                - key_takeaways: List of main points
                - topics_covered: List of topics
                - action_items: Things to do/remember
                - difficulty: Estimated difficulty level
                - quiz_questions: Auto-generated questions
                - timestamp: When summary was created
        """
        
        title = video_data.get('title', 'Unknown Video')
        platform = video_data.get('platform', 'unknown')
        transcript = video_data.get('transcript', '')
        
        print(f"📝 Generating summary for: {title}")
        
        # Try OpenAI first if API key is available
        if self.openai_api_key and transcript:
            summary = self._summarize_with_openai(video_data)
        else:
            # Fallback to local summarization
            summary = self._generate_local_summary(video_data)
        
        # Save summary
        self._save_summary(video_data['url'], summary)
        
        return summary
    
    def _summarize_with_openai(self, video_data: Dict) -> Dict:
        """Use OpenAI GPT-4 for advanced summarization"""
        
        prompt = f"""
        Analyze this educational video and provide a comprehensive summary:
        
        Title: {video_data['title']}
        Platform: {video_data['platform']}
        Duration: {video_data.get('duration', 0)} seconds
        Transcript: {video_data.get('transcript', 'Not available')}
        
        Please provide:
        1. A 3-sentence quick summary
        2. 5-7 key takeaways (bullet points)
        3. Main topics covered
        4. Action items or things to remember
        5. Difficulty level (Beginner/Intermediate/Advanced)
        6. 3 quiz questions to test understanding
        
        Format as JSON with keys: quick_summary, key_takeaways, topics_covered, 
        action_items, difficulty, quiz_questions
        """
        
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.openai_api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-4',
                    'messages': [
                        {'role': 'system', 'content': 'You are an expert at summarizing educational content.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.7,
                    'max_tokens': 1000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Parse JSON response
                try:
                    summary_data = json.loads(content)
                    summary_data['timestamp'] = datetime.now().isoformat()
                    summary_data['method'] = 'openai_gpt4'
                    print("✅ Summary generated with OpenAI GPT-4")
                    return summary_data
                except json.JSONDecodeError:
                    print("⚠️ OpenAI response not valid JSON, using fallback")
                    return self._generate_local_summary(video_data)
            else:
                print(f"⚠️ OpenAI API error: {response.status_code}")
                return self._generate_local_summary(video_data)
                
        except Exception as e:
            print(f"⚠️ OpenAI API error: {str(e)}")
            return self._generate_local_summary(video_data)
    
    def _generate_local_summary(self, video_data: Dict) -> Dict:
        """
        Generate summary using local analysis (fallback)
        This works without API keys
        """
        
        title = video_data.get('title', 'Unknown Video')
        platform = video_data.get('platform', 'unknown')
        duration = video_data.get('duration', 0)
        
        # Extract keywords from title for topics
        keywords = self._extract_keywords(title)
        
        # Generate summary based on available data
        summary = {
            'quick_summary': self._generate_quick_summary(video_data),
            'key_takeaways': self._generate_key_takeaways(video_data),
            'topics_covered': keywords,
            'action_items': [
                "Review the main concepts covered",
                "Practice examples from the video",
                "Take notes on key points"
            ],
            'difficulty': self._estimate_difficulty(title),
            'quiz_questions': self._generate_quiz_questions(video_data),
            'timestamp': datetime.now().isoformat(),
            'method': 'local_analysis',
            'duration_minutes': round(duration / 60, 1)
        }
        
        print("✅ Summary generated with local analysis")
        return summary
    
    def _generate_quick_summary(self, video_data: Dict) -> str:
        """Generate a 3-sentence summary"""
        
        title = video_data['title']
        platform = video_data['platform']
        duration = video_data.get('duration', 0)
        duration_min = round(duration / 60, 1)
        
        return (
            f"This video titled '{title}' from {platform} covers educational content in {duration_min} minutes. "
            f"The material presents key concepts and practical knowledge for learners. "
            f"Viewers can expect to gain understanding of the main topic and its applications."
        )
    
    def _generate_key_takeaways(self, video_data: Dict) -> List[str]:
        """Generate key takeaways from video data"""
        
        title = video_data['title']
        keywords = self._extract_keywords(title)
        
        takeaways = [
            f"Understanding of {title}",
            "Practical knowledge applicable to real-world scenarios",
            "Foundation for further learning in this topic"
        ]
        
        # Add keyword-based takeaways
        for keyword in keywords[:3]:
            takeaways.append(f"Key concepts related to {keyword}")
        
        return takeaways[:7]  # Max 7 takeaways
    
    def _extract_keywords(self, title: str) -> List[str]:
        """Extract important keywords from title"""
        
        # Common stop words to filter out
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'how', 'what', 'when', 'where', 'why', 'which', 'this', 'that', 'these',
            'those', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
            'might', 'must', 'can', 'tutorial', 'guide', 'introduction', 'course',
            'lecture', 'lesson', 'part', 'chapter', 'section', 'complete', 'full'
        }
        
        # Extract words
        words = title.lower().split()
        keywords = [
            word.strip('.,!?:;()[]{}')
            for word in words
            if word.lower() not in stop_words and len(word) > 3
        ]
        
        return keywords[:10]  # Return top 10 keywords
    
    def _estimate_difficulty(self, title: str) -> str:
        """Estimate difficulty level from title"""
        
        title_lower = title.lower()
        
        beginner_keywords = ['beginner', 'introduction', 'basics', 'fundamental', 'getting started', '101', 'intro']
        advanced_keywords = ['advanced', 'expert', 'professional', 'master', 'deep dive', 'complete guide']
        
        for keyword in beginner_keywords:
            if keyword in title_lower:
                return 'Beginner'
        
        for keyword in advanced_keywords:
            if keyword in title_lower:
                return 'Advanced'
        
        return 'Intermediate'
    
    def _generate_quiz_questions(self, video_data: Dict) -> List[Dict]:
        """Generate quiz questions based on video content"""
        
        title = video_data['title']
        keywords = self._extract_keywords(title)
        
        questions = [
            {
                'question': f"What is the main topic covered in '{title}'?",
                'type': 'text',
                'hint': 'Think about the title and key concepts'
            },
            {
                'question': f"Can you explain the practical applications of what you learned?",
                'type': 'text',
                'hint': 'Consider real-world scenarios'
            },
            {
                'question': f"What are the key takeaways from this video?",
                'type': 'text',
                'hint': 'List 3-5 main points'
            }
        ]
        
        return questions
    
    def _save_summary(self, video_url: str, summary: Dict):
        """Save summary to persistent storage"""
        
        try:
            # Load existing summaries
            with open(self.summaries_file, 'r') as f:
                summaries = json.load(f)
            
            # Add new summary
            summaries[video_url] = summary
            
            # Save back
            with open(self.summaries_file, 'w') as f:
                json.dump(summaries, f, indent=2)
            
            print(f"💾 Summary saved for: {video_url}")
            
        except Exception as e:
            print(f"⚠️ Error saving summary: {str(e)}")
    
    def get_summary(self, video_url: str) -> Optional[Dict]:
        """Retrieve saved summary for a video"""
        
        try:
            with open(self.summaries_file, 'r') as f:
                summaries = json.load(f)
            return summaries.get(video_url)
        except:
            return None
    
    def get_all_summaries(self) -> Dict:
        """Get all saved summaries"""
        
        try:
            with open(self.summaries_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def get_recent_summaries(self, limit: int = 10) -> List[Dict]:
        """Get most recent summaries"""
        
        summaries = self.get_all_summaries()
        
        # Convert to list with URLs
        summary_list = [
            {**data, 'url': url}
            for url, data in summaries.items()
        ]
        
        # Sort by timestamp (newest first)
        summary_list.sort(
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )
        
        return summary_list[:limit]
    
    def search_summaries(self, query: str) -> List[Dict]:
        """Search summaries by keyword"""
        
        query_lower = query.lower()
        summaries = self.get_all_summaries()
        
        results = []
        for url, data in summaries.items():
            # Search in summary text, topics, and takeaways
            searchable_text = (
                data.get('quick_summary', '') + ' ' +
                ' '.join(data.get('topics_covered', [])) + ' ' +
                ' '.join(data.get('key_takeaways', []))
            ).lower()
            
            if query_lower in searchable_text:
                results.append({**data, 'url': url})
        
        return results


# Example usage
if __name__ == '__main__':
    summarizer = VideoSummarizer()
    
    # Example video data
    test_video = {
        'title': 'Introduction to Python Programming',
        'platform': 'youtube',
        'url': 'https://youtube.com/watch?v=example',
        'duration': 1800,  # 30 minutes
        'transcript': 'This video covers Python basics including variables, functions, and loops...'
    }
    
    # Generate summary
    summary = summarizer.summarize_video(test_video)
    
    print("\n" + "="*60)
    print("VIDEO SUMMARY")
    print("="*60)
    print(f"\nQuick Summary:\n{summary['quick_summary']}")
    print(f"\nKey Takeaways:")
    for i, takeaway in enumerate(summary['key_takeaways'], 1):
        print(f"  {i}. {takeaway}")
    print(f"\nTopics: {', '.join(summary['topics_covered'])}")
    print(f"Difficulty: {summary['difficulty']}")
    print(f"\nQuiz Questions:")
    for i, q in enumerate(summary['quiz_questions'], 1):
        print(f"  {i}. {q['question']}")
