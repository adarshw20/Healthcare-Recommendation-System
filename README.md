# Health Recommendation System (HRS)

A modern web application that provides personalized health recommendations based on user input, including symptoms, vitals, and lifestyle factors. The system offers tailored medical advice, diet plans, and fitness recommendations.

## 🚀 Features

- **Health Assessment**: Input your symptoms, vitals, and health metrics
- **Personalized Recommendations**: Get customized health advice based on your inputs
- **Comprehensive Reports**: View detailed health reports with actionable insights
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Dark/Light Mode**: Toggle between themes for comfortable viewing

## 🛠️ Tech Stack

### Frontend
- React 18
- Vite (Build Tool)
- React Router (Navigation)
- Context API (State Management)
- Axios (HTTP Client)
- React Icons
- React Toastify (Notifications)

### Backend
- Python 3.x
- Flask (Web Framework)
- Flask-CORS (Cross-Origin Resource Sharing)

## 📦 Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Python 3.8+
- pip (Python package manager)

## 🚀 Getting Started

### Frontend Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hrs
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask development server:
   ```bash
   python app.py
   ```

5. The application should now be running at `http://localhost:5173`

## 📂 Project Structure

```
hrs/
├── src/
│   ├── components/        # React components
│   ├── contexts/          # React context providers
│   ├── assets/            # Static assets (images, fonts, etc.)
│   ├── App.jsx            # Main application component
│   └── main.jsx           # Application entry point
├── backend/
│   ├── app.py            # Flask application
│   └── requirements.txt   # Python dependencies
├── public/               # Static files
└── package.json          # Node.js dependencies and scripts
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [React](https://reactjs.org/)
- [Vite](https://vitejs.dev/)
- [Flask](https://flask.palletsprojects.com/)
- [React Icons](https://react-icons.github.io/react-icons/)
# Healthcare Recommendation System

A comprehensive health assessment and recommendation system that provides personalized medical recommendations based on user symptoms and health data.

## Features

- Personalized health assessment based on user symptoms and medical history
- AI-powered symptom analysis and diagnosis
- Detailed medication recommendations with dosage and usage instructions
- Customized diet plans for different meals of the day
- Tailored fitness recommendations including cardio, strength, flexibility, and recovery exercises
- Dark mode support for better readability
- Print-friendly report generation
- Shareable health assessment results
- Professional medical disclaimer and safety information

## Technical Architecture

### Medical Assessment Model

The core of the system is the `MedicalDiagnosisModel`, which utilizes a hybrid approach combining:

1. **Symptom Similarity Analysis**
   - Uses cosine similarity to match user symptoms with known medical conditions
   - Employs TF-IDF vectorization for symptom weighting
   - Implements semantic clustering for related symptoms

2. **Rule-Based Diagnosis System**
   - Implements a decision tree for symptom progression analysis
   - Uses Bayesian probability for condition likelihood calculation
   - Includes severity scoring based on symptom combinations

3. **Recommendation Engine**
   - Personalized medication recommendations based on condition and severity
   - Diet plans generated using nutritional science principles
   - Fitness recommendations tailored to medical condition and physical capabilities

### Implementation Details

#### Backend (Flask)

- **API Endpoints**:
  - `/api/health-assessment`: Main endpoint for symptom analysis and recommendations
  - `/api/health-tips`: Provides general health maintenance tips
  - `/api/emergency-contacts`: Returns emergency medical contact information
  - `/api/health-check`: Performs system health checks

- **Error Handling**:
  - Comprehensive error logging using Python logging module
  - Graceful error handling for missing or invalid input
  - Detailed error messages for debugging

- **Performance Optimizations**:
  - Caching of frequently accessed medical data
  - Asynchronous processing for heavy computations
  - Optimized database queries for symptom matching

#### Frontend (React)

- **State Management**:
  - Uses React Context API for global state management
  - Custom hooks for medical assessment state
  - Efficient state updates using React's batch updates

- **UI Components**:
  - Reusable medical cards for displaying recommendations
  - Custom symptom input components with validation
  - Dark mode support using CSS variables
  - Print-friendly layout using CSS media queries

- **Performance Features**:
  - Lazy loading of heavy components
  - Code splitting for faster initial load
  - Optimized image loading with WebP format
  - Virtual scrolling for long lists of recommendations

## Tech Stack and Implementation Details

### Frontend Technologies

1. **React.js**
   - Used for building the user interface
   - Provides efficient state management and component reusability
   - Enables server-side rendering for better SEO

2. **Vite**
   - Modern build tool with faster development server
   - Hot Module Replacement for instant updates
   - Optimized bundling for production

3. **React Icons**
   - Provides medical and fitness related icons
   - Optimized SVG icons for better performance
   - Easy integration with React components

4. **React To Print**
   - Enables seamless report generation
   - Customizable print styles
   - Handles complex layouts for medical reports

5. **React Context API**
   - Manages global state effectively
   - Reduces prop drilling
   - Efficient state updates with memoization

### Backend Technologies

1. **Flask**
   - Lightweight web framework for Python
   - Easy to set up and maintain
   - Built-in development server

2. **Python**
   - Used for medical diagnosis logic
   - Implements machine learning models
   - Handles complex data processing

3. **Werkzeug**
   - Provides HTTP utilities
   - Handles request routing
   - Implements middleware for security

### Key Libraries

1. **scikit-learn**
   - Used for symptom similarity calculations
   - Implements TF-IDF vectorization
   - Provides clustering algorithms

2. **numpy**
   - Handles numerical computations
   - Optimizes matrix operations
   - Provides statistical functions

3. **pandas**
   - Manages medical data efficiently
   - Provides data analysis tools
   - Handles data preprocessing

## Prerequisites and Setup

### System Requirements

1. **Python 3.9+**
   - Required for backend development
   - Supports modern Python features
   - Better performance than older versions

2. **Node.js 16+**
   - Required for frontend development
   - Provides npm package manager
   - Better performance with V8 engine

3. **Package Managers**
   - `pip` for Python dependencies
   - `npm` for JavaScript dependencies
   - Both required for project setup

### Development Environment Setup

1. **Backend Setup**:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   .\venv\Scripts\activate  # On Windows
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run Flask server
   python app.py
   ```

