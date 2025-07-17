import logging
import json
from typing import Dict, List, Tuple, Optional, Union
import difflib
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalDiagnosisModel:
    """A medical diagnosis model that uses string similarity to match symptoms to known conditions."""

    def __init__(self):
        """Initialize the medical diagnosis model."""
        # Core conditions database (simplified for brevity)
        self.conditions = {
            'common_cold': {
                'symptoms': ['runny nose', 'sneezing', 'sore throat', 'cough', 'congestion', 'mild headache'],
                'description': 'Viral infection of the upper respiratory tract',
                'severity': 'mild'
            },
            'influenza': {
                'symptoms': ['fever', 'cough', 'sore throat', 'muscle aches', 'headache', 'fatigue'],
                'description': 'Viral infection that attacks the respiratory system',
                'severity': 'moderate to severe'
            },
            'migraine': {
                'symptoms': ['severe headache', 'nausea', 'sensitivity to light', 'sensitivity to sound'],
                'description': 'Neurological condition characterized by intense headaches',
                'severity': 'moderate to severe'
            },
            'gastroenteritis': {
                'symptoms': ['diarrhea', 'nausea', 'vomiting', 'abdominal pain', 'fever'],
                'description': 'Inflammation of the stomach and intestines',
                'severity': 'mild to severe'
            },
            'hypertension': {
                'symptoms': ['headache', 'shortness of breath', 'nosebleeds', 'dizziness'],
                'description': 'High blood pressure',
                'severity': 'moderate to severe'
            },
            'diabetes': {
                'symptoms': ['increased thirst', 'frequent urination', 'fatigue', 'blurred vision'],
                'description': 'Metabolic disorder affecting blood sugar regulation',
                'severity': 'chronic'
            }
        }

    def get_differential_diagnosis(self, condition_key: str, symptoms: List[str]) -> List[Dict]:
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
        
        # Get the differential diagnoses for the given condition
        condition_differentials = differentials.get(condition_key, [])
        
        # Add symptom-based differentials
        symptom_differentials = []
        if 'fever' in symptoms:
            symptom_differentials.extend([
                'Infection',
                'Viral Syndrome',
                'Bacterial Infection'
            ])
        if 'headache' in symptoms:
            symptom_differentials.extend([
                'Migraine',
                'Tension Headache',
                'Cluster Headache'
            ])
        if 'nausea' in symptoms:
            symptom_differentials.extend([
                'Gastroenteritis',
                'Food Poisoning',
                'Vestibular Disorder'
            ])

        # Combine and remove duplicates
        all_differentials = list(set(condition_differentials + symptom_differentials))
        return [{
            'condition': cond,
            'similarity': 0.85 if cond in condition_differentials else 0.75,
            'description': f"Alternative diagnosis: {cond}"
        } for cond in all_differentials]

    def get_follow_up_instructions(self, condition: str, age: int, symptoms: List[str]) -> List[str]:
        """Generate follow-up instructions based on condition and patient data"""
        base_instructions = [
            "Follow up with your healthcare provider if symptoms persist or worsen",
            "Keep track of symptom patterns and triggers",
            "Maintain a symptom diary"
        ]

        condition_specific = {
            "migraine": [
                "Keep a headache diary to identify triggers",
                "Avoid known triggers like caffeine and stress"
            ],
            "tension_headache": [
                "Practice stress management techniques",
                "Regular exercise can help reduce tension"
            ]
        }

        age_based = []
        if age and age >= 65:
            age_based.append("Geriatric follow-up recommended due to increased risk of complications")

        return base_instructions + condition_specific.get(condition.lower(), []) + age_based

    def get_lifestyle_recommendations(self, lifestyle: Union[dict, str]) -> List[str]:
        """Generate personalized lifestyle recommendations"""
        recommendations = []
        
        # Handle dictionary input
        if isinstance(lifestyle, dict):
            exercise = lifestyle.get('exercise', 'sometimes')
            sleep = lifestyle.get('sleep', '7-8')
        # Handle string input (one of 'sedentary', 'moderate', 'active', 'very_active')
        elif isinstance(lifestyle, str):
            if lifestyle == 'sedentary':
                exercise = 'rarely'
                sleep = 'less than 6'
            elif lifestyle == 'moderate':
                exercise = 'sometimes'
                sleep = '6-7'
            elif lifestyle == 'active':
                exercise = 'regularly'
                sleep = '7-8'
            elif lifestyle == 'very_active':
                exercise = 'daily'
                sleep = '8-9'
            else:
                exercise = 'sometimes'
                sleep = '7-8'
        else:
            exercise = 'sometimes'
            sleep = '7-8'

        # Exercise recommendations
        if exercise in ['never', 'rarely']:
            recommendations.append(
                "Start with light exercise (e.g., 15-minute walks) and gradually increase"
            )
        elif exercise in ['sometimes', 'regularly']:
            recommendations.append(
                "Maintain your current exercise routine and consider adding variety"
            )
        elif exercise == 'daily':
            recommendations.append(
                "Great job! Keep up your active lifestyle and ensure proper rest days"
            )

        # Sleep recommendations
        if sleep == 'less than 6':
            recommendations.append(
                "Aim for 7-9 hours of sleep per night for optimal health"
            )
        elif sleep == '6-7':
            recommendations.append(
                "Try to get closer to 8 hours of sleep for better recovery"
            )
        elif sleep == '7-8':
            recommendations.append(
                "Great sleep duration! Maintain this for optimal health"
            )
        elif sleep == '8-9':
            recommendations.append(
                "Excellent sleep duration! Keep it up"
            )
        elif sleep == 'more than 9':
            recommendations.append(
                "If you feel tired, consider reducing sleep duration to 7-9 hours"
            )

        # General lifestyle tips
        recommendations.extend([
            "Maintain a balanced diet with plenty of fruits and vegetables",
            "Stay hydrated by drinking at least 8 glasses of water daily",
            "Practice stress management techniques like meditation or deep breathing",
            "Regular health check-ups are recommended"
        ])

        return recommendations

    def get_preventive_measures(self, condition: str) -> List[str]:
        """Generate preventive measures for the given condition"""
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
        return measures.get(condition, [
            "Regular health check-ups",
            "Balanced diet and regular exercise",
            "Adequate sleep and stress management"
        ])

    def emergency_contacts(self) -> List[Dict]:
        """Return emergency contact information"""
        return [
            {
                "type": "Emergency",
                "number": "911",
                "description": "For immediate medical emergencies"
            },
            {
                "type": "Poison Control",
                "number": "1-800-222-1222",
                "description": "For suspected poisoning or drug overdose"
            },
            {
                "type": "Mental Health Crisis",
                "number": "988",
                "description": "National Suicide Prevention Lifeline"
            }
        ]

    def health_tips(self) -> List[str]:
        """Return general health tips"""
        return [
            "Maintain regular exercise routine",
            "Eat a balanced diet",
            "Get adequate sleep",
            "Stay hydrated",
            "Practice stress management",
            "Regular health check-ups",
            "Wash hands frequently",
            "Maintain social connections"
        ]

    def generate_diet_plan(self, age: int, weight: float, height: float, lifestyle: Union[dict, str]) -> Dict:
        """Generate personalized diet plan based on user data"""
        bmi = weight / ((height / 100) ** 2)
        
        # Default values if lifestyle is string
        if isinstance(lifestyle, str):
            exercise = 'sometimes'
        else:
            exercise = lifestyle.get('exercise', 'sometimes')

        # Base recommendations
        recommendations = {
            'daily_calories': int(2000 + (100 if exercise in ['regularly', 'daily'] else 0)),
            'protein': '1.2-1.6g per kg body weight',
            'carbohydrates': '45-65% of daily calories',
            'fats': '20-35% of daily calories',
            'water': '8-10 glasses per day'
        }

        # Age-based recommendations
        if age < 18:
            recommendations['notes'] = 'Focus on balanced growth and development'
        elif age >= 65:
            recommendations['notes'] = 'Include more fiber and calcium-rich foods'

        # Weight-based recommendations
        if bmi < 18.5:
            recommendations['notes'] = 'Consider increasing calorie intake'
        elif bmi > 25:
            recommendations['notes'] = 'Consider reducing calorie intake'

        return recommendations

    def generate_fitness_plan(self, age: int, lifestyle: Union[dict, str]) -> Dict:
        """Generate personalized fitness plan based on user data"""
        # Default values if lifestyle is string
        if isinstance(lifestyle, str):
            exercise = 'sometimes'
            sleep = '7-8'
        else:
            exercise = lifestyle.get('exercise', 'sometimes')
            sleep = lifestyle.get('sleep', '7-8')

        plan = {
            'workout_frequency': {
                'never': 'Start with 2-3 days/week',
                'rarely': 'Increase to 3-4 days/week',
                'sometimes': 'Maintain 3-4 days/week',
                'regularly': 'Consider 4-5 days/week',
                'daily': 'Great! Keep up daily routine'
            }[exercise],
            'duration': '30-45 minutes per session',
            'intensity': {
                'never': 'Light (walking, gentle yoga)',
                'rarely': 'Moderate (brisk walking, light jogging)',
                'sometimes': 'Moderate (jogging, cycling)',
                'regularly': 'Moderate to vigorous (running, cycling)',
                'daily': 'Vigorous (HIIT, running)'
            }[exercise],
            'rest': {
                'less than 6': 'Prioritize recovery',
                '6-7': 'Consider more sleep',
                '7-8': 'Good recovery time',
                '8-9': 'Excellent recovery',
                'more than 9': 'Consider reducing sleep'
            }[sleep]
        }

        return plan

    def get_lifestyle_recommendations(self, lifestyle: Union[dict, str]) -> List[str]:
        """Generate personalized lifestyle recommendations based on lifestyle data"""
        recommendations = []
        
        # Handle dictionary input
        if isinstance(lifestyle, dict):
            exercise = lifestyle.get('exercise', 'sometimes')
            sleep = lifestyle.get('sleep', '7-8')
        # Handle string input (one of 'sedentary', 'moderate', 'active', 'very_active')
        elif isinstance(lifestyle, str):
            if lifestyle == 'sedentary':
                exercise = 'rarely'
                sleep = 'less than 6'
            elif lifestyle == 'moderate':
                exercise = 'sometimes'
                sleep = '6-7'
            elif lifestyle == 'active':
                exercise = 'regularly'
                sleep = '7-8'
            elif lifestyle == 'very_active':
                exercise = 'daily'
                sleep = '8-9'
            else:
                exercise = 'sometimes'
                sleep = '7-8'
        else:
            exercise = 'sometimes'
            sleep = '7-8'

        # Exercise recommendations
        if exercise in ['never', 'rarely']:
            recommendations.append(
                "Start with light exercise (e.g., 15-minute walks) and gradually increase"
            )
        elif exercise in ['sometimes', 'regularly']:
            recommendations.append(
                "Maintain your current exercise routine and consider adding variety"
            )
        elif exercise == 'daily':
            recommendations.append(
                "Great job! Keep up your active lifestyle and ensure proper rest days"
            )

        # Sleep recommendations
        if sleep == 'less than 6':
            recommendations.append(
                "Aim for 7-9 hours of sleep per night for optimal health"
            )
        elif sleep == '6-7':
            recommendations.append(
                "Try to get closer to 8 hours of sleep for better recovery"
            )
        elif sleep == '7-8':
            recommendations.append(
                "Great sleep duration! Maintain this for optimal health"
            )
        elif sleep == '8-9':
            recommendations.append(
                "Excellent sleep duration! Keep it up"
            )
        elif sleep == 'more than 9':
            recommendations.append(
                "If you feel tired, consider reducing sleep duration to 7-9 hours"
            )

        # General lifestyle tips
        recommendations.extend([
            "Maintain a balanced diet with plenty of fruits and vegetables",
            "Stay hydrated by drinking at least 8 glasses of water daily",
            "Practice stress management techniques like meditation or deep breathing",
            "Regular health check-ups are recommended"
        ])

        return recommendations

    def preprocess_symptoms(self, symptoms: List[str]) -> List[str]:
        """Convert list of symptoms into a normalized format."""
        return [symptom.lower().strip() for symptom in symptoms]

    def find_similar_conditions(self, symptoms: List[str], top_k: int = 3) -> List[Dict]:
        """Find conditions most similar to the given symptoms using string similarity."""
        processed_symptoms = self.preprocess_symptoms(symptoms)
        similarities = []

        for condition_key, condition in self.conditions.items():
            condition_symptoms = condition['symptoms']
            # Calculate similarity score
            matches = sum(1 for symptom in processed_symptoms if symptom in condition_symptoms)
            similarity = matches / len(condition_symptoms)
            
            if similarity > 0:
                similarities.append({
                    'condition': condition_key,
                    'description': condition['description'],
                    'severity': condition['severity'],
                    'symptoms': condition_symptoms,
                    'similarity': similarity
                })

        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_k]

    def generate_diagnosis(self, symptoms: List[str], age: Union[int, str, None] = None, gender: str = None) -> Dict:
        """Generate a diagnosis based on symptoms and patient information."""
        try:
            # Validate symptoms
            if not symptoms or not isinstance(symptoms, list):
                return {
                    'diagnosis': 'Insufficient information',
                    'confidence': 0.0,
                    'severity': 'low',
                    'description': 'Not enough symptoms provided for diagnosis',
                    'recommendation': 'Please provide more detailed symptoms',
                    'alternative_conditions': [],
                    'symptoms': [],
                    'condition': 'insufficient_data',
                    'condition_id': 'insufficient_data'
                }
            
            # Convert age to integer if it's a string
            if isinstance(age, str):
                try:
                    age = int(age)
                except (ValueError, TypeError):
                    age = None
                    logger.warning("Invalid age format, using None")
            
            # Get similar conditions
            similar_conditions = self.find_similar_conditions(symptoms)
            
            if not similar_conditions:
                return {
                    'diagnosis': 'Insufficient information',
                    'confidence': 0.0,
                    'severity': 'low',
                    'description': 'Symptoms do not match any known conditions',
                    'recommendation': 'Please consult a healthcare provider',
                    'alternative_conditions': [],
                    'symptoms': symptoms,
                    'condition': 'unknown_condition',
                    'condition_id': 'unknown_condition'
                }
            
            # Get top condition
            top_condition = similar_conditions[0]
            confidence = top_condition['similarity']
            
            # Generate recommendations based on condition severity
            recommendation = self._generate_recommendation(
                top_condition['condition'], 
                top_condition['severity'],
                age,
                gender
            )
            
            # Validate response structure
            required_fields = ['diagnosis', 'condition', 'condition_id', 'confidence', 'severity', 'description', 'recommendation', 'alternative_conditions', 'symptoms']
            response = {
                'diagnosis': top_condition['description'],
                'condition': top_condition['condition'],
                'condition_id': top_condition['condition'],
                'confidence': float(confidence),
                'severity': top_condition['severity'],
                'description': top_condition['description'],
                'recommendation': recommendation,
                'alternative_conditions': similar_conditions[1:],
                'symptoms': symptoms
            }
            
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                logger.error(f"Missing required fields in diagnosis response: {missing_fields}")
                raise ValueError(f"Missing required fields: {missing_fields}")
            
            return response
            
        except ValueError as ve:
            logger.error(f"Value error in diagnosis: {str(ve)}", exc_info=True)
            return {
                'diagnosis': 'Error in diagnosis',
                'confidence': 0.0,
                'severity': 'unknown',
                'description': 'Failed to generate diagnosis',
                'recommendation': 'Please try again or consult a healthcare provider',
                'alternative_conditions': [],
                'symptoms': symptoms,
                'condition': 'error',
                'condition_id': 'error'
            }
        except Exception as e:
            logger.error(f"Unexpected error generating diagnosis: {str(e)}", exc_info=True)
            return {
                'diagnosis': 'Error in diagnosis',
                'confidence': 0.0,
                'severity': 'unknown',
                'description': 'Failed to generate diagnosis',
                'recommendation': 'Please try again or consult a healthcare provider',
                'alternative_conditions': [],
                'symptoms': symptoms,
                'condition': 'error',
                'condition_id': 'error'
            }

    def _generate_recommendation(self, condition: str, severity: str, age: Union[str, int] = None, gender: str = None) -> str:
        """Generate personalized recommendations based on condition, severity, age, and gender."""
        try:
            # Convert age to integer if it's a string
            if isinstance(age, str):
                try:
                    age = int(age)
                except (ValueError, TypeError):
                    logger.warning(f"Invalid age format: {age}")
                    age = None
            
            # Base recommendations
            recommendations = []
            
            # Add severity-based recommendations
            if severity == 'high':
                recommendations.append("Seek medical attention immediately")
                recommendations.append("Avoid self-medication")
            elif severity == 'moderate':
                recommendations.append("Schedule a doctor's appointment")
                recommendations.append("Monitor symptoms closely")
            else:
                recommendations.append("Rest and monitor symptoms")
                recommendations.append("Stay hydrated")
            
            # Add age-specific recommendations
            if age is not None:
                if age < 2:
                    recommendations.append("Contact pediatrician immediately")
                elif age < 18:
                    recommendations.append("Inform school/teachers")
                elif age >= 65:
                    recommendations.append("Contact healthcare provider")
                    recommendations.append("Monitor for complications")
            
            # Add gender-specific recommendations
            if gender == 'female':
                recommendations.append("Monitor for pregnancy-related symptoms")
            
            # Add condition-specific recommendations
            condition_recommendations = {
                'migraine': [
                    "Keep a headache diary",
                    "Identify and avoid triggers",
                    "Practice stress management"
                ],
                'gastroenteritis': [
                    "Stay hydrated",
                    "Eat bland foods",
                    "Avoid dairy and fatty foods"
                ]
            }
            
            recommendations.extend(condition_recommendations.get(condition.lower(), []))
            
            return ". ".join(recommendations) + "."
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}", exc_info=True)
            return "Consult a healthcare provider for proper diagnosis and treatment."

    def preprocess_symptoms(self, symptoms: List[str]) -> List[str]:
        """Convert list of symptoms into a normalized format."""
        if not symptoms:
            raise ValueError("Symptoms list cannot be empty")
            
        return [s.lower().strip() for s in symptoms if s.strip()]

    def find_similar_conditions(self, symptoms: List[str], top_k: int = 3) -> List[Dict]:
        """Find conditions most similar to the given symptoms using string similarity."""
        try:
            if not symptoms:
                logger.warning("No symptoms provided for diagnosis")
                return []
            
            results = []
            
            # Normalize input symptoms
            symptoms = self.preprocess_symptoms(symptoms)
            
            logger.info(f"Analyzing symptoms: {symptoms}")
            
            for condition_id, condition in self.conditions.items():
                # Calculate similarity score by comparing each symptom
                condition_symptoms = self.preprocess_symptoms(condition['symptoms'])
                
                logger.debug(f"Checking condition {condition_id} with symptoms: {condition_symptoms}")
                
                # Calculate similarity for each symptom
                symptom_matches = []
                for symptom in symptoms:
                    best_match = 0
                    for cond_symptom in condition_symptoms:
                        # Convert both to lowercase for comparison
                        symptom_str = str(symptom).lower()
                        cond_symptom_str = str(cond_symptom).lower()
                        
                        matcher = difflib.SequenceMatcher(None, symptom_str, cond_symptom_str)
                        similarity = matcher.ratio()
                        logger.debug(f"Similarity between '{symptom}' and '{cond_symptom}': {similarity}")
                        best_match = max(best_match, similarity)
                    symptom_matches.append(best_match)
                
                # Average similarity across all symptoms
                avg_similarity = sum(symptom_matches) / len(symptom_matches) if symptom_matches else 0
                
                # Add a minimum threshold for similarity
                if avg_similarity > 0.3:  # Only consider conditions with reasonable similarity
                    results.append({
                        'condition': condition_id,
                        'similarity': avg_similarity,
                        'description': condition['description'],
                        'severity': condition['severity']
                    })
                
            # Sort by similarity score in descending order
            results.sort(key=lambda x: float(x['similarity']), reverse=True)
            
            if results:
                logger.info(f"Found {len(results)} matching conditions")
                logger.debug(f"Top conditions: {results[:top_k]}")
            else:
                logger.warning("No matching conditions found")
                
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"Error finding similar conditions: {str(e)}", exc_info=True)
            return []

    def generate_diagnosis(self, symptoms: List[str], age: Union[int, str, None] = None, gender: str = None) -> Dict:
        """Generate a comprehensive diagnosis based on symptoms."""
        try:
            # Validate symptoms
            if not symptoms or not isinstance(symptoms, list):
                return {
                    'diagnosis': 'Insufficient information',
                    'confidence': 0.0,
                    'severity': 'low',
                    'description': 'Not enough symptoms provided for diagnosis',
                    'recommendation': 'Please provide more detailed symptoms',
                    'alternative_conditions': [],
                    'symptoms': [],
                    'condition': 'insufficient_data',
                    'condition_id': 'insufficient_data'
                }
            
            # Convert age to integer if it's a string
            if isinstance(age, str):
                try:
                    age = int(age)
                except (ValueError, TypeError):
                    age = None
                    logger.warning("Invalid age format, using None")
            
            # Get similar conditions
            similar_conditions = self.find_similar_conditions(symptoms)
            
            if not similar_conditions:
                return {
                    'diagnosis': 'Insufficient information',
                    'confidence': 0.0,
                    'severity': 'low',
                    'description': 'Symptoms do not match any known conditions',
                    'recommendation': 'Please consult a healthcare provider',
                    'alternative_conditions': [],
                    'symptoms': symptoms,
                    'condition': 'unknown_condition',
                    'condition_id': 'unknown_condition'
                }
            
            # Get top condition
            top_condition = similar_conditions[0]
            confidence = top_condition['similarity']
            
            # Generate recommendations based on condition severity
            recommendation = self._generate_recommendation(
                top_condition['condition'], 
                top_condition['severity'],
                age,
                gender
            )
            
            # Validate response structure
            required_fields = ['diagnosis', 'condition', 'condition_id', 'confidence', 'severity', 'description', 'recommendation', 'alternative_conditions', 'symptoms']
            response = {
                'diagnosis': top_condition['description'],
                'condition': top_condition['condition'],
                'condition_id': top_condition['condition'],
                'confidence': float(confidence),
                'severity': top_condition['severity'],
                'description': top_condition['description'],
                'recommendation': recommendation,
                'alternative_conditions': similar_conditions[1:],
                'symptoms': symptoms
            }
            
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                logger.error(f"Missing required fields in diagnosis response: {missing_fields}")
                raise ValueError(f"Missing required fields: {missing_fields}")
            
            return response
            
        except ValueError as ve:
            logger.error(f"Value error in diagnosis: {str(ve)}", exc_info=True)
            return {
                'diagnosis': 'Error in diagnosis',
                'confidence': 0.0,
                'severity': 'unknown',
                'description': 'Failed to generate diagnosis',
                'recommendation': 'Please try again or consult a healthcare provider',
                'alternative_conditions': [],
                'symptoms': symptoms,
                'condition': 'error',
                'condition_id': 'error'
            }
        except Exception as e:
            logger.error(f"Unexpected error generating diagnosis: {str(e)}", exc_info=True)
            return {
                'diagnosis': 'Error in diagnosis',
                'confidence': 0.0,
                'severity': 'unknown',
                'description': 'Failed to generate diagnosis',
                'recommendation': 'Please try again or consult a healthcare provider',
                'alternative_conditions': [],
                'symptoms': symptoms,
                'condition': 'error',
                'condition_id': 'error'
            }

# Singleton instance
medical_model = MedicalDiagnosisModel()
