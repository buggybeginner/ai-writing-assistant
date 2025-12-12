# 🎭 PersonaWrite AI - Intelligent Writing Assistant

## 📋 Project Overview
PersonaWrite AI is an intelligent writing assistant that adapts to users' personal writing styles. 
This project was developed as a Final Year Project with a two-person team.

## 👥 Team Roles
- **Person A**: Backend/AI Development (LLM integration, style analysis algorithms)
- **Person B**: Frontend/UX Development (Streamlit interface, user experience design)

## 🚀 Features
### ✅ Implemented by Person B (Frontend)
- **4-Page Navigation System**: Home, Preset Personalities, Personal Style, Dashboard
- **Modern UI/UX**: Gradient-based design with responsive CSS
- **Interactive Components**: Personality cards, file upload, real-time generation
- **Modular Architecture**: Clean separation with pages/ and utils/ directories
- **Testing Framework**: Unit tests for UI components and completeness checks

### 🔄 To be Integrated by Person A (Backend)
- AI model integration for style analysis
- Real text generation with LLMs
- User authentication system
- Database for profile storage

## 🛠️ Tech Stack
- **Frontend**: Streamlit 1.28.0, Custom CSS, Plotly for visualizations
- **Backend**: Python 3.11, FastAPI (planned), LLM integration (planned)
- **Development**: Git, Virtual Environments, Modular Python

## 📁 Project Structure
personawrite-ai/
├── app.py # Main application router
├── requirements.txt # Python dependencies
├── pages/ # Modular page components
│ ├── home.py # Landing page
│ ├── preset.py # Preset personalities interface
│ ├── personal.py # Personal style learning
│ └── dashboard.py # Analytics dashboard
├── utils/ # Reusable components
│ └── ui_components.py
├── assets/ # Static assets
│ └── styles.css # Custom CSS
├── tests/ # Test scripts
│ ├── test_ui.py # Unit tests
│ └── final_test.py # Completeness tests
└── docs/ # Documentation (this folder)