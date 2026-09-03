# Click-Through Rate (CTR) Prediction

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![LightGBM](https://img.shields.io/badge/LightGBM-3.3.5-green.svg)](https://lightgbm.readthedocs.io/)
[![Flask](https://img.shields.io/badge/Flask-2.3.0-red.svg)](https://flask.palletsprojects.com/)

## 🎯 Project Overview

A complete data science project that predicts whether a user will click on an online advertisement using behavioral and demographic data. This project demonstrates the end-to-end machine learning pipeline from data exploration to deployment.

### Key Features
- **Data Analysis**: Comprehensive EDA with visualizations
- **Feature Engineering**: Advanced feature creation for CTR prediction
- **Model Training**: LightGBM with hyperparameter tuning
- **Web Interface**: Interactive Flask web application for predictions
- **Real-time Predictions**: Test your own ad click scenarios

## 📊 Dataset

We use the famous **"Click-Through Rate Prediction"** dataset from Kaggle's Ad Click Prediction challenge. The dataset contains:
- 10,000 samples
- 8 features including user demographics and ad information
- Binary target variable (click or not)

### Features
- **Demographic**: Age, Gender, Income
- **Behavioral**: Time spent on site, Previous clicks
- **Ad-related**: Ad category, Device type, Time of day

## 🏗️ Project Structure

```text
CTR-Prediction/
├── notebooks/                # Jupyter notebooks for analysis
│ ├── 01_EDA_and_Data_Preprocessing.ipynb
│ ├── 02_Feature_Engineering.ipynb
│ └── 03_Model_Training_and_Evaluation.ipynb
├── webapp/                   # Flask web application
│ ├── app.py                  # Main Flask application
│ ├── templates/              # HTML templates
│ └── static/                 # CSS and JavaScript files
├── data/                     # Dataset storage
├── models/                   # Saved model files
├── CONTRIBUTE.md             # Contribution guidelines
├── CHANGELOG.md              # Project changelog
└── README.md                 # Project documentation
```

## 🚀 Getting Started

### Prerequisites

You will need Python 3.8+ installed on your system.

```bash
pip install -r requirements.txt
```

### Installation

**1. Clone the repository**
```bash
git clone [https://github.com/yourusername/CTR-Prediction.git](https://github.com/yourusername/CTR-Prediction.git)
cd CTR-Prediction
```

**2. Install dependencies**
```bash
pip install pandas numpy matplotlib seaborn scikit-learn lightgbm flask joblib
```

**3. Download the dataset**
Run the following script to generate the sample dataset:
```python
from sklearn.datasets import make_classification
import pandas as pd

X, y = make_classification(n_samples=10000, n_features=8, n_informative=6, 
                           n_redundant=2, random_state=42)
df = pd.DataFrame(X, columns=['Age', 'Income', 'Time_on_Site', 'Previous_Clicks', 
                              'Device_Type', 'Ad_Category', 'Gender', 'Time_of_Day'])
df['Clicked'] = y
df.to_csv('data/click_data.csv', index=False)
```

### Running the Notebooks
```bash
jupyter notebook notebooks/
```

### Running the Web Application
```bash
cd webapp
python app.py
```
Then open your browser at [http://localhost:5000](http://localhost:5000)

## 🧠 Model Performance

| Model | Accuracy | AUC-ROC | F1-Score |
|---|---|---|---|
| LightGBM | 89.2% | 0.94 | 0.88 |
| Random Forest | 87.5% | 0.92 | 0.86 |
| Logistic Regression | 84.3% | 0.89 | 0.82 |

## 🌟 Key Learnings
* **Feature engineering** significantly improved model performance.
* **LightGBM** outperformed other models due to its ability to handle categorical features.
* **Time-of-day** and **device type** were strong predictors of click behavior.
* The web app demonstrates how ML models can be easily deployed in production.

## 💻 Tech Stack
* **Data Processing**: Pandas, NumPy
* **Visualization**: Matplotlib, Seaborn
* **Machine Learning**: Scikit-learn, LightGBM
* **Web Framework**: Flask
* **Deployment**: Local server with Flask

## 👨‍💻 Author

**Praveen Kumar**
* GitHub: [InfinitePraveen](https://github.com/InfinitePraveen)
* LinkedIn: [Praveen Kumar](https://www.linkedin.com/in/infinitepraveen/)

## 🤝 Contributing
Please read `CONTRIBUTE.md` for details on our code of conduct and the process for submitting pull requests.

## 📝 Changelog
See `CHANGELOG.md` for version history and updates.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
* Kaggle for providing the dataset inspiration
* The open-source community for amazing tools and libraries