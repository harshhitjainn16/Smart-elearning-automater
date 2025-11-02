// YouTube Content Script - Runs on YouTube pages

let isAutomationRunning = false;
let settings = {};
let videosWatchedCount = 0;
let currentVideoData = {};
let videoEndHandlerAttached = false; // Track if event listener is attached

// Initialize
console.log('🎓 Smart E-Learning Automator loaded on YouTube');

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'start') {
    settings = request.settings;
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
      const videoTitle = document.querySelector('h1.ytd-video-primary-info-renderer')?.textContent?.trim() || 
                        document.querySelector('h1 yt-formatted-string')?.textContent?.trim() ||
                        document.title.replace(' - YouTube', '');
      
      sendResponse({ 
        success: true, 
        timestamp: timestamp,
        formattedTime: formatTime(timestamp),
        videoTitle: videoTitle,
        videoUrl: window.location.href,
        platform: 'youtube'
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
  console.log('▶️ Automation started');
  
  // Log activity
  chrome.runtime.sendMessage({
    action: 'logActivity',
    data: {
      type: 'automation_start',
      message: 'Automation started on YouTube',
      url: window.location.href
    }
  });
  
  // Apply settings
  setPlaybackSpeed(settings.playbackSpeed);
  
  // Start monitoring
  monitorVideo();
  
  if (settings.autoSkipAds) {
    setupAdSkipper();
  }
  
  if (settings.autoNext) {
    setupAutoNext();
  }
}

// Stop automation
function stopAutomation() {
  isAutomationRunning = false;
  console.log('⏹️ Automation stopped');
  
  chrome.runtime.sendMessage({
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
  const titleElement = document.querySelector('h1.ytd-watch-metadata yt-formatted-string');
  const title = titleElement ? titleElement.textContent : 'Unknown';
  
  currentVideoData = {
    title: title,
    url: window.location.href,
    platform: 'youtube',
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
      
      // Send progress to popup
      chrome.runtime.sendMessage({
        action: 'updateProgress',
        title: title,
        progress: Math.round(progress),
        currentTime: formatTime(video.currentTime),
        duration: formatTime(video.duration)
      });
    }
  }, 1000);
  
  // Remove old listener if exists to prevent duplicates
  if (videoEndHandlerAttached) {
    video.removeEventListener('ended', handleVideoEnd);
  }
  
  // Listen for video end (only once per video)
  video.addEventListener('ended', handleVideoEnd, { once: true });
  videoEndHandlerAttached = true;
  
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
  
  // Send completion to background
  chrome.runtime.sendMessage({
    action: 'videoCompleted',
    data: currentVideoData
  });
  
  console.log(`✅ Video ${videosWatchedCount} completed: ${currentVideoData.title}`);
  
  // Reset the flag for next video
  videoEndHandlerAttached = false;
  
  // Check video limit
  if (settings.videoLimit > 0 && videosWatchedCount >= settings.videoLimit) {
    console.log('🛑 Video limit reached');
    stopAutomation();
    alert('Video limit reached! Automation stopped.');
    return;
  }
  
  // Let YouTube's autoplay handle navigation
  console.log('⏭️ Waiting for YouTube autoplay to load next video...');
}

// Play next video
function playNextVideo() {
  // This function is no longer needed since YouTube autoplay handles it
  // Keeping it for backward compatibility but it won't be called
  console.log('Note: Auto-next is handled by YouTube autoplay');
}

// Setup ad skipper
function setupAdSkipper() {
  console.log('🚫 Ad skipper activated');
  
  setInterval(() => {
    if (!isAutomationRunning) return;
    
    // Try multiple selectors for skip buttons (YouTube updates these frequently)
    const skipSelectors = [
      '.ytp-ad-skip-button',
      '.ytp-skip-ad-button',
      'button.ytp-ad-skip-button-modern',
      '.ytp-ad-skip-button-container button',
      'button[class*="skip"]'
    ];
    
    for (const selector of skipSelectors) {
      const skipButton = document.querySelector(selector);
      if (skipButton && skipButton.offsetParent !== null) {
        skipButton.click();
        console.log('⏩ Skipped ad');
        
        chrome.runtime.sendMessage({
          action: 'logActivity',
          data: {
            type: 'ad_skipped',
            message: 'Ad skipped automatically'
          }
        });
        break; // Exit after clicking first found button
      }
    }
    
    // Close overlay ads
    const overlayCloseButton = document.querySelector('.ytp-ad-overlay-close-button');
    if (overlayCloseButton) {
      overlayCloseButton.click();
      console.log('❌ Closed overlay ad');
    }
    
    // Check if video is paused by ad and try to resume
    const video = document.querySelector('video');
    const adShowing = document.querySelector('.ad-showing');
    if (video && adShowing && video.paused) {
      // Sometimes we need to wait for skip button to appear
      const adTimeLeft = document.querySelector('.ytp-ad-preview-text');
      if (adTimeLeft) {
        console.log('⏳ Waiting for ad skip button...');
      }
    }
  }, 500); // Check more frequently for faster ad skipping
}

// Setup auto-next
function setupAutoNext() {
  // Monitor for autoplay toggle
  const autoplayToggle = document.querySelector('.ytp-autonav-toggle-button');
  if (autoplayToggle && autoplayToggle.getAttribute('aria-checked') === 'false') {
    autoplayToggle.click();
    console.log('✅ Autoplay enabled');
  }
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

// Handle page navigation (for YouTube's SPA)
let lastUrl = location.href;
new MutationObserver(() => {
  const url = location.href;
  if (url !== lastUrl) {
    lastUrl = url;
    if (isAutomationRunning && url.includes('watch')) {
      console.log('📺 New video detected');
      setTimeout(monitorVideo, 1000);
    }
  }
}).observe(document, { subtree: true, childList: true });
