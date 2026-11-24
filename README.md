# Head & Brain Weight Prediction App

An end-to-end Machine Learning and Desktop GUI project built with **Python**, **scikit-learn**, and **Flet**, designed to predict human brain weight based on head size, gender, and age range.

---

## 🚀 Features
- **Machine Learning Model:** Trained Linear Regression model utilizing head size, gender, and age range features.
- **Interactive GUI:** Built using **Flet** (Flutter-inspired Python framework) for a modern desktop experience.
- **Input Validation:** Robust error handling for invalid, empty, or negative head size inputs.
- **Model Persistence:** Model is serialized and loaded efficiently using `joblib`.

---

## 📂 Project Structure
```text
head-brain-regression/
│
├── data/                  # Dataset files
├── images/                # App screenshots and analysis plots
├── app.py                 # Main Flet GUI application
├── head_brain_model.joblib # Trained machine learning model
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
🛠️ Installation & Setup
Clone the repository:
bash
   git clone https://github.com/Abolfazl0938/head-brain-regression.git
   cd head-brain-regression
   
Install dependencies:Make sure you have Python installed, then run:
bash
   pip install flet scikit-learn numpy joblib
   
Run the application:
bash
   python app.py
   
📊 Dataset Source
The dataset used for training this model is sourced from Kaggle:

Head and Brain Size Dataset

👨‍💻 Author
Developed as part of a Machine Learning & Python engineering journey.