"""
Quiz Solver Module
Automatically solves quizzes using ML/NLP and cached answers
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Optional, Tuple
import time
from config import ML_MODEL_NAME, CONFIDENCE_THRESHOLD, PLATFORMS
from database import Database

# Lazy import for transformers to avoid runtime errors
_transformers_available = True
try:
    from transformers import pipeline
except Exception as e:
    _transformers_available = False
    logging.warning(f"Transformers not available: {e}. Quiz solving will use simpler methods.")


class QuizSolver:
    """Solves quiz questions using ML/NLP and caching"""
    
    def __init__(self, platform: str, driver: webdriver.Chrome = None):
        self.platform = platform.lower()
        self.driver = driver
        self.db = Database()
        self.logger = logging.getLogger(__name__)
        
        # Initialize QA model (lazy loading)
        self._qa_model = None
        
        if self.platform not in PLATFORMS:
            raise ValueError(f"Unsupported platform: {platform}")
        
        self.config = PLATFORMS[self.platform]
    
    @property
    def qa_model(self):
        """Lazy load the QA model"""
        if self._qa_model is None:
            if not _transformers_available:
                self.logger.warning("Transformers not available. ML quiz solving disabled.")
                return None
            self.logger.info(f"Loading ML model: {ML_MODEL_NAME}")
            try:
                self._qa_model = pipeline("question-answering", model=ML_MODEL_NAME)
                self.db.add_log('ml_model', f'Loaded model: {ML_MODEL_NAME}', 'success')
            except Exception as e:
                self.logger.error(f"Failed to load ML model: {e}")
                self._qa_model = None
        return self._qa_model
    
    def extract_quiz_from_page(self) -> Optional[Dict]:
        """Extract quiz question and options from current page"""
        try:
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Platform-specific extraction
            if self.platform == 'coursera':
                return self._extract_coursera_quiz(soup)
            elif self.platform == 'udemy':
                return self._extract_udemy_quiz(soup)
            elif self.platform == 'moodle':
                return self._extract_moodle_quiz(soup)
            else:
                return self._extract_generic_quiz(soup)
        
        except Exception as e:
            self.logger.error(f"Error extracting quiz: {str(e)}")
            self.db.add_log('quiz_extract', f'Error: {str(e)}', 'error')
            return None
    
    def _extract_coursera_quiz(self, soup: BeautifulSoup) -> Optional[Dict]:
        """Extract quiz from Coursera"""
        try:
            question_elem = soup.find('div', {'data-test': 'quiz-question'})
            if not question_elem:
                return None
            
            question_text = question_elem.get_text(strip=True)
            
            # Get options
            options = []
            option_elems = soup.find_all('label', {'class': 'rc-Option'})
            for opt in option_elems:
                options.append(opt.get_text(strip=True))
            
            return {
                'question': question_text,
                'options': options,
                'type': 'multiple_choice'
            }
        except Exception as e:
            self.logger.error(f"Coursera quiz extraction error: {str(e)}")
            return None
    
    def _extract_udemy_quiz(self, soup: BeautifulSoup) -> Optional[Dict]:
        """Extract quiz from Udemy"""
        try:
            question_elem = soup.find('div', {'data-purpose': 'question-prompt'})
            if not question_elem:
                return None
            
            question_text = question_elem.get_text(strip=True)
            
            # Get options
            options = []
            option_elems = soup.find_all('label', {'class': 'mc-quiz-question--answer-label'})
            for opt in option_elems:
                options.append(opt.get_text(strip=True))
            
            return {
                'question': question_text,
                'options': options,
                'type': 'multiple_choice'
            }
        except Exception as e:
            self.logger.error(f"Udemy quiz extraction error: {str(e)}")
            return None
    
    def _extract_moodle_quiz(self, soup: BeautifulSoup) -> Optional[Dict]:
        """Extract quiz from Moodle"""
        try:
            question_elem = soup.find('div', {'class': 'qtext'})
            if not question_elem:
                return None
            
            question_text = question_elem.get_text(strip=True)
            
            # Get options
            options = []
            option_elems = soup.find_all('div', {'class': 'answer'})
            for opt in option_elems:
                options.append(opt.get_text(strip=True))
            
            return {
                'question': question_text,
                'options': options,
                'type': 'multiple_choice'
            }
        except Exception as e:
            self.logger.error(f"Moodle quiz extraction error: {str(e)}")
            return None
    
    def _extract_generic_quiz(self, soup: BeautifulSoup) -> Optional[Dict]:
        """Generic quiz extraction (fallback)"""
        # Try to find question and options using common patterns
        question = None
        options = []
        
        # Look for question
        for tag in ['h2', 'h3', 'p', 'div']:
            elem = soup.find(tag, text=lambda t: t and '?' in t)
            if elem:
                question = elem.get_text(strip=True)
                break
        
        # Look for options (radio buttons, checkboxes)
        for input_elem in soup.find_all(['input'], {'type': ['radio', 'checkbox']}):
            label = input_elem.find_next('label')
            if label:
                options.append(label.get_text(strip=True))
        
        if question and options:
            return {
                'question': question,
                'options': options,
                'type': 'multiple_choice'
            }
        
        return None
    
    def solve_question(self, question: str, options: List[str], context: str = "") -> Tuple[str, float]:
        """
        Solve a quiz question using ML/NLP
        Returns: (best_answer, confidence_score)
        """
        # Check cache first
        cached_answer = self.db.get_cached_answer(question)
        if cached_answer and cached_answer in options:
            self.logger.info(f"Using cached answer for: {question[:50]}...")
            return cached_answer, 1.0
        
        # Use ML model to find best answer
        best_answer = None
        best_score = 0.0
        
        # If context is provided, use it; otherwise use question as context
        if not context:
            context = question
        
        try:
            for option in options:
                # Use the QA model to score each option
                result = self.qa_model(question=question, context=f"{context}. {option}")
                score = result['score']
                
                if score > best_score:
                    best_score = score
                    best_answer = option
            
            self.logger.info(f"ML Answer: {best_answer} (confidence: {best_score:.2f})")
            
            # Cache if confidence is high
            if best_score >= CONFIDENCE_THRESHOLD and best_answer:
                self.db.cache_quiz_answer(question, best_answer)
            
            return best_answer, best_score
        
        except Exception as e:
            self.logger.error(f"Error solving question: {str(e)}")
            # Fallback: return first option
            return options[0] if options else None, 0.0
    
    def select_answer(self, answer: str):
        """Select the answer on the page"""
        try:
            # Platform-specific answer selection
            if self.platform == 'coursera':
                # Find the option with matching text
                option = self.driver.find_element(
                    By.XPATH, 
                    f"//label[contains(., '{answer}')]"
                )
                option.click()
            
            elif self.platform == 'udemy':
                option = self.driver.find_element(
                    By.XPATH,
                    f"//label[contains(@class, 'mc-quiz-question--answer-label') and contains(., '{answer}')]"
                )
                option.click()
            
            elif self.platform == 'moodle':
                option = self.driver.find_element(
                    By.XPATH,
                    f"//div[contains(@class, 'answer')]//label[contains(., '{answer}')]"
                )
                option.click()
            
            else:
                # Generic: find any radio/checkbox with matching label
                option = self.driver.find_element(
                    By.XPATH,
                    f"//label[contains(., '{answer}')]"
                )
                option.click()
            
            self.logger.info(f"Selected answer: {answer}")
            time.sleep(0.5)
            return True
        
        except Exception as e:
            self.logger.error(f"Error selecting answer: {str(e)}")
            return False
    
    def submit_quiz(self):
        """Submit the quiz"""
        try:
            submit_selector = self.config['selectors']['submit_button']
            submit_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, submit_selector))
            )
            submit_button.click()
            
            self.logger.info("Quiz submitted")
            self.db.add_log('quiz_submit', 'Quiz submitted', 'success')
            time.sleep(2)
            return True
        
        except Exception as e:
            self.logger.error(f"Error submitting quiz: {str(e)}")
            self.db.add_log('quiz_submit', f'Error: {str(e)}', 'error')
            return False
    
    def auto_solve_quiz(self, context: str = "") -> bool:
        """
        Automatically solve and submit current quiz
        context: Additional context to help answer questions (e.g., video transcript)
        """
        try:
            # Extract quiz
            quiz_data = self.extract_quiz_from_page()
            if not quiz_data:
                self.logger.warning("No quiz found on page")
                return False
            
            question = quiz_data['question']
            options = quiz_data['options']
            
            self.logger.info(f"Question: {question}")
            self.logger.info(f"Options: {options}")
            
            # Solve question
            answer, confidence = self.solve_question(question, options, context)
            
            if not answer:
                self.logger.error("Could not determine answer")
                return False
            
            # Select answer
            if not self.select_answer(answer):
                return False
            
            # Submit
            if not self.submit_quiz():
                return False
            
            # Save attempt
            self.db.save_quiz_attempt(
                platform=self.platform,
                question_text=question,
                options=options,
                user_answer=answer,
                confidence=confidence
            )
            
            return True
        
        except Exception as e:
            self.logger.error(f"Error auto-solving quiz: {str(e)}")
            self.db.add_log('quiz_auto_solve', f'Error: {str(e)}', 'error')
            return False
