# 🧠 ML-Based Cognitive Load Detection System

A real-time cognitive load detection system that analyzes user behavior — typing speed, mouse movement, and error rate — to classify mental workload levels (High/Low) using Machine Learning.

## 📌 Features
- ⌨️ Real-time behavioral tracking — typing speed, mouse movement, error rate
- 📊 Automated data collection pipeline storing metrics in CSV datasets
- 🤖 Random Forest ML model to classify cognitive load (High / Low)
- 🌐 Flask-based web interface for live prediction
- 🔧 Feature engineering & data preprocessing for improved model accuracy
- 📈 Model evaluation with performance metrics

## 🛠️ Tech Stack
| Category | Technology |
|---|---|
| Language | Python |
| ML Library | Scikit-Learn |
| Data Processing | Pandas |
| Behavioral Tracking | Pynput |
| Web Interface | Flask |
| Data Storage | CSV Files |

## ⚙️ Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/tejpratapsingh00/ML-Based-Cognitive-load-detection-
cd ML-Based-Cognitive-load-detection-

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Collect behavioral data
python data_collection.py

# 5. Train the model
python train_model.py

# 6. Run the Flask web app
python app.py
```

## 🧪 How It Works
1. **Data Collection** — `Pynput` tracks typing speed, mouse speed, and error rate in real time
2. **Preprocessing** — Raw data is cleaned and feature-engineered using Pandas
3. **Model Training** — Random Forest classifier trained on collected behavioral data
4. **Prediction** — Flask web app takes live input and predicts cognitive load level

## 📁 Project Structure
```
ML-Based-Cognitive-load-detection-/
├── data/
│   └── behavioral_data.csv
├── model/
│   └── random_forest_model.pkl
├── templates/
│   └── index.html
├── data_collection.py
├── train_model.py
├── app.py
└── requirements.txt
## 👤 Author
**Tej Pratap Singh**
- GitHub: [@tejpratapsingh00](https://github.com/tejpratapsingh00)
- LinkedIn: [tej-pratap-singh](https://www.linkedin.com/in/tejpratapsingh00/)
