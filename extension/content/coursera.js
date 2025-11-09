// Coursera Content Script - Runs on Coursera pages

let isAutomationRunning = false;
let settings = {};
let videosWatchedCount = 0;
let currentVideoData = {};
let videoEndHandlerAttached = false;
let userPausedVideo = false;  // Track if user manually paused
let lastPlayTime = 0;          // Track when video was last playing

console.log('🎓 Smart E-Learning Automator loaded on Coursera');
console.log('Current URL:', window.location.href);

// Safe message sending with error handling
function safeSendMessage(message, callback) {
  try {
    chrome.runtime.sendMessage(message, (response) => {
      if (chrome.runtime.lastError) {
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
  console.log('Coursera content script received message:', request.action);
  
  if (request.action === 'start') {
    settings = request.settings;
    console.log('Starting Coursera automation with settings:', settings);
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
  console.log('▶️ Coursera automation started');
  
  safeSendMessage({
    action: 'logActivity',
    data: {
      type: 'automation_start',
      message: 'Automation started on Coursera',
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
}

// Stop automation
function stopAutomation() {
  isAutomationRunning = false;
  console.log('⏹️ Coursera automation stopped');
  
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
    console.log(`⚡ Speed set to ${speed}x`);
  }
}

// Monitor video progress
function monitorVideo() {
  const video = document.querySelector('video');
  if (!video) {
    setTimeout(monitorVideo, 1000);
    return;
  }
  
  // Get video title
  const titleElement = document.querySelector('h1') || 
                       document.querySelector('.video-name') ||
                       document.querySelector('[data-e2e="item-title"]');
  const title = titleElement ? titleElement.textContent.trim() : 'Unknown Video';
  
  currentVideoData = {
    title: title,
    url: window.location.href,
    platform: 'coursera',
    speed: settings.playbackSpeed || 1.0,
    startTime: Date.now()
  };
  
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
  
  // Track user pause/play actions
  video.addEventListener('pause', () => {
    if (!video.ended && video.currentTime > 0 && video.currentTime < video.duration - 1) {
      userPausedVideo = true;
      console.log('⏸️ User paused video - automation will not auto-resume');
    }
  });
  
  video.addEventListener('play', () => {
    userPausedVideo = false;
    lastPlayTime = Date.now();
  });
  
  video.addEventListener('playing', () => {
    lastPlayTime = Date.now();
  });
  
  // Apply speed when video loads
  video.addEventListener('loadedmetadata', () => {
    setPlaybackSpeed(settings.playbackSpeed);
  });
}

// Handle video completion
function handleVideoEnd() {
  if (!isAutomationRunning) return;
  
  const video = document.querySelector('video');
  currentVideoData.duration = video ? video.duration : 0;
  
  videosWatchedCount++;
  
  safeSendMessage({
    action: 'videoCompleted',
    data: currentVideoData
  });
  
  console.log(`✅ Video ${videosWatchedCount} completed: ${currentVideoData.title}`);
  
  videoEndHandlerAttached = false;
  
  // Check video limit
  if (settings.videoLimit > 0 && videosWatchedCount >= settings.videoLimit) {
    console.log('🛑 Video limit reached');
    stopAutomation();
    alert('Video limit reached! Automation stopped.');
    return;
  }
  
  // Let Coursera's autoplay handle progression instead of manual click
  // This prevents double-advance bug (video skipping)
  if (settings.autoNext) {
    console.log('⏭️ Waiting for Coursera autoplay to load next item...');
  }
}

// Play next item (only called manually, not after video end)
function playNextItem() {
  // Check if current page is a quiz
  const isQuiz = window.location.href.includes('/quiz') || 
                 document.querySelector('[data-e2e="quiz-container"]') ||
                 document.querySelector('.rc-Quiz');
  
  if (isQuiz) {
    console.log('📝 Quiz detected - attempting to skip');
    skipQuiz();
    return;
  }
  
  // Try multiple selectors for next button
  const nextSelectors = [
    'button[data-e2e="next-button"]',
    '.rc-NavigationControls button[aria-label*="next"]',
    'button.next-button',
    'button[aria-label="Next Item"]'
  ];
  
  for (const selector of nextSelectors) {
    const nextButton = document.querySelector(selector);
    if (nextButton && !nextButton.disabled) {
      nextButton.click();
      console.log('⏭️ Moving to next item');
      
      // Re-monitor new video
      setTimeout(monitorVideo, 2000);
      return;
    }
  }
  
  console.log('📝 No next item found - module may be complete');
  stopAutomation();
}

// Skip quiz pages
function skipQuiz() {
  console.log('🔍 Attempting to skip quiz...');
  
  // Try to find skip button
  const skipSelectors = [
    'button[data-e2e="skip-quiz"]',
    'button:contains("Skip")',
    'a:contains("Skip Quiz")',
    'button[aria-label*="skip"]',
    '.skip-button',
    'button[data-e2e="next-button"]'
  ];
  
  for (const selector of skipSelectors) {
    const skipButton = document.querySelector(selector);
    if (skipButton) {
      console.log(`✅ Found skip button: ${selector}`);
      skipButton.click();
      setTimeout(monitorVideo, 2000);
      return;
    }
  }
  
  // Try to navigate via sidebar/item list
  const currentItem = document.querySelector('.rc-ItemListItem.active, .rc-ItemListItem[aria-current="true"]');
  if (currentItem) {
    const nextItem = currentItem.nextElementSibling;
    if (nextItem) {
      const link = nextItem.querySelector('a');
      if (link) {
        console.log('📚 Moving to next item via course navigation');
        link.click();
        setTimeout(monitorVideo, 2000);
        return;
      }
    }
  }
  
  console.log('⚠️ Could not find way to skip quiz');
  stopAutomation();
}

// Setup auto-next
function setupAutoNext() {
  console.log('✅ Auto-next enabled for Coursera');
  
  // Auto-resume paused videos (but respect user pause)
  setInterval(() => {
    if (!isAutomationRunning) return;
    
    const video = document.querySelector('video');
    if (!video) return;
    
    // Don't auto-resume if user manually paused
    if (userPausedVideo) {
      return;
    }
    
    // Only auto-play if video is paused and not ended
    // And it's been more than 3 seconds since last play (to avoid interfering with buffering)
    if (video.paused && !video.ended && video.currentTime > 0) {
      const timeSinceLastPlay = Date.now() - lastPlayTime;
      if (timeSinceLastPlay > 3000) {
        const playButton = document.querySelector('button[aria-label="Play"]') ||
                          document.querySelector('.vjs-play-control');
        if (playButton) {
          playButton.click();
          console.log('▶️ Auto-clicked play button (after 3s pause)');
        }
      }
    }
  }, 4000); // Check every 4 seconds
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
    
    if (url.includes('/lecture/') || url.includes('/item/')) {
      console.log('📺 New video detected');
      setTimeout(monitorVideo, 1500);
    } else if (url.includes('/quiz')) {
      console.log('📝 Quiz page detected - attempting to skip');
      setTimeout(() => {
        skipQuiz();
      }, 1500);
    }
  }
}).observe(document, { subtree: true, childList: true });
