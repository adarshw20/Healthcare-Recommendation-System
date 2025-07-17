from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
import datetime

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Health conditions with detailed diagnosis and recommendations
HEALTH_CONDITIONS = {
    'fever_headache': {
        'diagnosis': 'Viral Upper Respiratory Infection (Common Cold) or Influenza',
        'severity': 'Mild to Moderate',
        'description': 'Viral infection affecting the upper respiratory tract, often accompanied by systemic symptoms',
        'symptoms': ['fever', 'headache', 'body_aches', 'fatigue', 'sore_throat', 'nasal_congestion'],
        'possible_causes': [
            'Rhinovirus (most common)',
            'Influenza virus',
            'Coronavirus',
            'Adenovirus'
        ],
        'recommended_tests': [
            'Rapid Influenza Test (if within 48 hours of symptom onset)',
            'COVID-19 test',
            'Complete Blood Count (CBC) if symptoms persist',
            'Throat culture if strep throat is suspected'
        ],
        'urgency': 'Low to Medium (Seek care if symptoms worsen or persist > 3 days)',
        'self_care': [
            'Rest and adequate hydration',
            'Over-the-counter fever reducers',
            'Saline nasal spray',
            'Warm salt water gargles'
        ],
        'when_to_seek_help': [
            'Difficulty breathing or shortness of breath',
            'Persistent fever > 38.9°C (102°F) for more than 3 days',
            'Severe headache or neck stiffness',
            'Confusion or difficulty waking up',
            'Chest pain or pressure'
        ],
        'medications': [
            {
                'name': 'Paracetamol (Acetaminophen)',
                'dosage': '500-1000mg every 6 hours as needed',
                'max_daily': '4000mg',
                'purpose': 'Fever reduction and pain relief',
                'warning': 'Do not exceed maximum daily dose. Avoid in liver disease.'
            },
            {
                'name': 'Ibuprofen',
                'dosage': '200-400mg every 6-8 hours as needed',
                'max_daily': '1200mg',
                'purpose': 'Anti-inflammatory, fever and pain relief',
                'warning': 'Take with food. Avoid if history of stomach ulcers or kidney disease.'
            },
            {
                'name': 'Pseudoephedrine (decongestant)',
                'dosage': '30-60mg every 4-6 hours',
                'max_daily': '240mg',
                'purpose': 'Nasal congestion relief',
                'warning': 'Not recommended for patients with high blood pressure or heart conditions.'
            }
        ]
    },
    'cough_fatigue': {
        'diagnosis': 'Acute Bronchitis or Viral Respiratory Infection',
        'severity': 'Mild to Moderate',
        'description': 'Inflammation of the bronchial tubes causing cough, often following a cold or flu',
        'symptoms': ['cough', 'fatigue', 'chest_discomfort', 'slight_fever', 'sore_throat'],
        'possible_causes': [
            'Viral infection (90% of cases)',
            'Bacterial infection (less common)',
            'Environmental irritants',
            'Postnasal drip from allergies or cold'
        ],
        'recommended_tests': [
            'Chest X-ray if pneumonia is suspected',
            'Sputum culture if bacterial infection is suspected',
            'Pulse oximetry if breathing difficulties are present',
            'COVID-19 test'
        ],
        'urgency': 'Low (unless severe symptoms develop)',
        'self_care': [
            'Increase fluid intake',
            'Use a humidifier',
            'Honey (1-2 teaspoons) for cough relief',
            'Throat lozenges for throat irritation'
        ],
        'when_to_seek_help': [
            'Cough lasting more than 3 weeks',
            'High fever (>38.9°C or 102°F)',
            'Coughing up blood',
            'Wheezing or difficulty breathing',
            'Chest pain with breathing'
        ],
        'medications': [
            {
                'name': 'Dextromethorphan',
                'dosage': '10-20mg every 4 hours',
                'max_daily': '120mg',
                'purpose': 'Cough suppressant',
                'warning': 'Avoid with MAO inhibitors. May cause drowsiness.'
            },
            {
                'name': 'Guaifenesin',
                'dosage': '200-400mg every 4 hours',
                'max_daily': '2400mg',
                'purpose': 'Expectorant to loosen mucus',
                'warning': 'Drink plenty of fluids with this medication.'
            }
        ]
    },
    'gastroenteritis': {
        'diagnosis': 'Acute Viral Gastroenteritis',
        'severity': 'Mild to Severe',
        'description': 'Inflammation of the stomach and intestines causing diarrhea and vomiting',
        'symptoms': ['nausea', 'vomiting', 'diarrhea', 'abdominal_cramps', 'fever'],
        'possible_causes': [
            'Norovirus (most common)',
            'Rotavirus (in children)',
            'Food poisoning',
            'Bacterial infections (E. coli, Salmonella)'
        ],
        'recommended_tests': [
            'Stool culture if symptoms are severe or persistent',
            'Blood tests for electrolyte imbalance in severe cases',
            'Rapid antigen tests for specific pathogens'
        ],
        'urgency': 'Medium (Seek care if signs of dehydration or blood in stool)',
        'self_care': [
            'Oral rehydration solutions',
            'BRAT diet (Bananas, Rice, Applesauce, Toast)',
            'Small, frequent sips of clear fluids',
            'Avoid dairy, caffeine, and fatty foods'
        ],
        'when_to_seek_help': [
            'Signs of dehydration (dry mouth, dizziness, dark urine)',
            'Blood in vomit or stool',
            'Severe abdominal pain',
            'Fever > 38.9°C (102°F)',
            'Symptoms persisting > 2 days'
        ],
        'medications': [
            {
                'name': 'Loperamide',
                'dosage': '4mg initially, then 2mg after each loose stool',
                'max_daily': '16mg',
                'purpose': 'Anti-diarrheal',
                'warning': 'Not recommended for children under 12 or if fever or bloody diarrhea is present.'
            },
            {
                'name': 'Oral Rehydration Salts (ORS)',
                'dosage': 'As directed on package',
                'purpose': 'Prevent dehydration',
                'warning': 'Continue breastfeeding for infants.'
            }
        ]
    },
    'migraine': {
        'diagnosis': 'Migraine Headache',
        'severity': 'Moderate to Severe',
        'description': 'Recurrent headache disorder manifesting as moderate to severe headaches, often accompanied by nausea and light/sound sensitivity',
        'symptoms': ['severe_headache', 'nausea', 'vomiting', 'light_sensitivity', 'sound_sensitivity', 'aura'],
        'possible_causes': [
            'Genetic predisposition',
            'Hormonal changes',
            'Certain foods or food additives',
            'Stress and sleep disturbances',
            'Environmental factors (weather changes, strong smells)'
        ],
        'recommended_tests': [
            'Neurological examination',
            'MRI or CT scan if first severe headache or unusual symptoms',
            'Blood tests to rule out other conditions'
        ],
        'urgency': 'Medium (Seek immediate care for "worst headache of life" or neurological symptoms)',
        'self_care': [
            'Rest in a quiet, dark room',
            'Cold compress on forehead or neck',
            'Hydration',
            'Caffeine in small amounts (may help some people)'
        ],
        'when_to_seek_help': [
            'Sudden, severe headache ("thunderclap headache")',
            'Headache after head injury',
            'Fever, stiff neck, confusion, or seizures',
            'Weakness, numbness, or trouble speaking',
            'Headache that worsens over days or changes pattern'
        ],
        'medications': [
            {
                'name': 'Ibuprofen',
                'dosage': '400-600mg at onset',
                'max_daily': '1200mg',
                'purpose': 'Pain relief for mild migraines',
                'warning': 'Take with food. Avoid if history of stomach ulcers.'
            },
            {
                'name': 'Sumatriptan (prescription)',
                'dosage': '25-100mg at onset',
                'max_daily': '200mg',
                'purpose': 'Migraine-specific medication',
                'warning': 'Not for patients with heart disease or uncontrolled hypertension.'
            },
            {
                'name': 'Ondansetron (prescription)',
                'dosage': '4-8mg as needed',
                'max_daily': '24mg',
                'purpose': 'For nausea and vomiting',
                'warning': 'May cause drowsiness or headache.'
            }
        ]
    },
    'general': {
        'diagnosis': 'General Wellness Assessment',
        'severity': 'N/A',
        'description': 'Routine health assessment with no acute symptoms reported',
        'recommendations': [
            'Annual physical examination',
            'Routine blood work as per age and risk factors',
            'Dental check-up every 6 months',
            'Eye examination every 1-2 years',
            'Age-appropriate cancer screenings',
            'Vaccinations up to date'
        ],
        'medications': [
            {
                'name': 'Multivitamin',
                'dosage': 'As directed on label',
                'purpose': 'Nutritional support',
                'warning': 'Not a substitute for a balanced diet.'
            },
            {
                'name': 'Vitamin D',
                'dosage': '1000-2000 IU daily',
                'purpose': 'Bone health and immune function',
                'warning': 'Consult doctor for higher doses.'
            }
        ]
    }
}

