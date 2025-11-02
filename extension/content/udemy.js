// Udemy Content Script - Runs on Udemy pages

let isAutomationRunning = false;
let settings = {};
let lecturesWatchedCount = 0;
let currentLectureData = {};
let videoEndHandlerAttached = false;
let userPausedVideo = false; // Track if user manually paused
let lastPlayTime = 0; // Track when video was last playing

console.log('🎓 Smart E-Learning Automator loaded on Udemy');
console.log('Current URL:', window.location.href);

// Safe message sending with error handling
function safeSendMessage(message, callback) {
  try {
    chrome.runtime.sendMessage(message, (response) => {
      if (chrome.runtime.lastError) {
        // Extension context invalidated - ignore silently
        console.log('Extension reloaded, message not sent');
        return;
      }
      if (callback) callback(response);
    });
  } catch (error) {
    console.log('Could not send message:', error.message);
  }
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Udemy content script received message:', request.action);
  
  if (request.action === 'start') {
    settings = request.settings;
    console.log('Starting Udemy automation with settings:', settings);
    startAutomation();
    sendResponse({ success: true });
  }
  
  if (request.action === 'stop') {
    stopAutomation();
    sendResponse({ success: true });
  }
  
  if (request.action === 'setSpeed') {
    setPlaybackSpeed(request.speed);
    sendResponse({ success: true });
  }
  
  if (request.action === 'getCurrentTimestamp') {
    const video = document.querySelector('video');
    if (video) {
      const timestamp = Math.floor(video.currentTime);
      const videoTitle = document.querySelector('[data-purpose="lecture-title"]')?.textContent?.trim() ||
                        document.querySelector('h1')?.textContent?.trim() ||
                        document.title.replace(' | Udemy', '');
      
      sendResponse({ 
        success: true, 
        timestamp: timestamp,
        formattedTime: formatTime(timestamp),
        videoTitle: videoTitle,
        videoUrl: window.location.href,
        platform: 'udemy'
      });
    } else {
      sendResponse({ success: false, error: 'No video found' });
    }
  }
  
  if (request.action === 'jumpToTimestamp') {
    const video = document.querySelector('video');
    if (video && request.timestamp !== undefined) {
      video.currentTime = request.timestamp;
      sendResponse({ success: true });
    } else {
      sendResponse({ success: false, error: 'Cannot jump to timestamp' });
    }
  }
  
  return true;
});

// Check if already running on page load
chrome.storage.sync.get(['isRunning'], (data) => {
  if (data.isRunning) {
    chrome.storage.sync.get(null, (allSettings) => {
      settings = allSettings;
      startAutomation();
    });
  }
});

// Start automation
function startAutomation() {
  isAutomationRunning = true;
  console.log('▶️ Udemy automation started');
  
  safeSendMessage({
    action: 'logActivity',
    data: {
      type: 'automation_start',
      message: 'Automation started on Udemy',
      url: window.location.href
    }
  });
  
  // Apply settings
  setPlaybackSpeed(settings.playbackSpeed);
  
  // Start monitoring
  monitorVideo();
  
  if (settings.autoNext) {
    setupAutoNext();
  }
  
  // Auto-dismiss popups
  dismissPopups();
}

// Stop automation
function stopAutomation() {
  isAutomationRunning = false;
  console.log('⏹️ Udemy automation stopped');
  
  safeSendMessage({
    action: 'logActivity',
    data: {
      type: 'automation_stop',
      message: 'Automation stopped',
      url: window.location.href
    }
  });
}

// Set playback speed
function setPlaybackSpeed(speed) {
  const video = document.querySelector('video');
  if (video) {
    video.playbackRate = speed;
    console.log(`⚡ Speed set to ${speed}x on video element`);
    
    // Also ensure video is playing
    if (video.paused) {
      video.play().then(() => {
        console.log('▶️ Video started playing');
      }).catch(err => {
        console.log('Could not autoplay:', err.message);
      });
    }
  } else {
    console.log('⚠️ Video element not found');
  }
}

