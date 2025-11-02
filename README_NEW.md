# 🎓 Smart E-Learning Automator

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50.0-FF4B4B)](https://streamlit.io/)
[![Selenium](https://img.shields.io/badge/Selenium-4.38.0-43B02A)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **An intelligent automation platform for e-learning that watches videos, tracks progress, generates reports, and provides advanced analytics**  — all while you focus on other tasks!

---

## ✨ Key Features

### 🤖 **Intelligent Automation**
- ✅ **Auto-play videos** with configurable playback speeds (0.5x - 2.0x)
- ✅ **Smart ad-skipping** - automatically bypasses advertisements
- ✅ **Playlist support** - handles 100+ video playlists seamlessly
- ✅ **Manual pause/resume** - full user control during automation
- ✅ **Persistent speed** - playback speed maintained across all videos
- ✅ **Real-time progress** - dashboard updates immediately

### 👥 **Multi-User Support**
- ✅ **Secure authentication** - SHA-256 password hashing
- ✅ **User-specific databases** - complete data isolation
- ✅ **Multi-device support** - works across different machines
- ✅ **Personal profiles** - customizable user settings
- ✅ **Individual progress tracking** - no data mixing between users

### 📊 **Advanced Analytics**
- ✅ **Productivity score** - AI-driven performance metrics (0-100)
- ✅ **Learning streaks** - track daily consistency
- ✅ **Interactive charts** - visualize your learning patterns
- ✅ **Activity heatmaps** - identify your most productive hours
- ✅ **Platform distribution** - see where you learn most
- ✅ **Weekly comparisons** - track week-over-week progress
- ✅ **Personalized insights** - get AI-driven recommendations

### 📄 **Professional Reports**
- ✅ **PDF generation** - comprehensive learning summaries
- ✅ **Detailed statistics** - videos, quizzes, playlists
- ✅ **Beautiful formatting** - professional purple gradient theme
- ✅ **Download & share** - export your achievements

### 🎨 **Beautiful Dashboard**
- ✅ **Modern UI** - stunning purple gradient design
- ✅ **Responsive layout** - works on all screen sizes
- ✅ **Intuitive navigation** - easy-to-use interface
- ✅ **Real-time updates** - live progress tracking
- ✅ **Dark theme** - easy on the eyes

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Chrome browser
- Internet connection

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/smart-elearning-automater.git
cd smart-elearning-automater
```

2. **Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Run the dashboard**
```bash
streamlit run dashboard_v2.py
```

4. **Open your browser**
- Navigate to `http://localhost:8501`
- Create an account
- Start automating! 🎉

---

## 📖 How It Works

### 1. **Login/Register**
Create your account with a username and password (securely hashed)

### 2. **Configure Settings**
- Set your preferred playback speed
- Enable/disable quiz automation
- Customize preferences

### 3. **Start Automation**
- Paste a YouTube playlist URL
- Set playback speed (1x - 2x)
- Click "Start Automation"

### 4. **Track Progress**
- Real-time dashboard updates
- View completed videos
- Monitor playlist progress
- Check quiz statistics

### 5. **Analyze Performance**
- View productivity score
- Track learning streaks
- See activity charts
- Get personalized insights

### 6. **Generate Reports**
- Download PDF summaries
- Share your achievements
- Track long-term progress

---

## 🏗️ Architecture

```
smart-elearning-automater/
├── backend/
│   ├── dashboard_v2.py         # Main Streamlit dashboard
│   ├── video_automator.py      # Selenium automation engine
│   ├── database.py             # SQLite database operations
│   ├── auth.py                 # User authentication
│   ├── analytics.py            # Advanced analytics engine
│   ├── report_generator.py     # PDF report creation
│   ├── config.py               # Configuration settings
│   └── requirements.txt        # Python dependencies
├── data/
│   ├── users.db                # User accounts
│   ├── learning_progress_user_*.db  # Per-user databases
│   └── reports/                # Generated PDF reports
└── README.md
```

---

## 🎯 Key Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Core language | 3.8+ |
| **Streamlit** | Web dashboard | 1.50.0 |
| **Selenium** | Browser automation | 4.38.0 |
| **SQLite3** | Database | Built-in |
| **Plotly** | Interactive charts | Latest |
| **ReportLab** | PDF generation | Latest |
| **ChromeDriver** | Browser control | Auto-updated |

---

## 📊 Features in Detail

### **Automation Engine**
- **Smart Playback**: Automatically plays videos at your preferred speed
- **Ad Detection**: Identifies and skips advertisements instantly
- **Error Recovery**: Handles network issues and retries automatically
- **Multi-format Support**: Works with playlists, single videos, live streams

### **Analytics Dashboard**
- **Productivity Score**: 0-100 score based on videos, quizzes, streaks, activity
- **Learning Streaks**: Current & longest streak tracking with date analysis
- **Platform Charts**: Pie chart showing YouTube, Coursera, Udemy distribution
- **Time Heatmaps**: Bar chart of activity by hour (0-23)
- **Trend Analysis**: 30-day line chart of learning activity
- **Weekly Insights**: This week vs last week comparison

### **Multi-User System**
- **Isolated Databases**: Each user gets their own database file
- **Secure Auth**: Passwords hashed with SHA-256
- **Device Tracking**: Unique Chrome profiles per user per device
- **Session Management**: Persistent login sessions
- **Profile Settings**: Per-user preferences and customization

### **PDF Reports**
- **Summary Statistics**: Total videos, playlists, quizzes, accuracy
- **Video Tables**: Last 15 completed videos with dates
- **Playlist Progress**: All tracked playlists with video counts
- **Quiz Performance**: Accuracy, attempts, confidence scores
- **Activity Logs**: Recent 10 actions with timestamps
- **Professional Layout**: Purple gradient theme, tables, headers

---

## 🐛 Bug Fixes & Updates

### **Version 2.2 - Latest**
✅ **Fixed**: Manual pause not working  
✅ **Fixed**: Playback speed not persisting across videos  
✅ **Fixed**: Progress not updating in real-time  
✅ **Fixed**: Multi-user data isolation issues  
✅ **Fixed**: Browser opening on wrong device  
✅ **Added**: Advanced analytics with charts  
✅ **Added**: PDF report generation  
✅ **Added**: Productivity scoring system  

### **Version 2.1**
✅ **Fixed**: User-specific database isolation  
✅ **Fixed**: Device-specific automation  
✅ **Added**: Enhanced dashboard UI  

### **Version 2.0**
✅ **Fixed**: Browser closing after 3 videos  
✅ **Fixed**: Progress not saving for playlists  
✅ **Fixed**: Autoplay timeout issues  
✅ **Added**: User authentication  

---

## 📝 Use Cases

### **For Students**
- 📚 Complete online courses faster (2x speed)
- 📊 Track your learning progress
- 🏆 Maintain learning streaks
- 📄 Generate progress reports for accountability

### **For Professionals**
- 🎓 Upskill efficiently with automated playback
- ⏰ Save time with ad-skipping
- 📈 Monitor productivity metrics
- 💼 Generate certificates of completion

### **For Educators**
- 👨‍🏫 Review course materials quickly
- 📊 Track student progress (with their permission)
- 📝 Analyze learning patterns
- 🎯 Identify areas for improvement

---

## 🔒 Security & Privacy

- ✅ **Password Hashing**: SHA-256 encryption for all passwords
- ✅ **Data Isolation**: Each user's data stored in separate database
- ✅ **Local Storage**: All data stored locally on your machine
- ✅ **No Data Collection**: We don't collect or transmit your data
- ✅ **Secure Sessions**: Session-based authentication

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Streamlit** - For the amazing dashboard framework
- **Selenium** - For powerful browser automation
- **Plotly** - For beautiful interactive charts
- **ReportLab** - For PDF generation capabilities

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/smart-elearning-automater/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/smart-elearning-automater/discussions)
- **Email**: your.email@example.com

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐ on GitHub!

---

## 📸 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Analytics
![Analytics](screenshots/analytics.png)

### PDF Report
![Report](screenshots/report.png)

---

## 🎉 What Makes This Special?

1. **Complete Automation** - Set it and forget it
2. **Multi-User** - Perfect for families or study groups
3. **Advanced Analytics** - More than just a video player
4. **Professional Reports** - Share your achievements
5. **Active Development** - Regular updates and bug fixes
6. **Open Source** - Free to use and modify
7. **Well Documented** - Comprehensive guides and comments
8. **Modern Tech Stack** - Built with latest technologies

---

**Made with ❤️ by [Your Name]**

*Happy Learning! 🚀*