def analyze_symptoms(symptoms):
    """Analyze symptoms and return appropriate condition key with severity assessment"""
    if not symptoms:
        return 'general'
        
    symptoms_lower = [s.lower().replace(' ', '_') for s in symptoms]
    symptom_count = len(symptoms_lower)
    
    # Check for migraine pattern
    migraine_symptoms = {'severe_headache', 'nausea', 'vomiting', 'light_sensitivity', 'sound_sensitivity', 'aura'}
    if len(set(symptoms_lower) & migraine_symptoms) >= 3:
        return 'migraine'
    
    # Check for gastroenteritis
    gi_symptoms = {'nausea', 'vomiting', 'diarrhea', 'abdominal_cramps', 'fever'}
    if len(set(symptoms_lower) & gi_symptoms) >= 3:
        return 'gastroenteritis'
    
    # Check for fever-related conditions
    if 'fever' in symptoms_lower:
        if 'headache' in symptoms_lower or 'body_aches' in symptoms_lower:
            return 'fever_headache'
    
    # Check for respiratory conditions
    respiratory_symptoms = {'cough', 'fatigue', 'shortness_of_breath', 'chest_discomfort', 'sore_throat'}
    if len(set(symptoms_lower) & respiratory_symptoms) >= 2:
        return 'cough_fatigue'
    
    # If no specific pattern matches
    return 'general'

