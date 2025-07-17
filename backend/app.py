from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
import datetime
from typing import Dict, List, Optional, Any
from medical_model import MedicalDiagnosisModel

# Initialize medical model instance
medical_model = MedicalDiagnosisModel()


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization"]}}, supports_credentials=True)

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

def analyze_symptoms(symptoms: List[str], age: Optional[int] = None, gender: Optional[str] = None) -> Dict[str, Any]:
    """Analyze symptoms using the medical model"""
    if not symptoms:
        return 'general', 'low'
    
    try:
        # Get diagnosis from medical model
        diagnosis = medical_model.generate_diagnosis(
            symptoms=symptoms,
            age=age,
            gender=gender
        )
        
        return diagnosis['condition'], diagnosis['severity']
    except Exception as e:
        logger.error(f"Error analyzing symptoms: {str(e)}")
        return 'general', 'low'

def generate_diet_plan(age: int, weight: float, height: float, lifestyle: str) -> Dict[str, Any]:
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

def generate_fitness_plan(age: int, lifestyle: str) -> Dict[str, Any]:
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
        logger.info(f"Received health assessment request: {data}")
        
        # Validate request data
        if not data or not isinstance(data, dict):
            logger.error("Invalid input data format")
            return jsonify({
                'error': 'Invalid input data format',
                'details': 'Request body must be a JSON object'
            }), 400
        
        # Required fields validation
        required_fields = ['symptoms', 'age', 'gender', 'height', 'weight']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            logger.error(f"Missing required fields: {missing_fields}")
            return jsonify({
                'error': 'Missing required fields',
                'details': f"Missing fields: {', '.join(missing_fields)}"
            }), 400
        
        # Extract and validate data
        symptoms = data.get('symptoms', [])
        if not isinstance(symptoms, list) or not all(isinstance(s, str) for s in symptoms):
            logger.error("Invalid symptoms format")
            return jsonify({
                'error': 'Invalid symptoms format',
                'details': 'Symptoms must be a list of strings'
            }), 400
        
        # Convert and validate numeric values
        try:
            age = int(data.get('age', ''))
            weight = int(data.get('weight', ''))
            height = int(data.get('height', ''))
            
            if age <= 0 or weight <= 0 or height <= 0:
                raise ValueError("Numeric values must be positive")
                
        except (ValueError, TypeError) as e:
            logger.warning(f"Error converting numeric values: {str(e)}")
            return jsonify({
                'error': 'Invalid numeric values',
                'details': str(e)
            }), 400
        
        # Handle lifestyle data
        lifestyle = data.get('lifestyle', {})
        if not isinstance(lifestyle, dict):
            lifestyle = {}
            logger.warning("Lifestyle data not provided as dictionary, using default values")
        
        gender = data.get('gender', '').lower()
        if gender not in ['male', 'female', 'other']:
            gender = None
            logger.warning(f"Invalid gender value, using None")
        
        logger.info(f"Processing symptoms: {symptoms}")
        logger.info(f"User data - Age: {age}, Gender: {gender}, Weight: {weight}, Height: {height}, Lifestyle: {lifestyle}")
        
        # Generate diagnosis
        diagnosis = medical_model.generate_diagnosis(
            symptoms=symptoms,
            age=age,
            gender=gender
        )
        
        if not diagnosis:
            logger.error("Medical model returned empty diagnosis")
            return jsonify({
                'error': 'Failed to generate diagnosis',
                'details': 'Medical model returned empty response'
            }), 500
        
        # Validate diagnosis response
        required_diagnosis_fields = [
            'diagnosis', 'condition', 'condition_id', 'confidence',
            'severity', 'description', 'recommendation',
            'alternative_conditions', 'symptoms'
        ]
        missing_fields = [field for field in required_diagnosis_fields if field not in diagnosis]
        if missing_fields:
            logger.error(f"Missing fields in diagnosis: {missing_fields}")
            return jsonify({
                'error': 'Incomplete diagnosis data',
                'details': f"Missing fields: {', '.join(missing_fields)}"
            }), 500
        
        # Generate recommendations using medical_model instance
        response = {
            'timestamp': datetime.datetime.now().isoformat(),
            'success': True,
            'data': {
                **diagnosis
            }
        }

        try:
            # Try to get differential diagnosis
            try:
                differential = medical_model.get_differential_diagnosis(diagnosis['condition'], symptoms)
                response['data']['differential_diagnosis'] = differential
            except AttributeError:
                logger.warning("Differential diagnosis method not available")

            # Try to get follow-up instructions
            try:
                follow_up = medical_model.get_follow_up_instructions(diagnosis['condition'], age, symptoms)
                response['data']['follow_up_instructions'] = follow_up
            except AttributeError:
                logger.warning("Follow-up instructions method not available")

            # Try to get lifestyle recommendations
            try:
                lifestyle_rec = medical_model.get_lifestyle_recommendations(lifestyle)
                response['data']['lifestyle_recommendations'] = lifestyle_rec
            except AttributeError:
                logger.warning("Lifestyle recommendations method not available")

            # Try to get preventive measures
            try:
                preventive = medical_model.get_preventive_measures(diagnosis['condition'])
                response['data']['preventive_measures'] = preventive
            except AttributeError:
                logger.warning("Preventive measures method not available")

            # Try to get diet plan
            try:
                diet_plan = medical_model.generate_diet_plan(age, weight, height, lifestyle)
                response['data']['diet_plan'] = diet_plan
            except AttributeError:
                logger.warning("Diet plan method not available")

            # Try to get fitness plan
            try:
                fitness_plan = medical_model.generate_fitness_plan(age, lifestyle)
                response['data']['fitness_plan'] = fitness_plan
            except AttributeError:
                logger.warning("Fitness plan method not available")

            # Try to get emergency contacts
            try:
                emergency = medical_model.emergency_contacts()
                response['data']['emergency_contacts'] = emergency
            except AttributeError:
                logger.warning("Emergency contacts method not available")

            # Try to get health tips
            try:
                health_tips_list = medical_model.health_tips()
                response['data']['health_tips'] = health_tips_list
            except AttributeError:
                logger.warning("Health tips method not available")

        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}", exc_info=True)
            return jsonify({
                'error': 'Failed to generate recommendations',
                'details': str(e)
            }), 500

        logger.info("Successfully generated complete response")
        return jsonify(response)
        
    except ValueError as ve:
        logger.error(f"Value error in health assessment: {str(ve)}", exc_info=True)
        return jsonify({
            'error': 'Invalid input data',
            'details': str(ve)
        }), 400
    
    except Exception as e:
        logger.error(f"Unexpected error in health assessment: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500



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