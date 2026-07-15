# 🔐 AI-Based Fraud Detection System for Online Transactions with Real-Time Alerts

An intelligent Machine Learning-based system designed to detect fraudulent online financial transactions and generate real-time alerts through a Flask-based web application.

---

## 📌 Project Overview

The rapid growth of online financial transactions has increased the risk of fraudulent activities. Traditional rule-based fraud detection systems often struggle to identify new and evolving fraud patterns.

This project presents an **AI-Based Fraud Detection System** that uses Machine Learning algorithms to classify transactions as either **Legitimate** or **Fraudulent**.

The system compares multiple Machine Learning approaches and uses the **Random Forest Classifier** as the primary model due to its strong performance. The trained model is integrated into a **Flask web application** to provide real-time fraud predictions and alerts.

---

## 🎯 Objectives

- Develop an intelligent system for detecting fraudulent financial transactions.
- Preprocess and analyze highly imbalanced transaction data.
- Compare multiple Machine Learning algorithms.
- Select the best-performing model for fraud detection.
- Provide real-time fraud predictions through a web interface.
- Generate alerts when a fraudulent transaction is detected.
- Evaluate model performance using standard classification metrics.

---

## ✨ Key Features

- 🔍 Real-time transaction fraud detection
- 🤖 Machine Learning-based prediction
- ⚖️ Handling of imbalanced transaction data
- 📊 Comparison of multiple ML models
- 🌐 Flask-based web application
- 📧 Real-time fraud alert notifications
- 📈 Model performance visualization
- 🔎 Feature importance analysis
- 💾 SQLite database integration
- 🖥️ User-friendly web interface

---

## 🤖 Machine Learning Models

The following models were evaluated:

1. **Logistic Regression**
2. **Random Forest Classifier**
3. **Deep Learning / Artificial Neural Network (ANN)**

The **Random Forest Classifier** was selected as the primary model because of its strong overall performance and ability to handle complex and imbalanced transaction data.

---

## 📊 Model Performance

| Model | Accuracy | Fraud Precision | Fraud Recall | F1-Score |
|------|---------:|----------------:|-------------:|---------:|
| Logistic Regression | 97% | 6% | 92% | 11% |
| **Random Forest** | **99.99%** | **87%** | **83%** | **85%** |
| Deep Learning | 99.4% | 26% | 88% | 40% |

> **Note:** For highly imbalanced fraud datasets, accuracy alone can be misleading. Precision, recall, F1-score, confusion matrix, and ROC-AUC should also be considered when evaluating model performance.

---

## 🛠️ Technologies Used

### Programming Language
- Python

### Machine Learning & Data Processing
- Scikit-learn
- Pandas
- NumPy
- SMOTE / Imbalanced-learn

### Web Development
- Flask
- HTML
- CSS
- JavaScript

### Database
- SQLite

### Data Visualization
- Matplotlib

### Development Tools
- Visual Studio Code
- Google Colab
- Jupyter Notebook
- Git
- GitHub

---

## 📁 Project Structure

```text
AI-Based-Fraud-Detection-System-for-Online-Transactions-with-Real-Time-Alerts/
│
├── static/
│   └── Static files such as CSS, JavaScript, and images
│
├── templates/
│   └── HTML templates used by the Flask application
│
├── venv/
│   └── Python virtual environment
│
├── Google collab Code.ipynb
│   └── Model experimentation and data analysis notebook
│
├── app.py
│   └── Main Flask web application
│
├── check_importance.py
│   └── Feature importance analysis
│
├── creditcard.csv
│   └── Credit card transaction dataset
│
├── database.db
│   └── SQLite database
│
├── fraud_model.pkl
│   └── Saved trained fraud detection model
│
├── model_metrics.pkl
│   └── Saved model evaluation metrics
│
├── scaler.pkl
│   └── Saved feature scaler
│
├── train_model.py
│   └── Model training and evaluation script
│
├── requirements.txt
│   └── Required Python dependencies
│
├── read.txt
│   └── Additional project information
│
└── README.md
    └── Project documentation
```

---

## 🔄 Project Workflow

```text
Credit Card Transaction Dataset
              │
              ▼
       Data Preprocessing
              │
              ▼
       Feature Scaling
              │
              ▼
   Handle Class Imbalance
         Using SMOTE
              │
              ▼
       Train-Test Split
              │
              ▼
       Model Training
              │
              ▼
 ┌───────────────────────────┐
 │   Logistic Regression     │
 │   Random Forest           │
 │   Deep Learning (ANN)     │
 └───────────────────────────┘
              │
              ▼
   Model Evaluation & Comparison
              │
              ▼
    Select Best Performing Model
              │
              ▼
        Random Forest
              │
              ▼
     Save Trained Model
      (fraud_model.pkl)
              │
              ▼
      Integrate with Flask
           (app.py)
              │
              ▼
    User Enters Transaction Data
              │
              ▼
       Input Preprocessing
              │
              ▼
      Real-Time Prediction
              │
        ┌─────┴─────┐
        ▼           ▼
   Legitimate    Fraudulent
   Transaction   Transaction
        │           │
        ▼           ▼
   Safe Result   Fraud Alert
   Displayed     Generated
                    │
                    ▼
             Email Notification
```