def generate_diet_plan(age, weight, height, lifestyle):
    """Generate personalized diet plan based on user data"""
    bmi = weight / ((height / 100) ** 2)
    
    if bmi < 18.5:
        # Underweight
        return {
            'breakfast': ['Oatmeal with nuts and honey', 'Banana smoothie with protein powder', 'Whole grain toast with avocado'],
            'lunch': ['Grilled chicken with quinoa', 'Mixed vegetables', 'Brown rice with lentils'],
            'dinner': ['Salmon with sweet potato', 'Steamed broccoli', 'Greek yogurt with berries'],
            'snacks': ['Protein bars', 'Mixed nuts', 'Greek yogurt', 'Fresh fruits']
        }
    elif bmi > 25:
        # Overweight
        return {
            'breakfast': ['Greek yogurt with berries', 'Green smoothie', 'Whole grain cereal'],
            'lunch': ['Grilled chicken salad', 'Quinoa bowl with vegetables', 'Lentil soup'],
            'dinner': ['Grilled fish with vegetables', 'Cauliflower rice', 'Herbal tea'],
            'snacks': ['Apple slices', 'Almonds', 'Carrot sticks', 'Herbal tea']
        }
    else:
        # Normal weight
        return {
            'breakfast': ['Oatmeal with fruits', 'Green tea', 'Whole grain toast'],
            'lunch': ['Grilled chicken salad', 'Brown rice', 'Seasonal vegetables'],
            'dinner': ['Fish with quinoa', 'Steamed vegetables', 'Herbal tea'],
            'snacks': ['Greek yogurt', 'Fruits', 'Nuts', 'Green tea']
        }

