import React, { useEffect, useState } from 'react';
import { FaHeart, FaShieldAlt, FaPhoneAlt, FaEnvelope, FaExclamationTriangle } from 'react-icons/fa';
import './Footer.css';

const Footer = () => {
  const [currentYear, setCurrentYear] = useState(new Date().getFullYear());
  const [isVisible, setIsVisible] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    // Check for dark mode preference
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    setIsDarkMode(mediaQuery.matches);
    
    const handleChange = (e) => setIsDarkMode(e.matches);
    mediaQuery.addEventListener('change', handleChange);
    
    // Trigger animation
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, 300);
    
    return () => {
      mediaQuery.removeEventListener('change', handleChange);
      clearTimeout(timer);
    };
  }, []);

  return (
    <footer className={`footer ${isDarkMode ? 'dark-mode' : ''} ${isVisible ? 'visible' : ''}`}>
      <div className="footer-wave">
        <svg viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512,54.67,583,72c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25" className="shape-fill"></path>
          <path d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z" opacity=".5" className="shape-fill"></path>
          <path d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z" className="shape-fill"></path>
        </svg>
      </div>
      
      <div className="footer-content">
        <div className="footer-main">
          <div className="footer-brand">
            <div className="footer-logo">
              <FaHeart className="logo-icon" />
              <span>HealthCare AI</span>
            </div>
            <p className="footer-description">
              Your trusted companion for health and wellness guidance, powered by advanced AI technology.
            </p>
            <div className="footer-social">
              <a href="#" aria-label="Facebook" className="social-link">
                <i className="fab fa-facebook-f"></i>
              </a>
              <a href="#" aria-label="Twitter" className="social-link">
                <i className="fab fa-twitter"></i>
              </a>
              <a href="#" aria-label="Instagram" className="social-link">
                <i className="fab fa-instagram"></i>
              </a>
              <a href="#" aria-label="LinkedIn" className="social-link">
                <i className="fab fa-linkedin-in"></i>
              </a>
            </div>
          </div>
          
          <div className="footer-links">
            <div className="footer-links-group">
              <h4 className="footer-heading">Quick Links</h4>
              <ul className="footer-menu">
                <li><a href="#home" className="footer-link">Home</a></li>
                <li><a href="#assessment" className="footer-link">Health Assessment</a></li>
                <li><a href="#about" className="footer-link">About Us</a></li>
                <li><a href="#blog" className="footer-link">Blog</a></li>
                <li><a href="#contact" className="footer-link">Contact</a></li>
              </ul>
            </div>
            
            <div className="footer-links-group">
              <h4 className="footer-heading">Legal</h4>
              <ul className="footer-menu">
                <li><a href="#privacy" className="footer-link">Privacy Policy</a></li>
                <li><a href="#terms" className="footer-link">Terms of Service</a></li>
                <li><a href="#cookies" className="footer-link">Cookie Policy</a></li>
                <li><a href="#disclaimer" className="footer-link">Medical Disclaimer</a></li>
              </ul>
            </div>
            
            <div className="footer-links-group">
              <h4 className="footer-heading">Contact Us</h4>
              <ul className="footer-contact">
                <li className="contact-item">
                  <FaEnvelope className="contact-icon" />
                  <a href="mailto:info@healthcareai.com" className="footer-link">info@healthcareai.com</a>
                </li>
                <li className="contact-item">
                  <FaPhoneAlt className="contact-icon" />
                  <a href="tel:+15551234567" className="footer-link">+1 (555) 123-4567</a>
                </li>
                <li className="contact-item emergency">
                  <FaExclamationTriangle className="contact-icon" />
                  <span>Emergency: Always call 911</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <div className="footer-newsletter">
          <h4 className="newsletter-title">Subscribe to our Newsletter</h4>
          <p className="newsletter-description">Get the latest health tips and updates delivered to your inbox.</p>
          <form className="newsletter-form">
            <input 
              type="email" 
              placeholder="Enter your email" 
              className="newsletter-input" 
              required 
              aria-label="Email address"
            />
            <button type="submit" className="newsletter-button">
              Subscribe
            </button>
          </form>
        </div>
      </div>
      
      <div className="footer-bottom">
        <div className="container">
          <p className="copyright">
            &copy; {currentYear} HealthCare AI. All rights reserved.
          </p>
          <div className="footer-legal">
            <span className="disclaimer">
              <FaShieldAlt className="disclaimer-icon" />
              This tool is for informational purposes only and is not a substitute for professional medical advice.
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;