---

## ⚙️ How the System Works

### 1. Data Collection

The system uses a credit card transaction dataset containing legitimate and fraudulent transaction records.

### 2. Data Preprocessing

The dataset is cleaned and prepared before model training. This includes:

- Handling missing values
- Feature preparation
- Feature scaling
- Separating input features and target labels

### 3. Handling Class Imbalance

Fraud detection datasets are highly imbalanced because fraudulent transactions are much less common than legitimate transactions.

Techniques such as **SMOTE (Synthetic Minority Over-sampling Technique)** are used to improve the representation of fraudulent transactions during model training.

### 4. Model Training

Multiple Machine Learning models are trained and evaluated.

The **Random Forest Classifier** provides the best overall performance and is selected for the final application.

### 5. Model Saving

The trained model and preprocessing components are saved as:

```text
fraud_model.pkl
scaler.pkl
model_metrics.pkl
```

These files allow the Flask application to make predictions without retraining the model every time the application starts.

### 6. Flask Web Application

The trained model is integrated into a Flask-based web application.

Users can enter transaction information through the web interface. The application preprocesses the input and sends it to the trained model.

### 7. Real-Time Prediction

The model classifies the transaction as:

- ✅ **Legitimate Transaction**
- 🚨 **Fraudulent Transaction**

If fraud is detected, the system generates a real-time alert.

---

## 📈 Model Evaluation Metrics

The models are evaluated using:

- **Accuracy** – Overall percentage of correct predictions.
- **Precision** – How many transactions predicted as fraud were actually fraudulent.
- **Recall** – How many actual fraudulent transactions were successfully detected.
- **F1-Score** – Balance between precision and recall.
- **Confusion Matrix** – Displays correct and incorrect classifications.
- **ROC Curve / ROC-AUC** – Measures the model's ability to distinguish between legitimate and fraudulent transactions.

---

## 🔎 Feature Importance Analysis

The project includes feature importance analysis using:

```text
check_importance.py
```

Random Forest provides feature importance scores that help identify which transaction features contribute most strongly to fraud predictions.

---

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/dhilleswar07/AI-Based-Fraud-Detection-System-for-Online-Transactions-with-Real-Time-Alerts.git
```

### 2. Navigate to the Project Directory

```bash
cd AI-Based-Fraud-Detection-System-for-Online-Transactions-with-Real-Time-Alerts
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 5. Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the Flask application:

```bash
python app.py
```

After starting the server, open the local address displayed in the terminal, typically:

```text
http://127.0.0.1:5000
```

---

## 🧠 Training the Model

To train or retrain the Machine Learning model:

```bash
python train_model.py
```

The training process prepares the data, trains the model, evaluates its performance, and saves the required model files.

---

## 🔍 Running Feature Importance Analysis

```bash
python check_importance.py
```

This script analyzes the importance of different features used by the trained fraud detection model.

---


---

## 🎥 Project Demo

Add your project demonstration video or LinkedIn demo link here.

```text
https://www.linkedin.com/posts/dhilleswar07_machinelearning-artificialintelligence-datascience-ugcPost-7483111910595428352-fXgn/
```

---

## 🔮 Future Scope

Future enhancements may include:

- Integration of advanced Deep Learning models.
- Graph Neural Networks for detecting complex fraud relationships.
- Transformer-based fraud detection models.
- Explainable AI (XAI) for transparent predictions.
- Cloud deployment for improved scalability.
- Integration with real-time banking transaction APIs.
- Device fingerprint and geolocation analysis.
- Continuous model retraining for evolving fraud patterns.
- Mobile-friendly user interface.
- Multilingual support.

---

## ⚠️ Disclaimer

This project is developed for **educational and research purposes**. The predictions generated by the system should not be used as the sole basis for real-world financial or banking decisions without additional validation, security controls, and regulatory compliance.

---

## 👨‍💻 Author

### Jogi Dhilleswar

**B.Tech – Computer Science and Engineering**

Interested in:

- Data Science
- Machine Learning
- Artificial Intelligence
- Generative AI
- Agentic AI



---

## 📄 Research Project

**Title:** AI-Based Fraud Detection System for Online Transactions with Real-Time Alerts

The project focuses on combining Machine Learning techniques with a user-friendly web application to provide intelligent and responsive fraud detection.

---

## ⭐ Support

If you find this project useful, consider giving the repository a **⭐ Star**.

Your feedback and suggestions are always welcome!

---