def generate_fitness_plan(age, lifestyle):
    """Generate personalized fitness plan"""
    exercise_level = lifestyle.get('exercise', 'rarely')
    
    if exercise_level in ['never', 'rarely']:
        return {
            'cardio': ['15-minute daily walks', 'Light swimming 2x/week', 'Stretching routine'],
            'strength': ['Bodyweight exercises 2x/week', 'Light resistance bands', 'Wall push-ups'],
            'flexibility': ['10-minute daily stretching', 'Basic yoga poses', 'Neck and shoulder rolls'],
            'rest': ['8 hours sleep', '2 rest days per week', 'Stress management']
        }
    elif exercise_level == 'sometimes':
        return {
            'cardio': ['30-minute walks daily', 'Swimming 3x/week', 'Cycling 2x/week'],
            'strength': ['Bodyweight exercises 3x/week', 'Resistance training 2x/week', 'Core strengthening'],
            'flexibility': ['15-minute yoga daily', 'Full body stretching', 'Foam rolling'],
            'rest': ['7-8 hours sleep', '1-2 rest days per week', 'Active recovery']
        }
    else:
        return {
            'cardio': ['45-minute runs 3x/week', 'HIIT training 2x/week', 'Swimming'],
            'strength': ['Weight training 4x/week', 'Compound movements', 'Progressive overload'],
            'flexibility': ['20-minute yoga daily', 'Dynamic stretching', 'Mobility work'],
            'rest': ['7-8 hours sleep', '1 rest day per week', 'Recovery techniques']
        }

@app.route('/api/health-assessment', methods=['POST'])
def health_assessment():
    try:
        data = request.get_json()
        
        # Extract user data with validation
        age = max(0, min(120, int(data.get('age', 25))))  # Clamp age between 0-120
        weight = max(0, min(300, float(data.get('weight', 70))))  # Clamp weight between 0-300kg
        height = max(50, min(250, float(data.get('height', 170))))  # Clamp height between 50-250cm
        symptoms = [s.strip() for s in data.get('symptoms', []) if s.strip()]  # Clean symptoms
        lifestyle = data.get('lifestyle', {})
        
        # Analyze symptoms and get condition data
        condition_key = analyze_symptoms(symptoms)
        condition_data = HEALTH_CONDITIONS.get(condition_key, HEALTH_CONDITIONS['general'])
        
        # Calculate BMI and category
        bmi = round(weight / ((height / 100) ** 2), 1)
        bmi_category = (
            'Underweight' if bmi < 18.5 else
            'Normal weight' if bmi < 25 else
            'Overweight' if bmi < 30 else
            'Obese (Class I)' if bmi < 35 else
            'Obese (Class II)' if bmi < 40 else
            'Obese (Class III)'
        )
        
        # Generate comprehensive response
        response = {
            'assessment_summary': {
                'primary_diagnosis': condition_data['diagnosis'],
                'severity': condition_data.get('severity', 'Not Specified'),
                'condition_description': condition_data.get('description', ''),
                'identified_symptoms': symptoms,
                'urgency_level': condition_data.get('urgency', 'Low')
            },
            'clinical_information': {
                'possible_causes': condition_data.get('possible_causes', []),
                'differential_diagnosis': get_differential_diagnosis(condition_key, symptoms),
                'recommended_tests': condition_data.get('recommended_tests', []),
                'red_flags': condition_data.get('when_to_seek_help', [])
            },
            'treatment_plan': {
                'medications': condition_data.get('medications', []),
                'self_care': condition_data.get('self_care', []),
                'follow_up_instructions': get_follow_up_instructions(condition_key, age, symptoms)
            },
            'preventive_care': {
                'lifestyle_recommendations': get_lifestyle_recommendations(lifestyle),
                'preventive_measures': get_preventive_measures(condition_key)
            },
            'health_metrics': {
                'bmi': bmi,
                'bmi_category': bmi_category,
                'risk_factors': analyze_risk_factors(data),
                'vital_signs_interpretation': interpret_vital_signs(data.get('vital_signs', {}))
            },
            'additional_resources': [
                'Patient education materials',
                'Local healthcare providers',
                'Support groups if applicable',
                'Emergency contact information'
            ]
        }
        
        # Add metadata and return response
        response['metadata'] = {
            'assessment_timestamp': datetime.datetime.now().isoformat(),
            'symptoms_analyzed': len(symptoms),
            'condition_confidence': 'high' if len(symptoms) > 2 else 'medium' if symptoms else 'low'
        }
        
        logger.info(f"Comprehensive health assessment completed for {age}y/o with {len(symptoms)} symptoms")
        
        return jsonify({
            'success': True,
            'assessment': response,
            'diet': generate_diet_plan(age, weight, height, lifestyle),
            'fitness': generate_fitness_plan(age, lifestyle)
        })
    
    except Exception as e:
        logger.error(f"Error in health assessment: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your assessment'
        }), 500

