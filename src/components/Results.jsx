import React, { useRef, useState, useEffect } from 'react';
import { useTheme } from '../contexts/ThemeContext';
import './Results.css';
import { useReactToPrint } from 'react-to-print';
import { FaPrint, FaCalendarAlt, FaShare, FaPills, FaHeartbeat, FaUtensils, FaDumbbell, FaWeight, FaRuler, FaUser, FaVenusMars } from 'react-icons/fa';

const Results = React.forwardRef(({ assessmentData, recommendations, loading }, ref) => {
  const { isDarkMode } = useTheme();
  const [isClient, setIsClient] = useState(false);
  const printRef = useRef();

  useEffect(() => {
    setIsClient(true);
  }, []);

  const handlePrint = useReactToPrint({
    content: () => printRef.current,
    documentTitle: 'Health_Recommendation_Report',
    pageStyle: `
      @page { 
        size: A4;
        margin: 1cm;
      }
      @media print {
        body { 
          -webkit-print-color-adjust: exact !important;
          print-color-adjust: exact !important;
        }
        .no-print { 
          display: none !important; 
        }
        .result-card {
          break-inside: avoid;
          page-break-inside: avoid;
        }
      }
    `
  });

  if (loading) {
    return (
      <div className="results-container">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <h3>Generating your recommendations...</h3>
        </div>
      </div>
    );
  }

  if (!recommendations) {
    return (
      <div className="results-container">
        <div className="error-state">
          <h3>Unable to load recommendations</h3>
          <p>Please try again later or contact support if the issue persists.</p>
        </div>
      </div>
    );
  }

  const handleScheduleFollowUp = () => {
    alert('Feature coming soon: This will allow you to schedule a follow-up appointment with a healthcare provider.');
  };

  const handleShareWithDoctor = () => {
    if (navigator.share) {
      navigator.share({
        title: 'My Health Recommendations',
        text: 'Here are my health recommendations from the health assessment.',
        url: window.location.href,
      }).catch(console.error);
    } else {
      // Fallback for browsers that don't support Web Share API
      alert('Please use the share button in your browser or copy this page URL to share with your doctor.');
    }
  };

  return (
    <div className={`results-container ${isDarkMode ? 'dark-mode' : ''}`} ref={ref}>
      <div className="results-content" ref={printRef}>
        <div className="no-print" style={{ marginBottom: '20px' }}>
          <h2 className={`section-title ${isDarkMode ? 'dark-mode-text' : ''}`}>Your Health Assessment Results</h2>
          <p className={`results-subtitle ${isDarkMode ? 'dark-mode-text' : ''}`}>Generated on {new Date().toLocaleDateString()}</p>
        </div>
        <div className="results-header">
          <div className="header-content">
            <h1 className={`dark-mode-text ${isDarkMode ? 'dark-mode-text' : ''}`}>Your Personalized Health Report</h1>
            <p className={`subtitle ${isDarkMode ? 'dark-mode-text' : ''}`}>Based on your assessment on {new Date().toLocaleDateString()}</p>
          </div>
          <div className="patient-summary">
            <div className="patient-details">
              <div className="detail-item">
                <FaUser className="detail-icon" />
                <div>
                  <div className={`detail-label ${isDarkMode ? 'dark-mode-text' : ''}`}>Age</div>
                  <div className={`detail-value ${isDarkMode ? 'dark-mode-text' : ''}`}>{assessmentData?.age || 'N/A'} years</div>
                </div>
              </div>
              <div className="detail-item">
                <FaVenusMars className="detail-icon" />
                <div>
                  <div className={`detail-label ${isDarkMode ? 'dark-mode-text' : ''}`}>Gender</div>
                  <div className={`detail-value ${isDarkMode ? 'dark-mode-text' : ''}`}>{assessmentData?.gender ? assessmentData.gender.charAt(0).toUpperCase() + assessmentData.gender.slice(1) : 'N/A'}</div>
                </div>
              </div>
              {assessmentData?.weight && assessmentData?.height && (
                <div className="detail-item">
                  <FaWeight className="detail-icon" />
                  <div>
                    <div className={`detail-label ${isDarkMode ? 'dark-mode-text' : ''}`}>Weight</div>
                    <div className={`detail-value ${isDarkMode ? 'dark-mode-text' : ''}`}>{assessmentData.weight} kg</div>
                  </div>
                </div>
              )}
              {assessmentData?.height && (
                <div className="detail-item">
                  <FaRuler className="detail-icon" />
                  <div>
                    <div className={`detail-label ${isDarkMode ? 'dark-mode-text' : ''}`}>Height</div>
                    <div className={`detail-value ${isDarkMode ? 'dark-mode-text' : ''}`}>{assessmentData.height} cm</div>
                  </div>
                </div>
              )}
              {assessmentData?.weight && assessmentData?.height && (
                <div className="detail-item">
                  <FaHeartbeat className="detail-icon" />
                  <div>
                    <div className={`detail-label ${isDarkMode ? 'dark-mode-text' : ''}`}>BMI</div>
                    <div className={`detail-value ${isDarkMode ? 'dark-mode-text' : ''}`}>
                      {(assessmentData.weight / ((assessmentData.height / 100) ** 2)).toFixed(1)}
                      <span className="bmi-category">
                        {(() => {
                          const bmi = assessmentData.weight / ((assessmentData.height / 100) ** 2);
                          if (bmi < 18.5) return ' (Underweight)';
                          if (bmi < 25) return ' (Normal)';
                          if (bmi < 30) return ' (Overweight)';
                          return ' (Obese)';
                        })()}
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
        
        <div className="medical-disclaimer">
          <div className="disclaimer-icon">ℹ️</div>
          <div className={`disclaimer-text ${isDarkMode ? 'dark-mode-text' : ''}`}>
            <strong>Medical Disclaimer:</strong> These recommendations are for informational purposes only and not a substitute for professional medical advice. 
            Always consult with a qualified healthcare provider before making any health-related decisions.
          </div>
        </div>
      
        <div className="results-grid">
          {/* Diagnosis Section */}
          <div className="result-card">
            <div className="card-header">
              <div className="card-icon">
                <FaHeartbeat />
              </div>
              <h3 className={`card-title ${isDarkMode ? 'dark-mode-text' : ''}`}>Assessment Summary</h3>
            </div>
            <div className="card-content">
              <div className="diagnosis-section">
                <h4 className={`card-subtitle ${isDarkMode ? 'dark-mode-text' : ''}`}>Primary Concern</h4>
                <p className={`diagnosis-text ${isDarkMode ? 'dark-mode-text' : ''}`}>
                  {recommendations.diagnosis?.condition || 'No specific diagnosis available'}
                </p>
                {recommendations.diagnosis?.severity && (
                  <p className={`severity ${recommendations.diagnosis.severity.toLowerCase()}`}>
                    Severity: {recommendations.diagnosis.severity}
                  </p>
                )}
                {recommendations.diagnosis?.notes && (
                  <p className={`diagnosis-notes ${isDarkMode ? 'dark-mode-text' : ''}`}>
                    {recommendations.diagnosis.notes}
                  </p>
                )}
                
                <div className="symptoms-list">
                  <h4 className={`card-subtitle ${isDarkMode ? 'dark-mode-text' : ''}`}>Reported Symptoms</h4>
                  <div className="symptoms-tags">
                    {assessmentData?.symptoms?.length > 0 ? (
                      assessmentData.symptoms.map((symptom, index) => (
                        <span key={index} className={`symptom-tag ${isDarkMode ? 'dark-mode-text' : ''}`}>{symptom}</span>
                      ))
                    ) : (
                      <p className={`no-data ${isDarkMode ? 'dark-mode-text' : ''}`}>No specific symptoms reported</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Medications Section */}
          <div className="result-card">
            <div className="card-header">
              <div className="card-icon">
                <FaPills />
              </div>
              <h3 className={`card-title ${isDarkMode ? 'dark-mode-text' : ''}`}>Medication Recommendations</h3>
            </div>
            <div className="card-content">
              <div className="section-notice warning">
                <div className="notice-icon">⚠️</div>
                <div className={`notice-content ${isDarkMode ? 'dark-mode-text' : ''}`}>
                  <strong>Important Safety Information:</strong> These are general recommendations only. 
                  Always consult with your healthcare provider before starting any new medications.
                </div>
              </div>
              <div className="medications-grid">
                {Array.isArray(recommendations?.medications) && recommendations.medications.length > 0 ? (
                  recommendations.medications.map((med, index) => (
                    <div key={index} className="medication-card">
                      <h4 className={`medication-name ${isDarkMode ? 'dark-mode-text' : ''}`}>{med.name}</h4>
                      <div className="medication-details">
                        <div className="detail-row">
                          <span className={`detail-label ${isDarkMode ? 'dark-mode-text' : ''}`}>Dosage:</span>
                          <span className={`detail-value ${isDarkMode ? 'dark-mode-text' : ''}`}>{med.dosage}</span>
                        </div>
                        <div className="detail-row">
                          <span className={`detail-label ${isDarkMode ? 'dark-mode-text' : ''}`}>Purpose:</span>
                          <span className={`detail-value ${isDarkMode ? 'dark-mode-text' : ''}`}>{med.purpose}</span>
                        </div>
                        <div className="detail-row warning">
                          <span className={`detail-label ${isDarkMode ? 'dark-mode-text' : ''}`}>Note:</span>
                          <span className={`detail-value ${isDarkMode ? 'dark-mode-text' : ''}`}>{med.warning}</span>
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className={`no-data ${isDarkMode ? 'dark-mode-text' : ''}`}>No medication recommendations available</p>
                )}
              </div>
            </div>
          </div>
          
          {/* Diet Plan Section */}
          <div className="result-card fade-in">
            <div className="card-header">
              <h3 className={`card-title ${isDarkMode ? 'dark-mode-text' : ''}`}>🥗 Recommended Diet Plan</h3>
            </div>
            <div className="card-content">
              <div className="diet-plan">
                <div className="meal-section">
                  <h4 className={`card-subtitle ${isDarkMode ? 'dark-mode-text' : ''}`}>🌅 Breakfast</h4>
                  <ul>
                    {Array.isArray(recommendations?.diet?.breakfast) && recommendations.diet.breakfast.length > 0 ? (
                      recommendations.diet.breakfast.map((item, index) => (
                        <li key={index} className={`diet-item ${isDarkMode ? 'dark-mode-text' : ''}`}>{item}</li>
                      ))
                    ) : (
                      <li className={`diet-item ${isDarkMode ? 'dark-mode-text' : ''}`}>No specific breakfast recommendations available</li>
                    )}
                  </ul>
                </div>
                
                <div className="meal-section">
                  <h4 className={`card-subtitle ${isDarkMode ? 'dark-mode-text' : ''}`}>🌞 Lunch</h4>
                  <ul>
                    {Array.isArray(recommendations?.diet?.lunch) && recommendations.diet.lunch.length > 0 ? (
                      recommendations.diet.lunch.map((item, index) => (
                        <li key={index} className={`diet-item ${isDarkMode ? 'dark-mode-text' : ''}`}>{item}</li>
                      ))
                    ) : (
                      <li className={`diet-item ${isDarkMode ? 'dark-mode-text' : ''}`}>No specific lunch recommendations available</li>
                    )}
                  </ul>
                </div>
                
                <div className="meal-section">
                  <h4 className={`card-subtitle ${isDarkMode ? 'dark-mode-text' : ''}`}>🌙 Dinner</h4>
                  <ul>
                    {Array.isArray(recommendations?.diet?.dinner) && recommendations.diet.dinner.length > 0 ? (
                      recommendations.diet.dinner.map((item, index) => (
                        <li key={index} className={`diet-item ${isDarkMode ? 'dark-mode-text' : ''}`}>{item}</li>
                      ))
                    ) : (
                      <li className={`diet-item ${isDarkMode ? 'dark-mode-text' : ''}`}>No specific dinner recommendations available</li>
                    )}
                  </ul>
                </div>
                
                <div className="meal-section">
                  <h4 className={`card-subtitle ${isDarkMode ? 'dark-mode-text' : ''}`}>🍎 Snacks</h4>
                  <ul>
                    {Array.isArray(recommendations?.diet?.snacks) && recommendations.diet.snacks.length > 0 ? (
                      recommendations.diet.snacks.map((item, index) => (
                        <li key={index} className={`diet-item ${isDarkMode ? 'dark-mode-text' : ''}`}>{item}</li>
                      ))
                    ) : (
                      <li className={`diet-item ${isDarkMode ? 'dark-mode-text' : ''}`}>No specific snack recommendations available</li>
                    )}
                  </ul>
                </div>
              </div>
            </div>
          </div>
          
          {/* Fitness Plan Section */}
          <div className="result-card fade-in">
            <div className="card-header">
              <h3 className={`card-title ${isDarkMode ? 'dark-mode-text' : ''}`}>💪 Fitness Recommendations</h3>
            </div>
            <div className="card-content">
              <div className="fitness-plan">
                <div className="fitness-section">
                  <h4 className={`card-subtitle ${isDarkMode ? 'dark-mode-text' : ''}`}>🏃 Cardiovascular</h4>
                  <ul>
                    {Array.isArray(recommendations?.fitness?.cardio) && recommendations.fitness.cardio.length > 0 ? (
                      recommendations.fitness.cardio.map((item, index) => (
                        <li key={index} className={`fitness-item ${isDarkMode ? 'dark-mode-text' : ''}`}>{item}</li>
                      ))
                    ) : (
                      <li className={`fitness-item ${isDarkMode ? 'dark-mode-text' : ''}`}>No specific cardiovascular recommendations available</li>
                    )}
                  </ul>
                </div>
                
                <div className="fitness-section">
                  <h4 className={`card-subtitle ${isDarkMode ? 'dark-mode-text' : ''}`}>🏋️ Strength Training</h4>
                  <ul>
                    {Array.isArray(recommendations?.fitness?.strength) && recommendations.fitness.strength.length > 0 ? (
                      recommendations.fitness.strength.map((item, index) => (
                        <li key={index} className={`fitness-item ${isDarkMode ? 'dark-mode-text' : ''}`}>{item}</li>
                      ))
                    ) : (
                      <li className={`fitness-item ${isDarkMode ? 'dark-mode-text' : ''}`}>No specific strength training recommendations available</li>
                    )}
                  </ul>
                </div>
                
                <div className="fitness-section">
                  <h4 className={`card-subtitle ${isDarkMode ? 'dark-mode-text' : ''}`}>🧘 Flexibility</h4>
                  <ul>
                    {Array.isArray(recommendations?.fitness?.flexibility) && recommendations.fitness.flexibility.length > 0 ? (
                      recommendations.fitness.flexibility.map((item, index) => (
                        <li key={index} className={`fitness-item ${isDarkMode ? 'dark-mode-text' : ''}`}>{item}</li>
                      ))
                    ) : (
                      <li className={`fitness-item ${isDarkMode ? 'dark-mode-text' : ''}`}>No specific flexibility recommendations available</li>
                    )}
                  </ul>
                </div>
                
                <div className="fitness-section">
                  <h4 className={`card-subtitle ${isDarkMode ? 'dark-mode-text' : ''}`}>😴 Rest & Recovery</h4>
                  <ul>
                    {Array.isArray(recommendations?.fitness?.rest) && recommendations.fitness.rest.length > 0 ? (
                      recommendations.fitness.rest.map((item, index) => (
                        <li key={index} className={`fitness-item ${isDarkMode ? 'dark-mode-text' : ''}`}>{item}</li>
                      ))
                    ) : (
                      <li className={`fitness-item ${isDarkMode ? 'dark-mode-text' : ''}`}>No specific rest and recovery recommendations available</li>
                    )}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {isClient && (
          <div className="action-buttons no-print">
            <button onClick={handlePrint} className="action-btn print-btn">
              <FaPrint /> Print Report
            </button>
            <button onClick={handleScheduleFollowUp} className="action-btn schedule-btn">
              <FaCalendarAlt /> Schedule Follow-up
            </button>
            {navigator.share ? (
              <button onClick={handleShareWithDoctor} className="action-btn share-btn">
                <FaShare /> Share with Doctor
              </button>
            ) : (
              <button 
                onClick={() => alert('Please use your browser\'s share functionality or copy this page URL.')} 
                className="action-btn share-btn"
              >
                <FaShare /> Share with Doctor
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
});

export default Results;