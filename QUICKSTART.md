# 🚀 Quick Start Guide

## Installation & First Run

### Step 1: Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**Note**: First installation will take 5-10 minutes due to ML model downloads.

### Step 2: Test with YouTube (No Login Required)

```bash
python main.py --platform youtube --url "https://www.youtube.com/watch?v=VIDEO_ID&list=PLAYLIST_ID" --limit 2
```

This will:
- Open Chrome browser
- Play 2 videos from the playlist
- Track progress in database

### Step 3: Launch Dashboard (Recommended)

```bash
streamlit run dashboard.py
```

Then open `http://localhost:8501` in your browser.

## 📖 Example Commands

### YouTube Playlist (No login needed)
```bash
python main.py --platform youtube --url "https://www.youtube.com/playlist?list=PLWKjhJtqVAbnqBxcdjVGgT3uVR10bzTEB"
```

### Coursera Course (Requires login)
```bash
python main.py --platform coursera --url "https://www.coursera.org/learn/python" --username "your@email.com" --password "yourpass"
```

### Udemy Course (Requires login)
```bash
python main.py --platform udemy --url "https://www.udemy.com/course/your-course/" --username "your@email.com" --password "yourpass" --limit 5
```

### Watch without solving quizzes
```bash
python main.py --platform coursera --url "YOUR_URL" --username "email" --password "pass" --no-quiz
```

## 🎯 What to Expect

### First Run:
1. **ML Model Download**: ~250MB model downloads (one-time)
2. **Browser Opens**: Chrome window opens automatically
3. **Login**: If credentials provided, logs in automatically
4. **Automation Starts**: Videos play automatically
5. **Progress Tracking**: Check `data/learning_progress.db`

### Dashboard View:
- **Metrics**: Videos completed, quiz accuracy
- **Live Logs**: Real-time activity feed
- **Quiz Stats**: Performance trends
- **Control Panel**: Start/stop automation

## 🐛 Common Issues

### Issue: "Import X could not be resolved"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: ChromeDriver not found
**Solution**: webdriver-manager handles this automatically on first run

### Issue: Platform selectors not working
**Solution**: Platform HTML changes. Update `config.py` selectors

### Issue: Quiz not detected
**Solution**: Some platforms have dynamic quizzes. Check logs for details.

## 📊 Check Your Progress

### View Database
```bash
# Open SQLite database
sqlite3 data/learning_progress.db

# Query completed videos
SELECT * FROM videos WHERE completed = 1;

# Query quiz stats
SELECT * FROM quizzes;
```

### View Logs
```bash
# Check automation logs
cat data/automation.log
```

## ⚡ Pro Tips

1. **Start small**: Use `--limit 2` for testing
2. **Use dashboard**: Better visibility than CLI
3. **Check logs**: Monitor `automation.log` for issues
4. **Cache works**: Repeated quizzes use cached answers
5. **Headless mode**: Edit `video_automator.py` to set `headless=True`

## 🎓 Next Steps

1. ✅ Test with YouTube playlist (no login)
2. ✅ Try dashboard interface
3. ✅ Test quiz solving on Coursera/Udemy
4. ✅ Check database to see saved progress
5. ✅ Customize platform selectors in `config.py`

## ⚠️ Important Notes

- **Terms of Service**: May violate platform ToS
- **Use Responsibly**: For personal learning only
- **No Guarantee**: Platforms change frequently
- **Quiz Accuracy**: ~70-90% depending on question type

---

Need help? Check the full README.md for detailed documentation.