2. **Frontend Setup**:
   ```bash
   # Install dependencies
   npm install
   
   # Start development server
   npm run dev
   ```

## Installation

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask server:
   ```bash
   python app.py
   ```

### Frontend Setup

1. Navigate to the project root:
   ```bash
   cd src
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

## Project Structure and Organization

```
hrs/
├── backend/              # Flask backend server
│   ├── app.py           # Main Flask application
│   ├── medical_model.py # Health assessment logic
│   └── requirements.txt # Python dependencies
├── src/                 # React frontend
│   ├── components/      # React components
│   │   ├── Results.jsx # Health assessment results
│   │   ├── Assessment.jsx # User input form
│   │   └── HealthCard.jsx # Reusable medical card
│   ├── App.jsx          # Main application component
│   └── App.css          # Global styles
└── public/              # Static assets
    ├── images/         # Medical and fitness images
    └── fonts/          # Custom fonts
```

### Code Organization

1. **Backend**:
   - `app.py`: Main Flask application and API routes
   - `medical_model.py`: Core medical diagnosis logic
   - `utils.py`: Helper functions and data processing

2. **Frontend**:
   - `components/`: Reusable React components
   - `App.jsx`: Main application container
   - `App.css`: Global styles and theme management

3. **Assets**:
   - `public/images/`: Medical and fitness related images
   - `public/fonts/`: Custom fonts for medical symbols

## Usage

1. Enter your health information including symptoms, age, and medical history
2. Submit the assessment to generate personalized recommendations
3. View comprehensive health recommendations including:
   - Medical diagnosis and severity assessment
   - Medication recommendations with usage instructions
   - Customized diet plan for different meals
   - Tailored fitness recommendations
4. Print or share your health assessment report

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
