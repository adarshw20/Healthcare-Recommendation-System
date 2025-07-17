import React, { useState, useEffect, useCallback } from 'react';
import { ThemeProvider } from './contexts/ThemeContext';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import HealthAssessment from './components/HealthAssessment';
import Results from './components/Results';
import Footer from './components/Footer';
import LoadingSpinner from './components/common/LoadingSpinner';
import ErrorBoundary from './components/common/ErrorBoundary';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';

// Mock API service
const mockApiService = {
  getRecommendations: async (data) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const symptoms = data.symptoms || [];
    const age = data.age || 30;
    const bmi = data.weight && data.height 
      ? (data.weight / ((data.height / 100) ** 2)).toFixed(1)
      : 22.5; // Default normal BMI

    // Enhanced diagnosis logic
    let diagnosis = 'General wellness assessment';
    let severity = 'low';
    
    if (symptoms.includes('fever') && symptoms.includes('headache')) {
      diagnosis = 'Possible viral infection or flu-like symptoms';
      severity = 'moderate';
    }
    if ((symptoms.includes('cough') && symptoms.includes('fatigue')) || symptoms.includes('shortness of breath')) {
      diagnosis = 'Possible respiratory condition';
      severity = symptoms.includes('difficulty breathing') ? 'high' : 'moderate';
    }
    if (symptoms.includes('chest pain') || symptoms.includes('severe headache')) {
      diagnosis = 'Potentially serious condition - seek immediate medical attention';
      severity = 'high';
    }

    // Generate dynamic recommendations based on symptoms and health data
    const medications = [];
    const diet = { breakfast: [], lunch: [], dinner: [], snacks: [] };
    const fitness = { cardio: [], strength: [], flexibility: [], rest: [] };

    // Add medications based on symptoms
    if (symptoms.includes('fever') || symptoms.includes('headache')) {
      medications.push({
        name: 'Acetaminophen (Paracetamol)',
        dosage: '500-1000mg every 6 hours as needed',
        purpose: 'Pain and fever relief',
        warning: 'Do not exceed 4000mg in 24 hours. Consult doctor if symptoms persist for more than 3 days.'
      });
    }

    if (symptoms.includes('cough') && !symptoms.includes('fever')) {
      medications.push({
        name: 'Dextromethorphan',
        dosage: '10-20mg every 4-6 hours as needed',
        purpose: 'Cough suppression',
        warning: 'Not recommended for children under 4 years. Consult doctor for persistent cough.'
      });
    }

    // Add dietary recommendations
    if (bmi > 25) {
      diet.breakfast.push('Vegetable omelet with whole grain toast');
      diet.lunch.push('Grilled chicken salad with olive oil dressing');
      diet.dinner.push('Baked salmon with quinoa and steamed vegetables');
      diet.snacks.push('Greek yogurt with berries', 'Handful of mixed nuts');
      
      fitness.cardio = [
        '30-45 minutes of brisk walking daily',
        'Swimming or cycling 3-4 times per week',
        '10,000 steps per day goal'
      ];
      
      fitness.strength = [
        'Full-body strength training 2-3 times per week',
        'Focus on compound movements (squats, lunges, push-ups)'
      ];
    } else if (bmi < 18.5) {
      diet.breakfast.push('Oatmeal with banana, nuts, and honey');
      diet.lunch.push('Quinoa bowl with chicken, avocado, and mixed vegetables');
      diet.dinner.push('Brown rice with grilled fish and roasted vegetables');
      diet.snacks.push('Protein smoothie with banana and peanut butter', 'Cheese and whole grain crackers');
      
      fitness.strength = [
        'Progressive resistance training 3-4 times per week',
        'Focus on compound lifts (deadlifts, bench press, rows)'
      ];
      
      fitness.cardio = [
        '20-30 minutes of moderate cardio 2-3 times per week',
        'Focus on low-impact activities like walking or cycling'
      ];
    } else {
      // Normal BMI
      diet.breakfast.push('Greek yogurt with granola and mixed berries');
      diet.lunch.push('Grilled chicken wrap with whole wheat tortilla and vegetables');
      diet.dinner.push('Stir-fried tofu with brown rice and mixed vegetables');
      diet.snacks.push('Fruit with nut butter', 'Vegetable sticks with hummus');
      
      fitness.cardio = [
        '150 minutes of moderate aerobic activity per week',
        'Brisk walking, swimming, or cycling'
      ];
      
      fitness.strength = [
        'Strength training exercises for all major muscle groups 2+ times per week',
        'Include bodyweight exercises or resistance training'
      ];
    }

    // Add flexibility and rest recommendations
    fitness.flexibility = [
      'Daily stretching routine (10-15 minutes)',
      'Yoga or Pilates 2-3 times per week',
      'Focus on major muscle groups and problem areas'
    ];

    fitness.rest = [
      '7-9 hours of quality sleep per night',
      'Rest days between intense workouts',
      'Practice stress-reduction techniques (meditation, deep breathing)'
    ];

    // Add hydration recommendation
    diet.hydration = [
      'Drink at least 8-10 glasses of water daily',
      'Limit sugary and caffeinated beverages',
      'Increase water intake during exercise or hot weather'
    ];

    return {
      diagnosis: {
        condition: diagnosis,
        severity: severity,
        notes: severity === 'high' 
          ? 'Please consult a healthcare provider immediately.' 
          : severity === 'moderate'
            ? 'Monitor symptoms and consult a doctor if they persist or worsen.'
            : 'Maintain a healthy lifestyle and regular check-ups.'
      },
      medications,
      diet,
      fitness,
      lastUpdated: new Date().toISOString(),
      nextCheckup: severity === 'high' 
        ? 'ASAP (Within 24-48 hours)' 
        : severity === 'moderate'
          ? 'Within 1-2 weeks'
          : 'Routine check-up in 6-12 months'
    };
  }
};

