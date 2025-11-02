"""
Video Automation Module
Handles automatic video playback using Selenium
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import logging
import os
import tempfile
import platform
import getpass
from typing import Dict, Optional
from config import PLATFORMS, DEFAULT_WAIT_TIME, VIDEO_CHECK_INTERVAL
from database import Database


class VideoAutomator:
    """Automates video playback on various learning platforms"""
    
    def __init__(self, platform: str, headless: bool = False, playback_speed: float = 1.0, user_id: int = None):
        self.platform = platform.lower()
        self.db = Database(user_id=user_id)  # User-specific database
        self.user_id = user_id
        self.driver = None
        self.headless = headless
        self.playback_speed = playback_speed
        self.logger = logging.getLogger(__name__)
        
        if self.platform not in PLATFORMS:
            raise ValueError(f"Unsupported platform: {platform}")
        
        self.config = PLATFORMS[self.platform]
    
    def init_driver(self):
        """Initialize Selenium WebDriver"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # Additional options for better stability
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # IMPORTANT: Unique user data directory per user AND machine to prevent cross-device/user conflicts
        import tempfile
        import platform
        import getpass
        machine_id = f"{platform.node()}_{getpass.getuser()}".replace(" ", "_")
        
        # Add user_id to make it unique per user
        if self.user_id:
            profile_name = f'selenium_profile_user{self.user_id}_{machine_id}'
        else:
            profile_name = f'selenium_profile_{machine_id}'
        
        user_data_dir = os.path.join(tempfile.gettempdir(), profile_name)
        chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
        
        # User agent to avoid detection
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        
        self.logger.info(f"WebDriver initialized for {self.platform} on {machine_id} (user: {self.user_id})")
        self.db.add_log('driver_init', f'WebDriver initialized for {self.platform}', 'success')
    
    def login(self, credentials: Dict[str, str]):
        """
        Login to the learning platform
        credentials: {'username': '...', 'password': '...'}
        """
        if not self.driver:
            self.init_driver()
        
        try:
            # Platform-specific login logic
            if self.platform == 'coursera':
                self.driver.get('https://www.coursera.org/?authMode=login')
                
                # Wait for login form
                email_field = WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
                    EC.presence_of_element_located((By.ID, 'email'))
                )
                password_field = self.driver.find_element(By.ID, 'password')
                
                email_field.send_keys(credentials['username'])
                password_field.send_keys(credentials['password'])
                
                # Submit
                login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
                login_button.click()
                
                time.sleep(3)
                self.logger.info("Logged in to Coursera")
                self.db.add_log('login', 'Successfully logged in to Coursera', 'success')
            
            elif self.platform == 'udemy':
                self.driver.get('https://www.udemy.com/join/login-popup/')
                
                email_field = WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
                    EC.presence_of_element_located((By.ID, 'email--1'))
                )
                password_field = self.driver.find_element(By.ID, 'password--2')
                
                email_field.send_keys(credentials['username'])
                password_field.send_keys(credentials['password'])
                
                login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
                login_button.click()
                
                time.sleep(3)
                self.logger.info("Logged in to Udemy")
                self.db.add_log('login', 'Successfully logged in to Udemy', 'success')
            
            else:
                self.logger.warning(f"Login not implemented for {self.platform}")
                self.db.add_log('login', f'Login not implemented for {self.platform}', 'warning')
        
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            self.db.add_log('login', f'Login failed: {str(e)}', 'error')
            raise
    
    def navigate_to_playlist(self, playlist_url: str):
        """Navigate to a playlist/course and enable autoplay"""
        if not self.driver:
            self.init_driver()
        
        self.driver.get(playlist_url)
        time.sleep(3)
        
        # Enable YouTube autoplay if it's disabled
        if self.platform == 'youtube':
            try:
                # Wait for page to load
                time.sleep(2)
                
                # Find autoplay toggle button
                autoplay_selectors = [
                    'button.ytp-button[data-tooltip-target-id="ytp-autonav-toggle-button"]',
                    '.ytp-autonav-toggle-button',
                    'button[aria-label*="Autoplay"]'
                ]
                
                for selector in autoplay_selectors:
                    try:
                        autoplay_toggle = self.driver.find_element(By.CSS_SELECTOR, selector)
                        aria_checked = autoplay_toggle.get_attribute('aria-checked')
                        
                        if aria_checked == 'false':
                            autoplay_toggle.click()
                            self.logger.info("✅ Enabled YouTube autoplay")
                            time.sleep(1)
                            break
                        else:
                            self.logger.info("✅ YouTube autoplay already enabled")
                            break
                    except NoSuchElementException:
                        continue
            except Exception as e:
                self.logger.debug(f"Could not toggle autoplay: {str(e)}")
        
        self.logger.info(f"Navigated to: {playlist_url}")
        self.db.add_log('navigation', f'Navigated to playlist: {playlist_url}', 'info')
    
    def set_playback_speed(self, speed: float = None):
        """
        Set video playback speed
        speed: 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0
        """
        if speed is None:
            speed = self.playback_speed
        
        try:
            video_selector = self.config['selectors']['video_player']
            video = self.driver.find_element(By.CSS_SELECTOR, video_selector)
            
            # Set playback speed using JavaScript
            self.driver.execute_script(f"arguments[0].playbackRate = {speed}", video)
            
            self.logger.info(f"Playback speed set to {speed}x")
            self.db.add_log('playback_speed', f'Speed set to {speed}x', 'info')
            return True
        except Exception as e:
            self.logger.error(f"Error setting playback speed: {str(e)}")
            return False
    
    def play_video(self):
        """Start playing the current video - Enhanced version with manual pause detection"""
        try:
            video_selector = self.config['selectors']['video_player']
            
            # Wait for video element to be present
            video_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, video_selector))
            )
            
            # Wait for video to be ready (check if duration is available)
            self.logger.info("Waiting for video to be ready...")
            max_wait = 10
            for i in range(max_wait):
                try:
                    duration = self.driver.execute_script("return arguments[0].duration", video_element)
                    if duration and duration > 0 and not float('inf') == duration:
                        self.logger.info(f"Video ready (duration: {duration:.1f}s)")
                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.logger.warning("Video duration not detected, proceeding anyway...")
            
            # Wait a bit more for page to fully load
            time.sleep(2)
            
            # Skip ads immediately before playing
            self._skip_ads()
            
            # Set playback speed BEFORE starting playback (FIX BUG #2)
            time.sleep(1)
            self.set_playback_speed()
            self.logger.info(f"✅ Playback speed set to {self.playback_speed}x")
            
            # Click play if paused (try multiple selectors)
            play_button_selectors = [
                'button.ytp-play-button',
                '.ytp-play-button',
                'button[aria-label*="Play"]',
                '.ytp-large-play-button'
            ]
            
            for selector in play_button_selectors:
                try:
                    play_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    # Check if video is paused
                    paused = self.driver.execute_script("return arguments[0].paused", video_element)
                    if paused:
                        play_button.click()
                        self.logger.info("Clicked play button")
                        time.sleep(1)
                        break
                except:
                    continue
            
            # Alternative: Click on video player itself to play
            try:
                if self.driver.execute_script("return arguments[0].paused", video_element):
                    video_element.click()
                    self.logger.info("Clicked video element to play")
                    time.sleep(1)
            except:
                pass
            
            # Verify video is actually playing
            time.sleep(2)
            try:
                is_playing = self.driver.execute_script(
                    "return !arguments[0].paused && arguments[0].currentTime > 0", 
                    video_element
                )
                if not is_playing:
                    self.logger.warning("Video not playing, trying again...")
                    video_element.click()
                    time.sleep(1)
                else:
                    self.logger.info("✅ Video is playing")
            except:
                pass
            
            # Save video to database immediately (FIX BUG #3)
            current_url = self.driver.current_url
            self.db.add_video(self.platform, current_url, title=self.driver.title)
            self.db.add_log('video_play', f'Started playing: {self.driver.title}', 'success')
            
        except TimeoutException:
            self.logger.error("Video player not found")
            self.db.add_log('video_play', 'Video player not found', 'error')
        except Exception as e:
            self.logger.error(f"Error playing video: {str(e)}")
            self.db.add_log('video_play', f'Error: {str(e)}', 'error')
    
    def _skip_ads(self):
        """Skip ads if present - Enhanced version"""
        try:
            # YouTube ad skip button (appears after 5 seconds)
            ad_skip_selectors = [
                'button.ytp-ad-skip-button',
                'button.ytp-ad-skip-button-modern',
                '.ytp-ad-skip-button',
                'button[class*="skip"]',
                '.videoAdUiSkipButton'
            ]
            
            for selector in ad_skip_selectors:
                try:
                    skip_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if skip_button.is_displayed() and skip_button.is_enabled():
                        skip_button.click()
                        self.logger.info("Ad skipped successfully")
                        time.sleep(1)
                        return True
                except (NoSuchElementException, Exception):
                    continue
            
            # Check if ad is playing (YouTube specific)
            try:
                ad_indicator = self.driver.find_element(By.CSS_SELECTOR, '.ytp-ad-player-overlay, .video-ads')
                if ad_indicator.is_displayed():
                    self.logger.info("Ad detected, waiting for skip button...")
                    # Wait up to 6 seconds for skip button
                    for _ in range(6):
                        time.sleep(1)
                        if self._skip_ads():  # Recursive check
                            return True
            except NoSuchElementException:
                pass  # No ad present
                
        except Exception as e:
            self.logger.debug(f"Ad skip check: {str(e)}")
        
        return False
    
    def is_video_complete(self) -> bool:
        """Check if current video has finished"""
        try:
            video_selector = self.config['selectors']['video_player']
            video = self.driver.find_element(By.CSS_SELECTOR, video_selector)
            
            # Get current time and duration using JavaScript
            current_time = self.driver.execute_script("return arguments[0].currentTime", video)
            duration = self.driver.execute_script("return arguments[0].duration", video)
            
            # Make sure duration is valid (not 0, not infinity, not NaN)
            if not duration or duration <= 0 or float('inf') == duration:
                return False
            
            # Make sure current_time is valid
            if not current_time or current_time < 0:
                return False
            
            # Consider complete if within last 3 seconds (more precise)
            time_remaining = duration - current_time
            if time_remaining < 3:
                self.logger.info(f"Video nearly complete: {time_remaining:.1f}s remaining")
                return True
            
            return False
        except Exception as e:
            self.logger.debug(f"Error checking video completion: {str(e)}")
            return False
    
    def next_video(self):
        """Move to next video in playlist - Enhanced for YouTube autoplay with longer timeout"""
        try:
            # Save current URL to detect if we actually moved
            current_url = self.driver.current_url
            self.db.mark_video_completed(current_url)
            
            # For YouTube, try multiple approaches
            if self.platform == 'youtube':
                # Method 1: Click next button
                next_button_selectors = [
                    'a.ytp-next-button',
                    '.ytp-next-button',
                    'button.ytp-next-button',
                    'a[aria-label*="Next"]'
                ]
                
                for selector in next_button_selectors:
                    try:
                        next_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        next_button.click()
                        self.logger.info("Clicked next button")
                        time.sleep(3)  # Wait for navigation
                        
                        # Check if URL changed
                        if self.driver.current_url != current_url:
                            self.db.add_log('video_next', 'Moved to next video via button', 'success')
                            return True
                    except:
                        continue
                
                # Method 2: Wait for autoplay (YouTube usually autoplays next video)
                # Increased timeout for large playlists
                self.logger.info("Waiting for YouTube autoplay (up to 30 seconds)...")
                for i in range(30):  # Wait up to 30 seconds (increased from 10)
                    time.sleep(1)
                    new_url = self.driver.current_url
                    if new_url != current_url:
                        # Verify it's not just a URL parameter change
                        if 'watch?v=' in new_url:
                            video_id_old = current_url.split('watch?v=')[1].split('&')[0] if 'watch?v=' in current_url else ''
                            video_id_new = new_url.split('watch?v=')[1].split('&')[0] if 'watch?v=' in new_url else ''
                            if video_id_old != video_id_new:
                                self.logger.info(f"✅ Video autoplay detected (after {i+1}s)")
                                self.db.add_log('video_next', f'Autoplay to next video (waited {i+1}s)', 'success')
                                return True
                
                # Method 3: Check if we're at the end of playlist
                try:
                    # Look for "End of playlist" or similar indicators
                    end_indicators = [
                        'ytd-playlist-panel-renderer[playlist-type="WATCH_QUEUE_PANEL"]',
                        '.ytp-upnext-autoplay-icon'
                    ]
                    
                    # If next button is disabled, we're at the end
                    next_button = self.driver.find_element(By.CSS_SELECTOR, 'a.ytp-next-button')
                    if 'ytp-button-disabled' in next_button.get_attribute('class'):
                        self.logger.info("🏁 Next button disabled - reached end of playlist")
                        return False
                except:
                    pass
                
                # Method 4: Try to enable autoplay if disabled
                try:
                    autoplay_toggle = self.driver.find_element(By.CSS_SELECTOR, 'button.ytp-button[data-tooltip-target-id="ytp-autonav-toggle-button"]')
                    aria_checked = autoplay_toggle.get_attribute('aria-checked')
                    if aria_checked == 'false':
                        autoplay_toggle.click()
                        self.logger.info("Enabled autoplay, waiting for navigation...")
                        time.sleep(5)
                        if self.driver.current_url != current_url:
                            self.db.add_log('video_next', 'Autoplay enabled and moved to next', 'success')
                            return True
                except:
                    pass
            
            else:
                # For other platforms, use configured next button
                next_button_selector = self.config['selectors']['next_button']
                next_button = WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, next_button_selector))
                )
                next_button.click()
                time.sleep(2)
                self.logger.info("Moved to next video")
                self.db.add_log('video_next', 'Moved to next video', 'success')
                return True
            
            self.logger.warning("⚠️ Could not move to next video after all attempts")
            return False
            
        except TimeoutException:
            self.logger.warning("Next button not found - might be last video in playlist")
            self.db.add_log('video_next', 'Next button not found', 'warning')
            return False
        except Exception as e:
            self.logger.error(f"Error moving to next video: {str(e)}")
            return False
    
    def automate_playlist(self, playlist_url: str, video_limit: int = None, playback_speed: float = None):
        """
        Automate watching entire playlist - Enhanced with better ad handling and error recovery
        video_limit: Maximum number of videos to watch (None = all videos)
        playback_speed: Speed multiplier (0.5x to 2.0x)
        """
        if playback_speed:
            self.playback_speed = playback_speed
        
        self.navigate_to_playlist(playlist_url)
        videos_watched = 0
        consecutive_errors = 0
        max_consecutive_errors = 3
        
        self.logger.info(f"Starting playlist automation (limit: {video_limit if video_limit else 'unlimited'})")
        
        while True:
            try:
                # Check if we've reached the video limit
                if video_limit and videos_watched >= video_limit:
                    self.logger.info(f"✅ Reached video limit: {video_limit}")
                    break
                
                # Play current video
                self.logger.info(f"▶️ Playing video {videos_watched + 1}...")
                self.play_video()
                
                # Update progress immediately after starting video (FIX BUG #3)
                current_url = self.driver.current_url
                videos_watched += 1
                self.db.increment_video_count(playlist_url, videos_watched)
                self.logger.info(f"📊 Progress updated: {videos_watched} videos watched")
                
                # Monitor video playback with continuous ad checking and manual pause detection
                last_check_time = time.time()
                ad_check_interval = 5  # Check for ads every 5 seconds
                last_user_pause_check = time.time()
                user_pause_check_interval = 2  # Check for manual pause every 2 seconds (FIX BUG #1)
                
                while not self.is_video_complete():
                    # Regular interval check
                    time.sleep(VIDEO_CHECK_INTERVAL)
                    
                    # Periodic ad skip check
                    current_time = time.time()
                    if current_time - last_check_time >= ad_check_interval:
                        self._skip_ads()
                        # Re-apply playback speed after ad (FIX BUG #2)
                        self.set_playback_speed()
                        last_check_time = current_time
                    
                    # Check for manual user pause (FIX BUG #1)
                    if current_time - last_user_pause_check >= user_pause_check_interval:
                        try:
                            video = self.driver.find_element(By.CSS_SELECTOR, self.config['selectors']['video_player'])
                            is_paused = self.driver.execute_script("return arguments[0].paused", video)
                            
                            if is_paused:
                                self.logger.info("⏸️ Video manually paused by user - waiting for resume...")
                                # Wait for user to resume (check every second)
                                while True:
                                    time.sleep(1)
                                    is_still_paused = self.driver.execute_script("return arguments[0].paused", video)
                                    if not is_still_paused:
                                        self.logger.info("▶️ Video resumed by user")
                                        # Re-apply playback speed after resume (FIX BUG #2)
                                        self.set_playback_speed()
                                        break
                                    
                                    # Check if user closed the browser
                                    try:
                                        self.driver.current_url
                                    except:
                                        self.logger.info("🛑 Browser closed by user")
                                        return
                            
                            last_user_pause_check = current_time
                        except Exception as e:
                            self.logger.debug(f"Pause check: {str(e)}")
                    
                    # Make sure video is still playing (not paused by ad or system)
                    try:
                        video = self.driver.find_element(By.CSS_SELECTOR, self.config['selectors']['video_player'])
                        is_paused = self.driver.execute_script("return arguments[0].paused", video)
                        
                        # Only auto-resume if NOT manually paused by user
                        # Check if it's been paused for less than 1 second (likely ad or system pause)
                        if is_paused:
                            time.sleep(0.5)  # Brief wait
                            still_paused = self.driver.execute_script("return arguments[0].paused", video)
                            if still_paused:
                                # Check current time - if it's progressing, user might have paused
                                current_time_video = self.driver.execute_script("return arguments[0].currentTime", video)
                                time.sleep(1)
                                new_time_video = self.driver.execute_script("return arguments[0].currentTime", video)
                                
                                # If time is NOT progressing and it's been paused briefly, it's likely ad/system pause
                                if abs(new_time_video - current_time_video) < 0.1:
                                    self.logger.warning("⚠️ Video paused (possibly by ad), attempting to resume...")
                                    try:
                                        play_btn = self.driver.find_element(By.CSS_SELECTOR, 'button.ytp-play-button')
                                        play_btn.click()
                                        time.sleep(1)
                                        # Re-apply playback speed after resume (FIX BUG #2)
                                        self.set_playback_speed()
                                    except:
                                        video.click()
                                        time.sleep(1)
                                        self.set_playback_speed()
                    except Exception as e:
                        self.logger.debug(f"Playback check: {str(e)}")
                
                consecutive_errors = 0  # Reset error count on successful completion
                self.logger.info(f"✅ Completed video {videos_watched}")
                
                # Mark video as completed
                self.db.mark_video_completed(current_url)
                
                # Move to next video
                self.logger.info(f"Moving to next video...")
                if not self.next_video():
                    self.logger.info("🏁 Reached end of playlist (no more videos)")
                    break
                
                # Wait for next video to fully load
                self.logger.info("Waiting for next video to load...")
                time.sleep(5)  # Initial wait
                
                # Wait for video element to be present and ready
                try:
                    video_selector = self.config['selectors']['video_player']
                    WebDriverWait(self.driver, 15).until(  # Increased timeout to 15 seconds
                        EC.presence_of_element_located((By.CSS_SELECTOR, video_selector))
                    )
                    self.logger.info("✅ Next video loaded and ready")
                    
                    # IMPORTANT: Re-apply playback speed for new video (FIX BUG #2)
                    time.sleep(2)  # Wait for video to initialize
                    self.set_playback_speed()
                    self.logger.info(f"✅ Playback speed re-applied: {self.playback_speed}x")
                    
                except TimeoutException:
                    self.logger.warning("⚠️ Video element not found after navigation, retrying...")
                    consecutive_errors += 1
                    if consecutive_errors >= max_consecutive_errors:
                        self.logger.error(f"❌ Too many consecutive errors ({max_consecutive_errors}), stopping automation")
                        break
                    time.sleep(3)
                    continue  # Skip to next iteration
                
            except KeyboardInterrupt:
                self.logger.info("⏹️ Automation stopped by user")
                break
            except Exception as e:
                self.logger.error(f"❌ Error in automation loop: {str(e)}")
                consecutive_errors += 1
                if consecutive_errors >= max_consecutive_errors:
                    self.logger.error(f"❌ Too many consecutive errors ({max_consecutive_errors}), stopping automation")
                    break
                self.logger.info(f"Retrying... (error count: {consecutive_errors}/{max_consecutive_errors})")
                time.sleep(5)
                continue
        
        self.logger.info(f"🎉 Automation complete. Watched {videos_watched} videos")
        self.db.add_log('automation_complete', f'Watched {videos_watched} videos from {playlist_url}', 'success')
        self.db.update_playlist_progress(playlist_url, videos_watched)
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed")
            self.db.add_log('driver_close', 'Browser closed', 'info')
