import React, { useEffect, useState } from 'react';
import './Hero.css';
import { FaHeartbeat, FaPills, FaAppleAlt, FaDumbbell } from 'react-icons/fa';

const Hero = ({ scrollToSection }) => {
  const [isVisible, setIsVisible] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    // Check for dark mode preference
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    setIsDarkMode(mediaQuery.matches);
    
    const handleChange = (e) => setIsDarkMode(e.matches);
    mediaQuery.addEventListener('change', handleChange);
    
    // Trigger animation
    setTimeout(() => setIsVisible(true), 100);
    
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  return (
    <div className={`hero ${isDarkMode ? 'dark-mode' : ''}`}>
      <div className="hero-background">
        <div className="floating-elements">
          <div className="floating-element element-1"></div>
          <div className="floating-element element-2"></div>
          <div className="floating-element element-3"></div>
        </div>
      </div>
      
      <div className="hero-container">
        <div className={`hero-content ${isVisible ? 'visible' : ''}`}>
          <div className="hero-text">
            <h1 className="hero-title">
              Your Personal <span className="gradient-text">Healthcare</span> Assistant
            </h1>
            <p className="hero-subtitle">
              Get personalized health recommendations, medication guidance, and wellness plans 
              powered by advanced AI technology. Take control of your health journey today.
            </p>
            
            <div className="hero-features">
              <div className="feature-item">
                <div className="feature-icon">
                  <FaHeartbeat className="icon" />
                </div>
                <span>Health Assessment</span>
              </div>
              <div className="feature-item">
                <div className="feature-icon">
                  <FaPills className="icon" />
                </div>
                <span>Medication</span>
              </div>
              <div className="feature-item">
                <div className="feature-icon">
                  <FaAppleAlt className="icon" />
                </div>
                <span>Diet Plans</span>
              </div>
              <div className="feature-item">
                <div className="feature-icon">
                  <FaDumbbell className="icon" />
                </div>
                <span>Fitness</span>
              </div>
            </div>
            
            <div className="hero-actions">
              <button 
                className="btn btn-primary btn-large pulse"
                onClick={() => scrollToSection('assessment')}
              >
                Start Health Assessment
              </button>
              <button 
                className="btn btn-outline btn-large"
                onClick={() => scrollToSection('features')}
              >
                Learn More
              </button>
            </div>
          </div>
          
          <div className="hero-image">
            <div className="medical-illustration">
              <div className="pulse-ring"></div>
              <div className="heartbeat">
                <div className="heart"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="warning-banner">
        <div className="warning-content">
          <span className="warning-icon">⚠️</span>
          <div>
            <strong>Important Notice:</strong> This tool provides general health information only. 
            Always consult with qualified healthcare professionals before making any medical decisions. 
            Not a substitute for professional medical advice.
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;