def get_differential_diagnosis(condition_key, symptoms):
    """Generate a list of possible alternative diagnoses to consider"""
    differentials = {
        'fever_headache': [
            'Influenza (Flu)',
            'Common Cold',
            'COVID-19',
            'Sinusitis',
            'Meningitis (if severe headache and neck stiffness)',
            'Mononucleosis (in adolescents/young adults)'
        ],
        'cough_fatigue': [
            'Acute Bronchitis',
            'Pneumonia',
            'Asthma exacerbation',
            'Chronic Obstructive Pulmonary Disease (COPD)',
            'Postnasal Drip Syndrome',
            'Gastroesophageal Reflux Disease (GERD)'
        ],
        'gastroenteritis': [
            'Food Poisoning',
            'Inflammatory Bowel Disease flare',
            'Appendicitis (if severe abdominal pain)',
            'Diverticulitis',
            'Bowel Obstruction',
            'Gastroparesis'
        ],
        'migraine': [
            'Tension Headache',
            'Cluster Headache',
            'Sinus Headache',
            'Medication Overuse Headache',
            'Temporal Arteritis (in patients > 50 years)',
            'Intracranial Hemorrhage (if sudden onset)'
        ]
    }
    return differentials.get(condition_key, ['No specific differentials available'])

def get_follow_up_instructions(condition_key, age, symptoms):
    """Generate appropriate follow-up instructions based on condition and age"""
    base_instructions = [
        "Return immediately if symptoms worsen or new symptoms develop",
        "Follow up with primary care physician if symptoms persist beyond expected duration"
    ]
    
    condition_specific = {
        'fever_headache': [
            "Return if fever > 38.9°C (102°F) persists > 3 days",
            "Seek care for severe headache, confusion, or neck stiffness"
        ],
        'cough_fatigue': [
            "Follow up if cough persists > 3 weeks",
            "Seek care for difficulty breathing or chest pain"
        ],
        'gastroenteritis': [
            "Follow up if symptoms persist > 2 days",
            "Seek care for signs of dehydration or blood in stool"
        ],
        'migraine': [
            "Follow up with neurologist if migraines are frequent or severe",
            "Keep a headache diary to identify triggers"
        ]
    }
    
    age_based = []
    if age < 2:
        age_based.append("Pediatric follow-up recommended within 24-48 hours")
    elif age > 65:
        age_based.append("Geriatric follow-up recommended due to increased risk of complications")
    
    return base_instructions + condition_specific.get(condition_key, []) + age_based

