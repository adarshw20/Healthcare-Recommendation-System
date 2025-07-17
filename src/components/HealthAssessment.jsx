import React, { useState, useEffect } from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { FaInfoCircle, FaExclamationTriangle, FaCheckCircle, FaArrowRight, FaArrowLeft } from 'react-icons/fa';
import './HealthAssessment.css';

const HealthAssessment = ({ onSubmit, loading }) => {
  const { isDarkMode } = useTheme();
  
  // Set theme attribute on component mount and when theme changes
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', isDarkMode ? 'dark' : 'light');
  }, [isDarkMode]);
  const [formData, setFormData] = useState({
    age: '',
    gender: '',
    height: '',
    weight: '',
    currentSymptoms: [], // Initialize as empty array
    symptoms: [],
    duration: '',
    severity: '',
    medications: '',
    allergies: '',
    lifestyle: {
      smoking: false,
      alcohol: false,
      exercise: '',
      sleep: ''
    }
  });

  // Use symptoms array as the single source of truth for selected symptoms
  const selectedSymptoms = Array.isArray(formData.symptoms) ? formData.symptoms : [];

  const [currentStep, setCurrentStep] = useState(1);
  const totalSteps = 4;

  const symptomOptions = [
    'fever', 'headache', 'cough', 'fatigue', 'nausea', 'dizziness',
    'chest pain', 'shortness of breath', 'muscle pain', 'sore throat',
    'runny nose', 'stomach pain', 'back pain', 'joint pain'
  ];

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (name.startsWith('lifestyle.')) {
      const lifestyleField = name.split('.')[1];
      setFormData(prev => ({
        ...prev,
        lifestyle: {
          ...prev.lifestyle,
          [lifestyleField]: type === 'checkbox' ? checked : value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : value
      }));
    }
  };

  const handleSymptomToggle = (symptom) => {
    setFormData(prev => ({
      ...prev,
      symptoms: prev.symptoms.includes(symptom)
        ? prev.symptoms.filter(s => s !== symptom)
        : [...prev.symptoms, symptom]
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted with data:', formData);
    if (onSubmit && typeof onSubmit === 'function') {
      onSubmit(formData);
    } else {
      console.error('onSubmit prop is not a function');
    }
  };

  const nextStep = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="step-content fade-in">
            <h3>Basic Information</h3>
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="age">Age</label>
                <input
                  type="number"
                  id="age"
                  name="age"
                  value={formData.age}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="gender">Gender</label>
                <select
                  id="gender"
                  name="gender"
                  value={formData.gender}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select Gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="height">Height (cm)</label>
                <input
                  type="number"
                  id="height"
                  name="height"
                  value={formData.height}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="weight">Weight (kg)</label>
                <input
                  type="number"
                  id="weight"
                  name="weight"
                  value={formData.weight}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </div>
          </div>
        );
      
      case 2:
        return (
          <div className="step-content fade-in">
            <h3>Symptoms & Concerns</h3>
            <div className="form-group">
              <label>Current Symptoms (select all that apply)</label>
              <div className="symptoms-grid">
                {symptomOptions.map(symptom => (
                  <div
                    key={symptom}
                    className={`symptom-card ${formData.symptoms.includes(symptom) ? 'selected' : ''}`}
                    onClick={() => handleSymptomToggle(symptom)}
                  >
                    {symptom}
                  </div>
                ))}
              </div>
            </div>
            
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="duration">Duration of symptoms</label>
                <select
                  id="duration"
                  name="duration"
                  value={formData.duration}
                  onChange={handleInputChange}
                >
                  <option value="">Select duration</option>
                  <option value="1-2 days">1-2 days</option>
                  <option value="3-7 days">3-7 days</option>
                  <option value="1-2 weeks">1-2 weeks</option>
                  <option value="more than 2 weeks">More than 2 weeks</option>
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="severity">Severity level</label>
                <select
                  id="severity"
                  name="severity"
                  value={formData.severity}
                  onChange={handleInputChange}
                >
                  <option value="">Select severity</option>
                  <option value="mild">Mild</option>
                  <option value="moderate">Moderate</option>
                  <option value="severe">Severe</option>
                </select>
              </div>
            </div>
          </div>
        );
      
      case 3:
        return (
          <div className="step-content fade-in">
            <h3>Medical History</h3>
            <div className="form-group">
              <label htmlFor="medications">Current Medications</label>
              <textarea
                id="medications"
                name="medications"
                value={formData.medications}
                onChange={handleInputChange}
                placeholder="List any medications you're currently taking..."
                rows="4"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="allergies">Known Allergies</label>
              <textarea
                id="allergies"
                name="allergies"
                value={formData.allergies}
                onChange={handleInputChange}
                placeholder="List any known allergies..."
                rows="4"
              />
            </div>
          </div>
        );
      
      case 4:
        return (
          <div className="step-content fade-in">
            <h3>Lifestyle Information</h3>
            <div className="form-grid">
              <div className="form-group">
                <label>
                  <input
                    type="checkbox"
                    name="lifestyle.smoking"
                    checked={formData.lifestyle.smoking}
                    onChange={handleInputChange}
                  />
                  Do you smoke?
                </label>
              </div>
              <div className="form-group">
                <label>
                  <input
                    type="checkbox"
                    name="lifestyle.alcohol"
                    checked={formData.lifestyle.alcohol}
                    onChange={handleInputChange}
                  />
                  Do you consume alcohol regularly?
                </label>
              </div>
              <div className="form-group">
                <label htmlFor="exercise">Exercise frequency</label>
                <select
                  id="exercise"
                  name="lifestyle.exercise"
                  value={formData.lifestyle.exercise}
                  onChange={handleInputChange}
                >
                  <option value="">Select frequency</option>
                  <option value="never">Never</option>
                  <option value="rarely">Rarely</option>
                  <option value="sometimes">Sometimes</option>
                  <option value="regularly">Regularly</option>
                  <option value="daily">Daily</option>
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="sleep">Average sleep hours</label>
                <select
                  id="sleep"
                  name="lifestyle.sleep"
                  value={formData.lifestyle.sleep}
                  onChange={handleInputChange}
                >
                  <option value="">Select hours</option>
                  <option value="less than 6">Less than 6 hours</option>
                  <option value="6-7">6-7 hours</option>
                  <option value="7-8">7-8 hours</option>
                  <option value="8-9">8-9 hours</option>
                  <option value="more than 9">More than 9 hours</option>
                </select>
              </div>
            </div>
          </div>
        );
      
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <div className="assessment-container">
        <div className="card">
          <div className="loading-state">
            <div className="loading-spinner"></div>
            <h3>Analyzing Your Health Data...</h3>
            <p>Please wait while we generate your personalized recommendations.</p>
          </div>
        </div>
      </div>
    );
  }

  // Calculate progress percentage for the progress bar
  const progressPercentage = (currentStep / totalSteps) * 100;
  
  return (
    <div className="assessment-container">
      <div className="card">
        <div className="assessment-header">
          <h2>Health Assessment</h2>
          <div className="progress-container">
            <div className="progress-text">
              <span>Progress</span>
              <span>{currentStep} of {totalSteps}</span>
            </div>
            <div className="progress-bar">
              <div 
                className="progress-fill"
                style={{ width: `${progressPercentage}%` }}
                aria-valuenow={progressPercentage}
                aria-valuemin="0"
                aria-valuemax="100"
              ></div>
            </div>
          </div>
        </div>
        
        <form onSubmit={handleSubmit} className="assessment-form">
          {renderStep()}
          
          <div className="form-actions">
            {currentStep > 1 && (
              <button 
                type="button" 
                className="btn btn-secondary" 
                onClick={prevStep}
                disabled={loading}
              >
                <FaArrowLeft className="btn-icon" />
                Previous
              </button>
            )}
            
            <div className="step-indicator">
              Step {currentStep} of {totalSteps}
            </div>
            
            {currentStep < totalSteps ? (
              <button 
                type="button" 
                className="btn btn-primary" 
                onClick={nextStep}
                disabled={loading}
              >
                Next
                <FaArrowRight className="btn-icon" />
              </button>
            ) : (
              <button 
                type="submit" 
                className="btn btn-primary submit-btn"
                disabled={loading || selectedSymptoms.length === 0}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Processing...
                  </>
                ) : (
                  <>
                    <FaCheckCircle className="btn-icon" />
                    Get Recommendations
                  </>
                )}
              </button>
            )}
          </div>
          
          {selectedSymptoms.length === 0 && currentStep === totalSteps && (
            <div className="warning-message">
              <FaExclamationTriangle />
              <div>
                <strong>Please select at least one symptom</strong> to get personalized recommendations.
              </div>
            </div>
          )}
        </form>
      </div>
    </div>
  );
};

export default HealthAssessment;