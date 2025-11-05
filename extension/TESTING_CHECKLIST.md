# Quick Testing Checklist ✅

## Before Testing:
- [ ] Reload extension in `chrome://extensions/`
- [ ] Open browser console (F12)
- [ ] Clear console to see fresh logs

---

## YouTube Testing:
- [ ] Go to any playlist
- [ ] Start automation (1.5x speed)
- [ ] Verify: Video 1 → 2 → 3 (sequential, not skipping)
- [ ] Verify: Ads auto-skipped when skip button appears
- [ ] Verify: Can pause manually and video stays paused
- [ ] Verify: Console shows "Waiting for YouTube autoplay..."

**Expected Console Logs**:
```
🎓 Smart E-Learning Automator loaded on YouTube
▶️ YouTube automation started
✅ Video 1 completed: [title]
⏭️ Waiting for YouTube autoplay...
📺 New video detected
```

---

## Udemy Testing:
- [ ] Go to course with quizzes
- [ ] Start automation (1.5x speed)
- [ ] Verify: Lecture 1 → 2 → 3 (sequential)
- [ ] Verify: Quiz auto-skipped (if encountered)
- [ ] Verify: Can pause manually and stays paused
- [ ] Verify: Console shows "Waiting for Udemy autoplay..."

**Expected Console Logs**:
```
🎓 Smart E-Learning Automator loaded on Udemy
▶️ Udemy automation started
✅ Lecture 1 completed: [title]
⏭️ Waiting for Udemy autoplay...
📝 Quiz page detected - attempting to skip (if quiz)
```

---

## Coursera Testing:
- [ ] Go to any course module
- [ ] Start automation (1.5x speed)
- [ ] Verify: Items play sequentially
- [ ] Verify: Quiz auto-skipped (if encountered)
- [ ] Verify: Can pause manually
- [ ] Verify: Console shows "Waiting for Coursera autoplay..."

**Expected Console Logs**:
```
🎓 Smart E-Learning Automator loaded on Coursera
▶️ Coursera automation started
✅ Video completed: [title]
⏭️ Waiting for Coursera autoplay...
```

---

## LinkedIn Learning Testing:
- [ ] Go to any course
- [ ] Start automation (1.5x speed)
- [ ] Verify: Videos play sequentially
- [ ] Verify: Assessment auto-skipped (if encountered)
- [ ] Verify: Can pause manually
- [ ] Verify: Console shows "Waiting for LinkedIn Learning autoplay..."

**Expected Console Logs**:
```
🎓 Smart E-Learning Automator loaded on LinkedIn Learning
▶️ LinkedIn Learning automation started
✅ Video completed: [title]
⏭️ Waiting for LinkedIn Learning autoplay...
```

---

## Skillshare Testing:
- [ ] Go to any class
- [ ] Start automation (1.5x speed)
- [ ] Verify: Lessons play sequentially
- [ ] Verify: Project auto-skipped (if encountered)
- [ ] Verify: Can pause manually
- [ ] Verify: Console shows "Waiting for Skillshare autoplay..."

**Expected Console Logs**:
```
🎓 Smart E-Learning Automator loaded on Skillshare
▶️ Skillshare automation started
✅ Lesson completed: [title]
⏭️ Waiting for Skillshare autoplay...
```

---

## Universal Tests (All Platforms):

### Test 1: Sequential Playback ✅
- [ ] Videos/Lessons play 1 → 2 → 3 → 4 → 5
- [ ] NO skipping (not 1 → 3 → 5)
- [ ] Console shows "Waiting for [Platform] autoplay..."

### Test 2: Quiz/Assessment Skip ✅
- [ ] When quiz/assessment encountered
- [ ] Console shows "Quiz/Assessment detected"
- [ ] Extension auto-skips to next video
- [ ] OR console shows "Moving to next via navigation"

### Test 3: Manual Pause Control ✅
- [ ] Click pause during video
- [ ] Console shows "⏸️ User paused video - will not auto-resume"
- [ ] Video stays paused (no auto-resume)
- [ ] Click play manually
- [ ] Automation continues normally

### Test 4: Speed Control ✅
- [ ] Adjust speed slider (0.5x - 2.0x)
- [ ] Console shows "⚡ Speed set to [X]x"
- [ ] Video plays at selected speed
- [ ] Speed persists across videos

### Test 5: Stats Tracking ✅
- [ ] Videos watched count increases
- [ ] Time saved calculated correctly
- [ ] Stats persist after stopping/starting

---

## Common Issues & Solutions:

### Issue: Videos still skipping alternate ones
**Solution**: 
1. Check console for double "New video detected"
2. Reload extension
3. Disable platform's native autoplay and let extension enable it

### Issue: Quiz not auto-skipped
**Solution**:
1. Check console for "Quiz detected" message
2. If not detected, check URL and DOM
3. Report selectors needed for new quiz type
4. Try sidebar/curriculum navigation manually

### Issue: Can't pause
**Solution**:
1. Check console for "User paused video" message
2. Wait 1 full second after clicking pause
3. Should stay paused indefinitely
4. If still auto-resumes, check `userPausedVideo` flag in code

### Issue: Extension not loading
**Solution**:
1. Go to `chrome://extensions/`
2. Enable "Developer mode"
3. Check for errors in extension
4. Reload extension

---

## What to Report:

If you find bugs, please report:

1. **Platform**: Which platform (YouTube, Udemy, etc.)
2. **Bug Type**: Skipping, quiz, pause, speed, or other
3. **Console Logs**: Copy relevant logs from F12 console
4. **Steps to Reproduce**: 
   - What you did
   - What happened
   - What should have happened
5. **Course/Video URL**: (if possible)
6. **Browser**: Chrome version

---

## Success Criteria:

✅ **All platforms**:
- Videos play sequentially (1→2→3, not 1→3→5)
- Quizzes/assessments auto-skip
- Manual pause works (no auto-resume)
- Speed control works
- Stats track correctly

✅ **Console logs**:
- No errors
- Clear messages for each action
- "Waiting for autoplay" after video end
- "User paused" when manually paused

✅ **User experience**:
- Smooth automation
- Full manual control when needed
- No interference from extension

---

**If all tests pass → Extension is production-ready! 🚀**
**If any test fails → Report details for quick fix 🔧**