def get_lifestyle_recommendations(lifestyle):
    """Generate personalized lifestyle recommendations"""
    recommendations = []
    
    # Exercise recommendations
    exercise = lifestyle.get('exercise', 'sometimes')
    if exercise in ['never', 'rarely']:
        recommendations.append(
            "Start with light exercise (e.g., 15-minute walks) and gradually increase"
        )
    
    # Sleep recommendations
    sleep = lifestyle.get('sleep', '7-9')
    if sleep == 'less than 6':
        recommendations.append(
            "Aim for 7-9 hours of sleep per night for optimal health"
        )
    
    # Diet recommendations
    diet = lifestyle.get('diet', 'mixed')
    if diet == 'unhealthy':
        recommendations.append(
            "Incorporate more fruits, vegetables, and whole grains into your diet"
        )
    
    # Stress management
    if lifestyle.get('stress_level') in ['high', 'very high']:
        recommendations.extend([
            "Practice stress-reduction techniques (e.g., meditation, deep breathing)",
            "Consider counseling or therapy for stress management"
        ])
    
    # Smoking and alcohol
    if lifestyle.get('smoking'):
        recommendations.append(
            "Consider smoking cessation programs to reduce health risks"
        )
    if lifestyle.get('alcohol') in ['moderate', 'heavy']:
        recommendations.append(
            "Limit alcohol consumption to recommended guidelines"
        )
    
    return recommendations if recommendations else ["No specific lifestyle changes recommended at this time."]

def get_preventive_measures(condition_key):
    """Provide preventive measures for specific conditions"""
    measures = {
        'fever_headache': [
            "Annual flu vaccination",
            "Frequent hand washing",
            "Avoid close contact with sick individuals",
            "Stay home when feeling unwell"
        ],
        'cough_fatigue': [
            "Annual flu shot",
            "Pneumonia vaccine if eligible",
            "Avoid smoking and secondhand smoke",
            "Use a humidifier in dry environments"
        ],
        'gastroenteritis': [
            "Frequent hand washing, especially before eating",
            "Proper food handling and preparation",
            "Avoid undercooked foods when traveling",
            "Stay hydrated"
        ],
        'migraine': [
            "Identify and avoid personal triggers",
            "Maintain regular sleep schedule",
            "Stay hydrated and don't skip meals",
            "Consider preventive medications if migraines are frequent"
        ]
    }
    return measures.get(condition_key, [
        "Regular health check-ups",
        "Balanced diet and regular exercise",
        "Adequate sleep and stress management"
    ])

def interpret_vital_signs(vital_signs):
    """Interpret vital signs and flag any abnormalities"""
    if not vital_signs:
        return "No vital signs provided"
    
    results = []
    
    # Temperature interpretation
    if 'temperature' in vital_signs:
        temp = float(vital_signs['temperature'])
        if temp < 36.1:  # 97°F
            results.append(f"Low body temperature ({temp}°C): May indicate hypothermia or other conditions")
        elif temp > 37.2:  # 99°F
            results.append(f"Elevated temperature ({temp}°C): May indicate fever")
    
    # Heart rate interpretation
    if 'heart_rate' in vital_signs:
        hr = int(vital_signs['heart_rate'])
        if hr < 60:
            results.append(f"Low heart rate ({hr} bpm): Bradycardia")
        elif hr > 100:
            results.append(f"High heart rate ({hr} bpm): Tachycardia")
    
    # Blood pressure interpretation
    if 'blood_pressure' in vital_signs:
        try:
            systolic, diastolic = map(int, vital_signs['blood_pressure'].split('/'))
            if systolic < 90 or diastolic < 60:
                results.append(f"Low blood pressure ({systolic}/{diastolic}): Hypotension")
            elif systolic >= 140 or diastolic >= 90:
                results.append(f"High blood pressure ({systolic}/{diastolic}): Hypertension")
        except (ValueError, AttributeError):
            pass
    
    # Respiratory rate interpretation
    if 'respiratory_rate' in vital_signs:
        rr = int(vital_signs['respiratory_rate'])
        if rr < 12:
            results.append(f"Low respiratory rate ({rr} breaths/min): Bradypnea")
        elif rr > 20:
            results.append(f"High respiratory rate ({rr} breaths/min): Tachypnea")
    
    # Oxygen saturation interpretation
    if 'oxygen_saturation' in vital_signs:
        spo2 = float(vital_signs['oxygen_saturation'])
        if spo2 < 92:
            results.append(f"Low oxygen saturation ({spo2}%): Hypoxemia - seek medical attention")
    
    return results if results else "All vital signs within normal ranges"

