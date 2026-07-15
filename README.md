# 🔐 AI-Based Fraud Detection System for Online Transactions with Real-Time Alerts

## 📌 Project Overview

The **AI-Based Fraud Detection System** is a Machine Learning-based web application designed to detect fraudulent online financial transactions and generate real-time alerts.

The system analyzes transaction data using trained Machine Learning models and classifies transactions as either **Legitimate** or **Fraudulent**. When a fraudulent transaction is detected, the system generates an immediate alert.

## 🎯 Objectives

* Detect fraudulent online transactions using Machine Learning.
* Handle highly imbalanced transaction datasets.
* Compare the performance of different Machine Learning algorithms.
* Provide real-time fraud predictions through a web application.
* Generate real-time alerts when suspicious transactions are detected.

## 🤖 Machine Learning Models

The following models were evaluated:

* Logistic Regression
* Random Forest Classifier
* Deep Learning / Artificial Neural Network (ANN)

The **Random Forest Classifier** was selected as the primary model because of its strong performance in detecting fraudulent transactions.

## 📊 Model Performance

| Model               | Accuracy | Fraud Precision | Fraud Recall | F1-Score |
| ------------------- | -------: | --------------: | -----------: | -------: |
| Logistic Regression |      97% |              6% |          92% |      11% |
| Random Forest       |   99.99% |             87% |          83% |      85% |
| Deep Learning       |    99.4% |             26% |          88% |      40% |

## ✨ Key Features

* 🔍 Real-time fraud detection
* 🤖 Machine Learning-based prediction
* ⚖️ Handling class imbalance using SMOTE
* 🌐 Flask-based web application
* 📧 Real-time fraud alert notifications
* 📊 Model performance evaluation
* 📈 Confusion Matrix and ROC Curve analysis
* 🔎 Feature Importance Analysis
* 💻 User-friendly web interface

## 🛠️ Technologies Used

* **Programming Language:** Python
* **Machine Learning:** Scikit-learn
* **Data Processing:** Pandas, NumPy
* **Imbalanced Data Handling:** SMOTE
* **Web Framework:** Flask
* **Frontend:** HTML, CSS, JavaScript
* **Data Visualization:** Matplotlib
* **Development Environment:** VS Code

## ⚙️ System Workflow

1. Transaction data is provided through the web interface.
2. The input data is validated and preprocessed.
3. The trained Machine Learning model analyzes the transaction.
4. The system predicts whether the transaction is legitimate or fraudulent.
5. The prediction result is displayed to the user.
6. If fraud is detected, a real-time alert is generated.

## 📈 Evaluation Metrics

The models were evaluated using:

* Accuracy
* Precision
* Recall
* F1-Score
* Confusion Matrix
* ROC Curve

## 🚀 Future Scope

Future improvements may include:

* Integration of advanced Deep Learning models.
* Explainable AI (XAI) for better model transparency.
* Cloud deployment for improved scalability.
* Integration of behavioral and device-related data.
* Mobile-friendly interfaces.
* Continuous model retraining to detect evolving fraud patterns.


