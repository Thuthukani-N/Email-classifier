# 🔐 Email Scam Detection NLP Project

This project detects whether an email is **suspicious** or **safe** using Natural Language Processing (NLP).

I trained three models:
- **Logistic Regression** → 99.2% accuracy ✅ (chosen model)
- **Naive Bayes** → 97% accuracy
- **LSTM** → 99.7% accuracy but overfitted

The app is built using **Streamlit**, and the model and vectorizer are saved using **Joblib**.

---

## 📂 Files in This Project

| File | Description |
|------|--------------|
| `app.py` | The Streamlit web app |
| `NLP Model.ipynb` | Jupyter notebook where the models were trained |
| `NLP_Model2.pkl` | Saved Logistic Regression model |
| `vectorizer2.pkl` | Saved vectorizer |
| `requirements.txt` | Libraries used |
| `.gitignore` | Files to exclude when uploading |
| `Datasets/README.txt` | Contains the link to the dataset |

---

## 📊 Dataset

The dataset used for training comes from:  
🔗 [https://zenodo.org/records/8339691](https://zenodo.org/records/8339691)

---

## ⚙️ How to Run It

To run this project on your local machine, follow the steps below:

```bash
# 1️⃣ Clone this repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# 2️⃣ Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # On Windows
# or
source venv/bin/activate   # On Mac/Linux

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run the Streamlit app
streamlit run app.py

👤 Author

Thuthukani Nhlengethwa
💡 Built for educational and cybersecurity awareness purposes.