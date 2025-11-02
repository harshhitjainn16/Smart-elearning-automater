# Supported Platforms Guide

The Smart E-Learning Automator extension now supports **5+ major learning platforms**! This guide shows what features work on each platform.

## 🌐 Platform Support Matrix

| Platform | Speed Control | Auto-Next | Ad Skip | Progress Tracking | Status |
|----------|--------------|-----------|---------|-------------------|--------|
| **YouTube** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | 🟢 Fully Working |
| **Udemy** | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes | 🟢 Fully Working |
| **Coursera** | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes | 🟢 Fully Working |
| **LinkedIn Learning** | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes | 🟡 Beta |
| **Skillshare** | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes | 🟡 Beta |

---

## 📺 YouTube
**URL Pattern**: `youtube.com/watch`

### Features:
- ✅ Playback speed control (0.5x - 2.0x)
- ✅ Auto-skip ads (when skip button available)
- ✅ Auto-play next video in playlist
- ✅ Close overlay ads automatically
- ✅ Real-time progress tracking
- ✅ Statistics tracking

### How to Use:
1. Open any YouTube video or playlist
2. Click the extension icon
3. Set your preferred speed
4. Enable "Auto Skip Ads" and "Auto Next Video"
5. Click "Start Automation"

### Tips:
- Works best with YouTube playlists
- Autoplay must be enabled in YouTube settings
- Ad skip works for skippable ads only (non-skippable ads play in full)

---

## 🎓 Udemy
**URL Pattern**: `udemy.com/course/*/learn/lecture/*`

### Features:
- ✅ Playback speed control
- ✅ Auto-advance to next lecture
- ✅ Auto-dismiss rating popups
- ✅ Progress tracking
- ✅ Course completion tracking

### How to Use:
1. Enroll in a Udemy course
2. Open any lecture
3. Click extension icon → Start Automation
4. Lectures will auto-advance when complete

### Tips:
- Automatically closes "Rate this course" popups
- Respects video limit setting
- Marks lectures as complete automatically

---

## 🏫 Coursera
**URL Pattern**: `coursera.org/learn/*/lecture/*`

### Features:
- ✅ Playback speed control
- ✅ Auto-advance to next item
- ✅ Progress tracking
- ✅ Works with video lectures

### How to Use:
1. Enroll in a Coursera course
2. Open any video lecture
3. Start automation via extension
4. Videos will auto-advance

### Tips:
- Works with video lectures (not quizzes)
- Module navigation supported
- Speed settings persist across videos

---

## 💼 LinkedIn Learning
**URL Pattern**: `linkedin.com/learning/*`

### Features:
- ✅ Playback speed control
- ✅ Auto-next video
- ✅ Progress tracking
- ✅ Course completion tracking

### How to Use:
1. Start any LinkedIn Learning course
2. Open first video
3. Enable automation
4. Sit back and learn!

### Tips:
- Beta feature - may need selector updates
- Works with most courses
- Report any issues on GitHub

---

## 🎨 Skillshare
**URL Pattern**: `skillshare.com/classes/*`

### Features:
- ✅ Playback speed control
- ✅ Auto-next lesson
- ✅ Progress tracking
- ✅ Class completion

### How to Use:
1. Enroll in a Skillshare class
2. Start first lesson
3. Enable automation
4. Lessons auto-advance

### Tips:
- Beta feature
- Works with video lessons
- May need updates for new Skillshare UI

---

## 🛠️ Platform-Specific Notes

### YouTube
- **Ads**: Extension skips ads automatically when "Skip Ad" button appears
- **Playlists**: Works seamlessly with any YouTube playlist
- **Live Streams**: Not supported (designed for recorded content)

### Udemy
- **Quizzes**: Extension pauses automation (manual completion required)
- **Resources**: Download prompts may pause automation
- **Coding Exercises**: Not automated (requires manual work)

### Coursera
- **Readings**: Extension only works with video lectures
- **Quizzes**: Manual completion required
- **Peer Reviews**: Not automated

### LinkedIn Learning
- **Chapter Markers**: Respected during playback
- **Transcripts**: Extension doesn't interfere
- **Exercise Files**: Manual download required

### Skillshare
- **Project Videos**: Automation works normally
- **Community**: Extension doesn't affect community features

---

## 🚀 Adding More Platforms

Want support for more platforms? Here's how you can help:

### Popular Requests:
- [ ] Khan Academy
- [ ] Pluralsight
- [ ] edX
- [ ] Codecademy
- [ ] Treehouse
- [ ] DataCamp

### How to Request:
1. Open an issue on GitHub
2. Provide the platform URL
3. Describe the video player type
4. Share any specific requirements

---

## 🔧 Troubleshooting

### Extension Not Working?

**YouTube:**
- ✅ Check if autoplay is enabled
- ✅ Try reloading the page
- ✅ Ensure you're on a video/playlist page

**Udemy:**
- ✅ Make sure you're enrolled in the course
- ✅ Check if popup blockers are disabled
- ✅ Reload extension if selectors changed

**Coursera:**
- ✅ Ensure you're on a video lecture (not reading/quiz)
- ✅ Check browser console for errors
- ✅ Try refreshing the page

**LinkedIn/Skillshare:**
- ✅ These are beta - report issues
- ✅ UI updates may break selectors
- ✅ Check console logs for clues

### General Tips:
1. **Reload Extension**: Go to `chrome://extensions/` → Click reload
2. **Check Console**: Press F12 → Console tab → Look for extension logs
3. **Clear Cache**: Sometimes helps with UI updates
4. **Update Extension**: Make sure you have the latest version

---

## 📊 Feature Comparison

### Speed Control
All platforms support 0.5x to 2.0x playback speed. The extension:
- Applies speed immediately on video load
- Maintains speed across video changes
- Overrides platform default speeds

### Auto-Next
Behavior varies by platform:
- **YouTube**: Uses native autoplay
- **Udemy**: Clicks "Next Lecture" button
- **Coursera**: Clicks "Next Item" button
- **LinkedIn**: Clicks "Next Video" button
- **Skillshare**: Clicks next lesson

### Progress Tracking
All platforms track:
- Current video title
- Time elapsed / Total duration
- Completion percentage
- Total videos watched
- Average playback speed

---

## 🎯 Best Practices

### For YouTube:
- Use with playlists for best results
- Enable autoplay in YouTube settings
- Create custom playlists for courses

### For Paid Platforms (Udemy, Coursera, etc.):
- Ensure active subscription
- Complete quizzes manually
- Download resources before automation
- Review important concepts manually

### General:
- Set realistic speed (1.25x-1.5x for learning)
- Use video limit to prevent burnout
- Take breaks every hour
- Review statistics regularly

---

## 🔐 Privacy & Security

### Data Storage:
- All data stored locally (Chrome Storage API)
- No data sent to external servers
- Statistics stay on your device
- Settings sync across Chrome instances (if Chrome sync enabled)

### Permissions:
- **storage**: Save settings locally
- **tabs**: Detect active platform
- **activeTab**: Control video playback
- **scripting**: Inject automation scripts

### Platform Terms of Service:
- ⚠️ Check each platform's ToS before use
- Some platforms prohibit automation
- Use responsibly and ethically
- Extension is for personal learning enhancement

---

## 📝 Changelog

### Version 1.0.0 (Current)
- ✅ YouTube full support with ad skipping
- ✅ Udemy full support
- ✅ Coursera full support
- ✅ LinkedIn Learning (beta)
- ✅ Skillshare (beta)
- ✅ Statistics tracking
- ✅ Progress monitoring
- ✅ Customizable speed control

### Coming Soon:
- 🔜 Pluralsight support
- 🔜 edX support
- 🔜 Khan Academy support
- 🔜 Advanced statistics dashboard
- 🔜 Export statistics to CSV

---

## 🤝 Contributing

Found a bug or want to add a platform? 

### Steps:
1. Fork the repository
2. Create content script for new platform
3. Update manifest.json with new domain
4. Test thoroughly
5. Submit pull request

### Content Script Template:
```javascript
// platform.js
let isAutomationRunning = false;
let settings = {};

// Implement: startAutomation(), stopAutomation()
// Implement: monitorVideo(), handleVideoEnd()
// Implement: setPlaybackSpeed(), playNextVideo()
```

---

## 📧 Support

- 🐛 **Bug Reports**: GitHub Issues
- 💡 **Feature Requests**: GitHub Discussions
- 📖 **Documentation**: README.md
- 🎥 **Video Tutorial**: Coming Soon

---

## ⚖️ License

MIT License - Use freely, modify as needed, share with others!

---

**Happy Learning! 🎓✨**
