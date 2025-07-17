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
# Healthcare-Recommendation-System