def analyze_risk_factors(data):
    """Analyze risk factors based on user data"""
    risk_factors = []
    
    lifestyle = data.get('lifestyle', {})
    age = int(data.get('age', 25))
    
    # Basic demographics
    if age > 50:
        risk_factors.append('Age > 50: Increased risk for chronic conditions')
    
    # Lifestyle factors
    if lifestyle.get('smoking'):
        risk_factors.append('Tobacco use: Increases risk of cardiovascular, respiratory diseases, and cancer')
    
    if lifestyle.get('alcohol') in ['moderate', 'heavy']:
        risk_factors.append('Alcohol consumption: May affect liver, cardiovascular, and mental health')
    
    if lifestyle.get('exercise') in ['never', 'rarely']:
        risk_factors.append('Physical inactivity: Associated with increased risk of chronic diseases')
    
    if lifestyle.get('diet') == 'unhealthy':
        risk_factors.append('Poor diet: May contribute to obesity, diabetes, and heart disease')
    
    # Sleep patterns
    sleep = lifestyle.get('sleep', '7-9')
    if sleep == 'less than 6':
        risk_factors.append('Insufficient sleep: Associated with various health risks')
    elif sleep == 'more than 9':
        risk_factors.append('Excessive sleep: May indicate underlying health issues')
    
    # Stress levels
    if lifestyle.get('stress_level') in ['high', 'very high']:
        risk_factors.append('Chronic stress: May impact immune function and overall health')
    
    # Medical history
    medical_history = data.get('medical_history', [])
    if 'diabetes' in medical_history:
        risk_factors.append('Diabetes: Requires careful management to prevent complications')
    if 'hypertension' in medical_history:
        risk_factors.append('Hypertension: Increases cardiovascular risk')
    if 'high_cholesterol' in medical_history:
        risk_factors.append('High cholesterol: Contributes to cardiovascular disease risk')
    
    # Family history
    family_history = data.get('family_history', [])
    if 'heart_disease' in family_history:
        risk_factors.append('Family history of heart disease: Increased cardiovascular risk')
    if 'diabetes' in family_history:
        risk_factors.append('Family history of diabetes: Increased risk of developing diabetes')
    
    return risk_factors if risk_factors else ['No significant risk factors identified']

@app.route('/api/health-tips', methods=['GET'])
def health_tips():
    """Get general health tips"""
    tips = [
        "Stay hydrated by drinking at least 8 glasses of water daily",
        "Include fruits and vegetables in every meal",
        "Exercise for at least 30 minutes daily",
        "Get 7-8 hours of quality sleep",
        "Practice stress management techniques",
        "Avoid smoking and limit alcohol consumption",
        "Regular health check-ups are important",
        "Maintain a healthy weight",
        "Practice good hygiene",
        "Stay socially connected"
    ]
    
    return jsonify({
        'success': True,
        'tips': tips
    })

@app.route('/api/emergency-contacts', methods=['GET'])
def emergency_contacts():
    """Get emergency contact information"""
    contacts = {
        'emergency': '911',
        'poison_control': '1-800-222-1222',
        'mental_health': '988',
        'healthcare_provider': 'Contact your primary care physician'
    }
    
    return jsonify({
        'success': True,
        'contacts': contacts
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Healthcare AI API is running'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)