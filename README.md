# 🎓 Smart E-Learning Automator

An AI-powered Python automation tool that automatically plays video lectures and solves quizzes on various e-learning platforms.

## ⚠️ Disclaimer

**This project is for educational and demonstration purposes only.** Automating quizzes may violate the terms of service of some learning platforms. Use responsibly and at your own risk.

## ✨ Features

### 🎥 Video Automation
- **Auto-play** video lectures from playlists
- **Skip ads** and intros automatically
- **Playback speed control** - 0.5x to 2.0x (save up to 50% time!)
- **Track progress** - remembers which videos you've watched
- **Multi-platform support**: YouTube, Coursera, Udemy, Moodle

### 🧠 Smart Quiz Solving
- **AI-powered** quiz answering using NLP models (BERT/DistilBERT)
- **Answer caching** - remembers correct answers for repeated quizzes
- **Confidence scoring** - shows how confident the AI is in each answer
- **Web scraping** - extracts questions and options automatically

### 📊 Progress Tracking
- **SQLite database** stores all progress
- **Activity logs** for debugging and monitoring
- **Quiz statistics** - accuracy, attempts, confidence scores
- **Streamlit dashboard** for real-time monitoring

## 🛠️ Tech Stack

- **Selenium** - Browser automation
- **BeautifulSoup** - Web scraping
- **Transformers (HuggingFace)** - ML/NLP for quiz solving
- **FastAPI** - REST API (optional)
- **Streamlit** - Interactive dashboard
- **SQLite** - Local database

## 📋 Prerequisites

- Python 3.8+
- Chrome browser
- ChromeDriver (auto-installed by webdriver-manager)

## 🚀 Installation

### 1. Clone the Repository
```bash
cd smart-elearning-automater/backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Settings (Optional)
Create a `.env` file:
```env
API_HOST=0.0.0.0
API_PORT=8000
SECRET_KEY=your-secret-key-here
```

## 📖 Usage

### Method 1: Command Line Interface

#### Basic Usage (YouTube Playlist)
```bash
python main.py --platform youtube --url "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
```

#### With Login (Coursera)
```bash
python main.py --platform coursera --url "https://www.coursera.org/learn/course-name" --username "your@email.com" --password "yourpassword"
```

#### Limit Number of Videos
```bash
python main.py --platform udemy --url "YOUR_COURSE_URL" --limit 5
```

#### Disable Quiz Auto-Solving
```bash
python main.py --platform moodle --url "YOUR_MOODLE_URL" --no-quiz
```

#### Set Playback Speed (NEW!)
```bash
# 2x speed - Save 50% time
python main.py --platform youtube --url "YOUR_URL" --speed 2.0

# 1.5x speed - Balanced (save 33% time)
python main.py --platform coursera --url "YOUR_URL" --speed 1.5

# 1.25x speed - Slightly faster
python main.py --platform udemy --url "YOUR_URL" --speed 1.25
```

Available speeds: `0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0`

### Method 2: Streamlit Dashboard (Recommended)

```bash
python main.py --dashboard
```

Or directly:
```bash
streamlit run dashboard.py
```

This opens an interactive web interface at `http://localhost:8501` where you can:
- Start/stop automation
- Monitor progress in real-time
- View quiz statistics
- See activity logs

## 📂 Project Structure

```
smart-elearning-automater/
├── backend/
│   ├── main.py                 # Entry point
│   ├── video_automator.py      # Selenium video automation
│   ├── quiz_solver.py          # AI quiz solving
│   ├── database.py             # SQLite operations
│   ├── dashboard.py            # Streamlit dashboard
│   ├── config.py               # Configuration
│   ├── requirements.txt        # Dependencies
│   ├── models/                 # Saved ML models (auto-created)
│   └── platforms/              # Platform-specific configs
└── data/
    ├── learning_progress.db    # SQLite database (auto-created)
    └── automation.log          # Activity logs (auto-created)
```

## 🔧 How It Works

### Video Automation
1. Opens browser using Selenium
2. Logs in to platform (if credentials provided)
3. Navigates to playlist/course
4. Plays each video in sequence
5. Detects when video completes
6. Skips ads/intros automatically
7. Moves to next video
8. Logs all activity to database

### Quiz Solving
1. Detects quiz on page
2. Extracts question text and options using BeautifulSoup
3. Checks cache for previously correct answers
4. If not cached:
   - Uses DistilBERT QA model to analyze question
   - Scores each option
   - Selects highest confidence answer
5. Submits answer automatically
6. Caches answer if confidence > 70%

## 🎯 Supported Platforms

| Platform | Video Automation | Quiz Solving | Login Support |
|----------|-----------------|--------------|---------------|
| YouTube  | ✅              | ❌           | ❌            |
| Coursera | ✅              | ✅           | ✅            |
| Udemy    | ✅              | ✅           | ✅            |
| Moodle   | ✅              | ✅           | ✅            |

## 📊 Database Schema

The tool creates a SQLite database with these tables:

- **videos** - Tracks watched videos
- **quizzes** - Stores quiz attempts and answers
- **activity_logs** - All automation actions
- **quiz_cache** - Cached correct answers

## 🔒 Security Notes

- Credentials are **not** encrypted by default
- For production use, implement proper credential encryption
- Don't commit `.env` file to version control
- Use environment variables for sensitive data

## 🐛 Troubleshooting

### ChromeDriver Issues
```bash
pip install --upgrade webdriver-manager
```

### ML Model Download Stuck
The first run downloads ~250MB BERT model. Be patient.

### Platform Selector Not Working
Platform HTML changes frequently. Update selectors in `config.py`:
```python
PLATFORMS['platform_name']['selectors']['element'] = 'new-css-selector'
```

## 🚀 Future Enhancements

- [ ] Add more platforms (Khan Academy, edX, etc.)
- [ ] Real-time WebSocket updates
- [ ] Voice notifications (pyttsx3)
- [ ] Custom ML model training
- [ ] Docker containerization
- [ ] REST API for remote control
- [ ] Chrome extension interface

## 📝 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Created as a demonstration of Python automation + AI/ML integration

## 🙏 Acknowledgments

- HuggingFace Transformers for NLP models
- Selenium WebDriver team
- BeautifulSoup contributors

---

⚠️ **Remember**: Use this tool responsibly and ensure compliance with platform terms of service.
