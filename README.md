# PlanIt: AI-Powered Travel Planning Assistant

**PlanIt** is your intelligent travel planning companion! Powered by state-of-the-art AI technologies, it provides a seamless chat-based interface to help users plan their trips. From selecting a destination to finding the best hotels and managing your budget, **PlanIt** simplifies the entire process by utilizing the latest in AI and web technologies.

---

## ✨ Features

1. **Interactive Chat Interface**  
   Plan your travel conveniently through an AI-powered chat interface.  
   
2. **Destination Selection**  
   Get recommendations for destinations based on preferences like weather, activities, or budget.  

3. **Accommodation Assistance**  
   Explore curated hotel suggestions tailored to your location, budget, and preferences.

4. **Budget Management**  
   Estimate and manage costs for your trip with real-time data.

5. **Dynamic Data Collection**  
   Pulls live information from the internet for the most accurate and up-to-date travel planning.

---

## 🛠️ Tech Stack

- **Backend Framework**: Django  
- **Authentication**: Django Allauth  
- **AI Integration**: Ollama, LangChain  
- **Data Retrieval**: Web scraping & API calls  
- **Frontend**: Chat-based interface for user interaction  

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js (for the chat interface)
- Virtual environment (recommended)

### Steps

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/yourusername/PlanIt.git
   cd PlanIt
   ```

2. **Set Up Virtual Environment**  
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: .\env\Scripts\activate
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**  
   Create a `.env` file with the following:
   ```env
   DJANGO_SECRET_KEY=your-secret-key
   DATABASE_URL=your-database-url
   ```

5. **Run Migrations**  
   ```bash
   python manage.py migrate
   ```

6. **Start the Server**  
   ```bash
   python manage.py runserver
   ```

---

## 🧩 Usage

1. **Login/Sign Up**  
   Use Django Allauth to create an account or log in.  

2. **Start Chatting**  
   Initiate your travel planning with simple queries like:  
   - "I want to go to a beach destination within a $1000 budget."  
   - "Suggest a family-friendly hotel in Paris."

3. **Explore Suggestions**  
   Receive AI-generated recommendations for destinations, accommodations, and budget management in real time.

---

## 🗂️ Project Structure

```
PlanIt/
│
├── core/               # Main app logic
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🚀 Future Features

- **Flight Recommendations**  
  AI-curated flight options with price comparisons.  
- **Itinerary Suggestions**  
  Detailed activity plans for your selected destination.  
- **Integration with Google Maps**  
  Display hotel and destination locations visually.  

---

## 🤝 Contributing

We welcome contributions! To get started:  

1. Fork the repository.  
2. Create a feature branch (`git checkout -b feature-name`).  
3. Commit your changes (`git commit -m "Add feature name"`).  
4. Push to the branch (`git push origin feature-name`).  
5. Create a pull request.  

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🌟 Acknowledgements

Special thanks to the following tools and frameworks that made this project possible:  
- **Django**  
- **Django Allauth**  
- **Ollama**  
- **LangChain**  

Happy Planning with **PlanIt**! 🌍✈️