// Monitor video progress
function monitorVideo() {
  const video = document.querySelector('video');
  if (!video) {
    console.log('⏳ Waiting for video element...');
    setTimeout(monitorVideo, 1000);
    return;
  }
  
  console.log('✅ Video element found, starting monitoring');
  
  // Get lecture title
  const titleElement = document.querySelector('[data-purpose="lecture-title"]') || 
                       document.querySelector('.ud-heading-xl') ||
                       document.querySelector('h1');
  const title = titleElement ? titleElement.textContent.trim() : 'Unknown Lecture';
  
  console.log('📺 Current lecture:', title);
  
  currentLectureData = {
    title: title,
    url: window.location.href,
    platform: 'udemy',
    speed: settings.playbackSpeed || 1.0,
    startTime: Date.now()
  };
  
  // Apply speed immediately
  setPlaybackSpeed(settings.playbackSpeed);
  
  // Ensure video plays
  if (video.paused) {
    video.play().catch(err => console.log('Play error:', err.message));
  }
  
  // Track user pause/play actions
  video.addEventListener('pause', () => {
    if (!video.ended && video.currentTime > 0) {
      // User manually paused
      userPausedVideo = true;
      console.log('⏸️ User paused video - automation will not auto-resume');
    }
  });
  
  video.addEventListener('play', () => {
    // User resumed, reset flag
    userPausedVideo = false;
    lastPlayTime = Date.now();
    console.log('▶️ Video playing');
  });
  
  video.addEventListener('playing', () => {
    lastPlayTime = Date.now();
  });
  
  // Update progress periodically
  const progressInterval = setInterval(() => {
    if (!isAutomationRunning) {
      clearInterval(progressInterval);
      return;
    }
    
    if (video.duration) {
      const progress = (video.currentTime / video.duration) * 100;
      
      safeSendMessage({
        action: 'updateProgress',
        title: title,
        progress: Math.round(progress),
        currentTime: formatTime(video.currentTime),
        duration: formatTime(video.duration)
      });
    }
  }, 1000);
  
  // Remove old listener if exists
  if (videoEndHandlerAttached) {
    video.removeEventListener('ended', handleVideoEnd);
  }
  
  // Listen for video end
  video.addEventListener('ended', handleVideoEnd, { once: true });
  videoEndHandlerAttached = true;
  
  // Apply speed when video loads/plays
  video.addEventListener('loadedmetadata', () => {
    console.log('📊 Video metadata loaded');
    setPlaybackSpeed(settings.playbackSpeed);
  });
  
  video.addEventListener('play', () => {
    console.log('▶️ Video playing event');
    setPlaybackSpeed(settings.playbackSpeed);
  });
  
  // Reapply speed every 3 seconds (Udemy sometimes resets it)
  const speedInterval = setInterval(() => {
    if (!isAutomationRunning) {
      clearInterval(speedInterval);
      return;
    }
    const currentVideo = document.querySelector('video');
    if (currentVideo && Math.abs(currentVideo.playbackRate - settings.playbackSpeed) > 0.01) {
      currentVideo.playbackRate = settings.playbackSpeed;
      console.log('🔄 Speed re-applied:', settings.playbackSpeed);
    }
  }, 3000);
}

// Handle video completion
function handleVideoEnd() {
  if (!isAutomationRunning) return;
  
  const video = document.querySelector('video');
  currentLectureData.duration = video ? video.duration : 0;
  
  lecturesWatchedCount++;
  
  // Send video completion with request for summary
  safeSendMessage({
    action: 'videoCompleted',
    data: {
      ...currentLectureData,
      requestSummary: true  // Request AI summary generation
    }
  });
  
  console.log(`✅ Lecture ${lecturesWatchedCount} completed: ${currentLectureData.title}`)
  console.log(`📝 Requesting AI summary generation...`);
  
  videoEndHandlerAttached = false;
  
  // Check video limit
  if (settings.videoLimit > 0 && lecturesWatchedCount >= settings.videoLimit) {
    console.log('🛑 Lecture limit reached');
    stopAutomation();
    alert('Lecture limit reached! Automation stopped.');
    return;
  }
  
  // Let Udemy's autoplay handle it - don't manually click next
  // This prevents skipping videos
  console.log('⏭️ Waiting for Udemy autoplay to load next lecture...');
}

// Play next lecture (for manual skip or quiz handling)
function playNextLecture() {
  console.log('🔍 Looking for next lecture button...');
  
  // Check if current page is a quiz
  const isQuiz = window.location.href.includes('/quiz/') || 
                 document.querySelector('[data-purpose="quiz-container"]') ||
                 document.querySelector('.quiz-view-page');
  
  if (isQuiz) {
    console.log('📝 Quiz detected - skipping to next lecture');
    skipQuiz();
    return;
  }
  
  // Try multiple selectors for next button
  const nextSelectors = [
    '[data-purpose="go-to-next"]',
    'button[data-purpose="go-to-next"]',
    '.next-btn',
    'button[aria-label="Next"]',
    '.ud-btn[data-purpose="go-to-next"]',
    'button.ud-btn.ud-btn-large.ud-btn-primary.ud-heading-md'
  ];
  
  for (const selector of nextSelectors) {
    const nextButton = document.querySelector(selector);
    if (nextButton && !nextButton.disabled) {
      console.log(`✅ Found next button with selector: ${selector}`);
      nextButton.click();
      console.log('⏭️ Clicked next lecture button');
      
      // Re-monitor new video after navigation
      setTimeout(() => {
        console.log('🔄 Re-initializing video monitoring...');
        monitorVideo();
      }, 2000);
      return;
    }
  }
  
  console.log('❌ No next lecture button found - checking alternative methods');
  
  // Alternative: Try to find and click next item in sidebar
  const nextItem = document.querySelector('.curriculum-item-link.active + .curriculum-item-link');
  if (nextItem) {
    console.log('✅ Found next item in sidebar');
    nextItem.click();
    setTimeout(monitorVideo, 2000);
    return;
  }
  
  console.log('📝 No next lecture found - course may be complete');
  stopAutomation();
}

