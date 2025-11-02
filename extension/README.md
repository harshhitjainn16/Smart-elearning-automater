# 🎓 Smart E-Learning Automator - Chrome Extension

## ✨ What is This?

A **Chrome Extension** that automates video learning on YouTube (and soon Coursera/Udemy). It runs **locally in YOUR browser** - meaning:

✅ Browser automation happens **on YOUR device**  
✅ Works for any user who installs it  
✅ No central server needed  
✅ Complete privacy - data stays on your computer  

---

## 🚀 Quick Start

### Step 1: Install the Extension

1. **Download or clone** this repository
2. **Open Chrome** and go to: `chrome://extensions/`
3. **Enable "Developer mode"** (toggle in top-right)
4. **Click "Load unpacked"**
5. **Select the `extension` folder** from this project
6. **Done!** You'll see the extension icon in your toolbar

### Step 2: Use It!

1. **Go to YouTube** and open any playlist or video
2. **Click the extension icon** in your toolbar
3. **Set your preferences:**
   - Playback speed (0.5x - 2.0x)
   - Auto-skip ads
   - Auto-play next video
   - Video limit (optional)
4. **Click "Start Automation"**
5. **Sit back and watch!** The extension will:
   - Set your chosen playback speed
   - Skip ads automatically
   - Play next videos
   - Track your progress

---

## 🎯 Features

### Current (v1.0)
✅ **YouTube Support**
- Custom playback speed (0.5x - 2.0x)
- Auto-skip ads (all types)
- Auto-play next video
- Progress tracking
- Real-time statistics
- Video completion logging

✅ **Statistics Dashboard**
- Videos watched count
- Total watch time
- Average playback speed
- Time saved calculation
- Video history (last 100 videos)

✅ **Privacy-First**
- All data stored locally (Chrome Storage API)
- No external servers
- No data collection
- Works offline (once installed)

### Coming Soon
⏳ **Coursera Support**
⏳ **Udemy Support**
⏳ **Moodle Support**
⏳ **Quiz auto-solver**
⏳ **Export data to CSV/PDF**

---

## 📁 Project Structure

```
extension/
├── manifest.json           # Extension configuration
├── popup.html              # Extension popup UI
├── popup.js                # Popup logic
├── background.js           # Background service worker
├── content/
│   ├── youtube.js          # YouTube automation
│   ├── coursera.js         # Coursera (coming soon)
│   └── udemy.js            # Udemy (coming soon)
├── icons/
│   ├── icon16.png          # Extension icon (16x16)
│   ├── icon48.png          # Extension icon (48x48)
│   └── icon128.png         # Extension icon (128x128)
└── README.md               # This file
```

---

## 🔧 How It Works

### Architecture

```
User's Browser (Chrome)
├── Extension Popup (UI)
│   ├── Set speed, limits, preferences
│   └── Start/Stop automation
│
├── Content Scripts (Automation)
│   ├── Runs on YouTube pages
│   ├── Manipulates video player
│   ├── Clicks next video button
│   └── Skips ads
│
├── Background Worker (Data)
│   ├── Tracks statistics
│   ├── Stores video history
│   └── Manages settings
│
└── Chrome Storage API
    ├── User settings
    └── Statistics data
```

### Key Technologies

- **Manifest V3** - Latest Chrome extension standard
- **Content Scripts** - JavaScript injected into web pages
- **Service Workers** - Background processing
- **Chrome Storage API** - Local data persistence
- **Message Passing** - Communication between components

---

## 🎨 Customization

### Change Default Speed

Edit `background.js` line 7:
```javascript
playbackSpeed: 2.0,  // Change to your preferred default
```

### Change Video Limit

Edit `background.js` line 8:
```javascript
videoLimit: 10,  // Change default limit
```

### Add New Platform

1. Create new content script: `content/newplatform.js`
2. Add to `manifest.json`:
```json
{
  "matches": ["https://www.newplatform.com/*"],
  "js": ["content/newplatform.js"]
}
```
3. Implement automation logic similar to `youtube.js`

---

## 🐛 Troubleshooting