function App() {
  const [currentSection, setCurrentSection] = useState('home');
  const [assessmentData, setAssessmentData] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Memoize scroll function to prevent unnecessary re-renders
  const scrollToSection = useCallback((sectionId) => {
    setCurrentSection(sectionId);
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
      });
      // Update URL without page reload
      window.history.pushState({}, '', `#${sectionId}`);
    }
  }, []);

  // Handle back/forward browser buttons
  useEffect(() => {
    document.body.classList.add('smooth-scroll');
    
    const handleHashChange = () => {
      const hash = window.location.hash.substring(1);
      if (hash) {
        scrollToSection(hash);
      }
    };
    
    window.addEventListener('popstate', handleHashChange);
    
    // Initial scroll to hash if present
    if (window.location.hash) {
      const hash = window.location.hash.substring(1);
      scrollToSection(hash);
    }
    
    return () => {
      window.removeEventListener('popstate', handleHashChange);
    };
  }, [scrollToSection]);

  const handleAssessmentSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    setAssessmentData(formData);
    
    try {
      // Show loading toast
      const toastId = toast.loading('Analyzing your health data...');
      
      // Simulate API call with mock service
      const result = await mockApiService.getRecommendations(formData);
      
      setRecommendations(result);
      setLoading(false);
      
      // Update toast to success
      toast.update(toastId, {
        render: 'Health assessment complete!',
        type: 'success',
        isLoading: false,
        autoClose: 3000,
        closeButton: true,
      });
      
      // Scroll to results after a short delay
      setTimeout(() => {
        scrollToSection('results');
      }, 500);
      
    } catch (err) {
      console.error('Error getting recommendations:', err);
      setError('Failed to generate recommendations. Please try again.');
      setLoading(false);
      
      toast.error('Failed to process your assessment. Please try again.', {
        position: 'top-center',
        autoClose: 5000,
        closeOnClick: true,
        pauseOnHover: true,
      });
    }
  };

  return (
    <ThemeProvider>
      <ErrorBoundary>
        <div className="app">
          <Navbar currentSection={currentSection} scrollToSection={scrollToSection} />
          <main>
            <Hero id="home" scrollToAssessment={() => scrollToSection('assessment')} />
            <HealthAssessment 
              id="assessment" 
              onSubmit={handleAssessmentSubmit} 
              loading={loading}
            />
            {loading && (
              <div className="loading-overlay">
                <LoadingSpinner />
                <p>Analyzing your health data...</p>
              </div>
            )}
            {error && (
              <div className="error-message">
                <p>{error}</p>
                <button 
                  className="btn btn-primary" 
                  onClick={() => window.location.reload()}
                >
                  Try Again
                </button>
              </div>
            )}
            {recommendations && (
              <Results 
                id="results" 
                data={assessmentData}
                recommendations={recommendations}
                loading={loading}
              />
            )}
          </main>
          <Footer />
          <ToastContainer 
            position="top-center"
            autoClose={5000}
            hideProgressBar={false}
            newestOnTop={false}
            closeOnClick
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover
            theme="light"
          />
        </div>
      </ErrorBoundary>
    </ThemeProvider>
  );
}

export default App;