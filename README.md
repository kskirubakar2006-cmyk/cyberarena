# CyberArena

## Overview
CyberArena is an interactive, gamified cybersecurity awareness and threat simulation platform. It helps users learn about cybersecurity through realistic but completely safe simulated scenarios. 

## Problem Statement
Traditional cybersecurity training is often static, boring, and theoretical. Users fail to recognize real-world threats because they haven't practiced making decisions under pressure in realistic situations.

## Solution
CyberArena provides a "learn by doing" approach. Users face simulated threats (like phishing emails, social engineering calls, and digital payment scams), make decisions, and receive immediate feedback, XP, and skill tracking based on their choices.

## Features
- **Realistic Scenario Engine**: 20+ safe, simulated cyber threats across 8 categories.
- **Immediate Feedback**: Detailed explanations and security tips after every decision.
- **Gamified Progression**: Earn XP, level up (from Cyber Rookie to Cyber Champion), and maintain daily streaks.
- **Skill Analytics**: Track proficiency in specific areas like Phishing, Password Security, and Malware Awareness using radar charts.
- **Adaptive Recommendations**: Suggests challenges based on the user's weakest skill category.
- **Badge System**: Unlock achievements based on performance.
- **Global Leaderboard**: Compete with other recruits for the top rank.
- **Admin Dashboard**: Comprehensive platform management and analytics.

## Technology Stack
- **Backend**: Python 3, Flask
- **Database**: SQLite, SQLAlchemy ORM
- **Authentication**: Flask-Login, Werkzeug Password Hashing
- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Bootstrap 5 (Responsive)
- **Data Visualization**: Chart.js

## System Architecture
The platform uses a monolithic MVC architecture built on Flask:
- **Routes**: Handle HTTP requests and business logic (`auth`, `dashboard`, `challenges`, `admin`).
- **Services**: Encapsulate complex logic like scoring and badge calculation.
- **Models**: Define the SQLite database schema using SQLAlchemy.
- **Templates**: Jinja2 HTML templates for dynamic frontend rendering.

## Project Structure
```text
CyberArena/
├── app.py                 # Application factory and entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── seed.py                # Database seeding script
├── database/              # SQLAlchemy models and setup
├── routes/                # Flask blueprints for routing
├── services/              # Business logic (scoring, badges)
├── templates/             # HTML templates (Jinja2)
├── static/                # CSS, JS, and image assets
├── instance/              # SQLite database storage
└── tests/                 # Pytest automated tests
```

## Database Design
The core database tables include:
- `User`: Stores student and admin accounts with XP and level data.
- `Scenario`: Defines the cybersecurity challenges.
- `Option`: Represents the choices available for each scenario.
- `Attempt`: Tracks a user's answer and response time for a specific scenario.
- `Badge` & `UserBadge`: Handles the achievement system.
- `Skill` & `UserSkill`: Tracks performance across different cybersecurity domains.

## Installation
Ensure you have Python 3 installed.

1. Clone or download the repository.
2. Open a terminal in the project directory.
3. Create a virtual environment:
   ```cmd
   python -m venv venv
   ```
4. Activate the virtual environment (Windows):
   ```cmd
   venv\Scripts\activate
   ```
5. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

## Running the Project
1. Initialize the database and populate it with seed data (do this once):
   ```cmd
   python seed.py
   ```
2. Start the Flask server:
   ```cmd
   python app.py
   ```
3. Open your browser and navigate to: `http://127.0.0.1:5000`

## Demo Accounts
Use these accounts to test the platform (passwords are hashed in the database):

**Student Account:**
- **Email:** `student@cyberarena.local`
- **Password:** `student123`

**Admin Account:**
- **Email:** `admin@cyberarena.local`
- **Password:** `admin123`

## Screenshots section placeholder
*(Add screenshots of the Dashboard, Arena, and Admin Panel here)*

## Future Enhancements
- **Machine Learning Integration**: Implement risk classification models using scikit-learn.
- **Multiplayer/Team Modes**: Allow users to compete or collaborate in teams.
- **More Advanced Scenarios**: Add multi-stage threat scenarios with branching storylines.
- **Email Notifications**: Send alerts for new challenges or lost streaks.

## Safety and Ethics
CyberArena is strictly for educational purposes. All scenarios, emails, and links are simulated and contained within the application. The platform does not perform real credential harvesting, malicious execution, or unauthorized network scanning. 

## Author
Antigravity
