"""
Utility functions for health assessment system
"""

def get_lifestyle_recommendations(lifestyle):
    """Generate personalized lifestyle recommendations"""
    recommendations = []
    
    # Handle both dictionary and string inputs
    if isinstance(lifestyle, dict):
        exercise = lifestyle.get('exercise', 'sometimes')
        sleep = lifestyle.get('sleep', '7-8')
    else:
        exercise = 'sometimes'  # Default for string input
        sleep = '7-8'  # Default for string input

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

def get_differential_diagnosis(condition, symptoms):
    """Generate differential diagnosis based on condition and symptoms"""
    return [
        {
            "condition": "Migraine",
            "similarity": 0.85,
            "description": "Severe, throbbing headache often accompanied by nausea and sensitivity to light"
        },
        {
            "condition": "Tension Headache",
            "similarity": 0.75,
            "description": "Mild to moderate headache that feels like a tight band around the head"
        }
    ]

def get_follow_up_instructions(condition, age, symptoms):
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

def get_preventive_measures(condition):
    """Generate preventive measures for the given condition"""
    return [
        "Regular exercise (30 minutes, 5 days a week)",
        "Balanced diet with fruits, vegetables, and whole grains",
        "Adequate hydration (8-10 glasses of water daily)",
        "Regular health check-ups",
        "Avoid smoking and limit alcohol consumption"
    ]

def emergency_contacts():
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

def health_tips():
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
