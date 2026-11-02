# 🛡️ Phishing Website Detection System

### Machine Learning-Based Phishing Website Detection Using URL Feature Analysis

<p align="center">
  A Machine Learning-powered web application that analyzes URLs and identifies potentially malicious phishing websites using a Random Forest classifier.
</p>

---

## 📌 Project Overview

The **Phishing Website Detection System** is a web-based cybersecurity application designed to identify potentially malicious phishing websites using Machine Learning techniques.

The system analyzes submitted URLs by extracting **17 different URL-based features** and processes them using a trained **Random Forest classification model** to predict whether a website is **Legitimate** or **Phishing**.

Developed using Python and Flask, the application provides a user-friendly interface for instant URL security analysis. It also maintains previous scanning records using an SQLite database.

## 🎯 Objectives

- Detect potentially malicious phishing websites using Machine Learning.
- Analyze URLs using 17 important URL-based features.
- Classify websites as legitimate or phishing.
- Provide fast and automated URL security analysis.
- Maintain previous scan records.
- Improve awareness of phishing website threats.

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 URL Detection | Analyze submitted website URLs. |
| 🤖 Machine Learning | Uses a Random Forest classification model. |
| 📊 17 URL Features | Extracts important URL characteristics. |
| ⚡ Instant Results | Displays prediction results through the web interface. |
| 🗂️ Scan History | Stores and displays previous scanning records. |
| 📈 Model Performance | Provides model evaluation information. |
| 💻 User-Friendly Interface | Simple and easy-to-use web application. |

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | HTML, CSS, JavaScript |
| Backend | Flask |
| Machine Learning | Scikit-learn, Random Forest |
| Database | SQLite |
| Data Processing | Pandas, NumPy |
| Model Storage | Joblib |

## 🏗️ System Architecture

The application follows this workflow:

```text
          User
           |
           v
    Enter Website URL
           |
           v
     Flask Application
           |
           v
     URL Feature Extraction
           |
           v
   Extract 17 URL Features
           |
           v
   Random Forest Classifier
           |
           v
     Prediction Result
       /         \
      v           v
 Legitimate     Phishing
       \         /
           |
           v
    Display Result
           |
           v
    SQLite Database
           |
           v
       Scan History
```

## 📂 Project Structure

```text
Phishing-Website-Detection/
│
├── app.py
├── feature_extraction.py
├── train_model.py
├── test_system.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── phishing_dataset.csv
│   └── download_dataset.py
│
├── database/
│   ├── db.py
│   └── scan_history.db
│
├── models/
│   ├── phishing_model.joblib
│   └── model_metrics.json
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│       └── logo.svg
│
└── templates/
    ├── base.html
    ├── index.html
    ├── result.html
    ├── history.html
    ├── about.html
    └── model_performance.html
```

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/USERNAME/REPOSITORY-NAME.git
```

### 2. Navigate to the Project Folder

```bash
cd Phishing-Website-Detection
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```powershell
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

### 7. Open in Browser

Visit:

```text
http://127.0.0.1:5000/
```

## 🧠 Machine Learning Model

The project uses a **Random Forest Classifier** to identify potentially phishing websites.

The model analyzes URL characteristics using the extracted features and classifies the submitted URL into one of two categories:

- **Legitimate:** The URL is classified as legitimate by the trained model.
- **Phishing:** The URL is classified as potentially associated with phishing activity by the trained model.

### Model Highlights

- Random Forest classification algorithm.
- 17 URL-based features.
- Trained phishing detection model.
- Automated URL classification.
- Model performance evaluation.

## 🗄️ Database

The application uses **SQLite** to maintain scan history.

The database stores relevant scanning information, allowing users to:

- View previous URL scans.
- Retrieve stored prediction results.
- Maintain scanning records.
- Access historical analysis information.

## 🔮 Future Enhancements

- Integration with real-time threat intelligence services.
- Improved detection using advanced Machine Learning algorithms.
- Browser extension support.
- Automated blacklist checking.
- Additional website security analysis features.
- Cloud-based application deployment.

## 🔐 Disclaimer

This project is developed for educational and cybersecurity research purposes.

The predictions generated by the Machine Learning model are based on URL characteristics and should not be considered a guarantee that a website is completely safe or malicious. Users should exercise caution when visiting unfamiliar websites.

## 👨‍💻 Authors

**Pranesh**  
Computer Science and Engineering Student

**Mohammed Arshath**  
Computer Science and Engineering Student

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

<p align="center">
  <b>🛡️ Phishing Website Detection System</b><br>
  Protecting Users Through Machine Learning
</p>