// Skip quiz and move to next lecture
function skipQuiz() {
  console.log('🔍 Attempting to skip quiz...');
  
  // Look for skip/next button on quiz page
  const skipSelectors = [
    'button[data-purpose="skip-question"]',
    'button[data-purpose="next-item"]',
    '[data-purpose="go-to-next"]',
    'button:contains("Skip")',
    '.next-btn',
    'button[aria-label="Next"]'
  ];
  
  for (const selector of skipSelectors) {
    const skipButton = document.querySelector(selector);
    if (skipButton && !skipButton.disabled) {
      console.log(`✅ Found skip button: ${selector}`);
      skipButton.click();
      console.log('⏭️ Skipped quiz');
      setTimeout(() => {
        // Check if still on quiz, try next item in curriculum
        if (window.location.href.includes('/quiz/')) {
          const nextItem = document.querySelector('.curriculum-item-link.active + .curriculum-item-link');
          if (nextItem) {
            nextItem.click();
            console.log('📚 Moved to next item via curriculum');
          }
        }
        monitorVideo();
      }, 2000);
      return;
    }
  }
  
  // If no skip button, try to go to next item in curriculum
  console.log('ℹ️ No skip button found, using curriculum navigation...');
  const nextItem = document.querySelector('.curriculum-item-link.active + .curriculum-item-link');
  if (nextItem) {
    nextItem.click();
    console.log('📚 Moved to next item via curriculum');
    setTimeout(monitorVideo, 2000);
  } else {
    console.log('❌ Cannot skip quiz - please complete manually');
    stopAutomation();
  }
}

// Setup auto-next
function setupAutoNext() {
  // Enable autoplay if available
  const autoplayToggle = document.querySelector('[data-purpose="autoplay-toggle"]');
  if (autoplayToggle && autoplayToggle.getAttribute('aria-checked') === 'false') {
    autoplayToggle.click();
    console.log('✅ Autoplay enabled');
  }
  
  // Monitor and auto-click play button ONLY if not user-paused
  setInterval(() => {
    if (!isAutomationRunning) return;
    
    // Don't auto-resume if user manually paused
    if (userPausedVideo) {
      return;
    }
    
    const video = document.querySelector('video');
    if (video && video.paused && !video.ended) {
      // Only auto-play if video has been paused for more than 3 seconds
      // This prevents interfering with user controls
      const timeSinceLastPlay = Date.now() - lastPlayTime;
      if (timeSinceLastPlay > 3000) {
        // Check if there's a play button overlay
        const playButton = document.querySelector('[data-purpose="play-button"]') ||
                          document.querySelector('.vjs-big-play-button') ||
                          document.querySelector('button[aria-label*="Play"]');
        
        if (playButton && playButton.offsetParent !== null) {
          playButton.click();
          console.log('▶️ Auto-clicked play button (after 3s pause)');
          userPausedVideo = false;
        }
      }
    }
  }, 4000); // Check every 4 seconds instead of 2
}

// Dismiss annoying popups
function dismissPopups() {
  setInterval(() => {
    if (!isAutomationRunning) return;
    
    // Close review/rating popups
    const closeButtons = document.querySelectorAll('[data-purpose="modal-close"], .ud-modal-close');
    closeButtons.forEach(btn => {
      if (btn.offsetParent !== null) {
        btn.click();
        console.log('❌ Closed popup');
      }
    });
    
    // Dismiss "Take notes" prompts
    const dismissButtons = document.querySelectorAll('[data-purpose="dismiss-button"]');
    dismissButtons.forEach(btn => {
      if (btn.offsetParent !== null) {
        btn.click();
      }
    });
  }, 3000);
}

// Format time helper
function formatTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  
  if (h > 0) {
    return `${h}:${pad(m)}:${pad(s)}`;
  }
  return `${m}:${pad(s)}`;
}

function pad(num) {
  return num.toString().padStart(2, '0');
}

// Handle page navigation
let lastUrl = location.href;
new MutationObserver(() => {
  const url = location.href;
  if (url !== lastUrl) {
    lastUrl = url;
    console.log('🔄 URL changed:', url);
    
    if (!isAutomationRunning) return;
    
    // Reset user pause flag on new page
    userPausedVideo = false;
    
    if (url.includes('/learn/lecture/')) {
      console.log('📺 New lecture detected');
      setTimeout(monitorVideo, 1500);
    } else if (url.includes('/quiz/')) {
      console.log('📝 Quiz page detected - attempting to skip');
      setTimeout(() => {
        skipQuiz();
      }, 1500);
    }
  }
}).observe(document, { subtree: true, childList: true });