### Extension Not Loading
**Solution:** Make sure you selected the `extension` folder, not the parent folder

### Automation Not Starting
**Solution:** 
- Refresh the YouTube page after installing
- Make sure you're on a YouTube video page
- Check browser console for errors (F12)

### Speed Not Changing
**Solution:**
- Some videos restrict speed changes
- Try a different video
- Check if video has loaded fully

### Ads Not Being Skipped
**Solution:**
- YouTube's ad structure changes frequently
- Extension updates automatically handle this
- Some ads can't be skipped (non-skippable ads)

### Statistics Not Updating
**Solution:**
- Open popup to refresh stats
- Check Chrome Storage: `chrome://extensions/` → Extension details → Storage

---

## 🔒 Privacy & Security

### Data Storage
- ✅ All data stored **locally** in your browser
- ✅ Uses Chrome's built-in `storage.sync` API
- ✅ Syncs across your Chrome browsers (if signed in)
- ❌ **NO external servers**
- ❌ **NO data collection**
- ❌ **NO tracking**

### Permissions Explained

| Permission | Why Needed |
|-----------|------------|
| `storage` | Save settings and statistics |
| `tabs` | Detect active YouTube tabs |
| `activeTab` | Access current video page |
| `scripting` | Inject automation code |
| Host permissions | Run on YouTube/Coursera/Udemy |

---

## 📊 How to View Statistics

### Option 1: Popup
- Click extension icon
- See quick stats at bottom

### Option 2: Full Stats Page (Coming Soon)
- Click "View Statistics" button
- Opens full-page dashboard
- Detailed charts and graphs

---

## 🚀 Publishing to Chrome Web Store (Optional)

To make it available to everyone:

1. **Create icons** (16x16, 48x48, 128x128 PNG)
2. **Test thoroughly** on multiple videos/playlists
3. **Create developer account** ($5 one-time fee)
4. **Go to:** https://chrome.google.com/webstore/devconsole
5. **Upload extension** as ZIP
6. **Fill in details:**
   - Description
   - Screenshots
   - Privacy policy
7. **Submit for review** (takes 1-3 days)
8. **Get approved** and published!

---

## 📈 Roadmap

### Version 1.1 (Next Release)
- [ ] Full statistics page with charts
- [ ] Export data to CSV
- [ ] Keyboard shortcuts
- [ ] Dark/light theme toggle

### Version 1.2
- [ ] Coursera support
- [ ] Udemy support
- [ ] Playlist progress tracking

### Version 2.0
- [ ] Quiz auto-solver (AI-powered)
- [ ] Study schedule planner
- [ ] Integration with calendar
- [ ] Social sharing features

---

## 🤝 Contributing

Want to improve this extension?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Areas Needing Help
- Coursera automation implementation
- Udemy automation implementation
- UI/UX improvements
- Icon design
- Testing on different browsers

---

## 📝 License

MIT License - feel free to use, modify, and distribute!

---

## 🎓 For Students

This extension is perfect for:
- **Online course students** watching long lectures
- **Self-learners** on YouTube
- **Professional development** through MOOCs
- **Anyone** who wants to learn faster

### Pro Tips
- Use **1.5x-2.0x speed** for lectures you understand
- Use **1.0x speed** for complex topics
- Enable **auto-skip ads** to avoid distractions
- Check **statistics** to track your learning progress

---

## ⚠️ Disclaimer

This extension is for **educational purposes** only. Use responsibly and in accordance with platform terms of service. Automated playback should be used for content you have legitimate access to.

---

## 📞 Support

Having issues? 

1. Check the **Troubleshooting** section above
2. Open the browser console (F12) and check for errors
3. Create an issue on GitHub
4. Contact the developer

---

## 🌟 Acknowledgments

Built with ❤️ for learners everywhere who want to make the most of their time.

**Happy Learning!** 🎉

---

## 📸 Screenshots

*Add screenshots here after testing*

---

**Version:** 1.0.0  
**Last Updated:** October 30, 2025  
**Author:** Harshit  
**Status:** Active Development
