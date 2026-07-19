# 📧 Mail Spam Detection Web Application

A modern, responsive web application for classifying email messages as **Spam** or **Ham (Safe)** using Machine Learning (**Logistic Regression** with **TF-IDF Vectorisation**). 

Built with **Flask**, **scikit-learn**, **HTML5**, **CSS3**, and **Vanilla JavaScript** (AJAX-based, zero page reloads).

---

## 🚀 Features

- 🔍 **Real-Time Classification**: Instantly detects whether an email message is **Ham** (Legitimate) or **Spam**.
- ⚡ **AJAX Integration**: Asynchronous API call ensures seamless prediction without refreshing the page.
- 🎨 **Modern & Responsive UI**: Premium dark glassmorphism design with animated particles, smooth micro-interactions, responsive grid layout, and keyboard shortcuts (`Ctrl/Cmd + Enter`).
- 📊 **High Model Accuracy**:
  - **Training Accuracy**: ~96.86%
  - **Testing Accuracy**: ~95.34%
- 🐞 **Fixed Jupyter Notebook Bug**: Corrected the original training logic where `model.fit()` was inadvertently called on features instead of labels.

---

## 📁 Project Structure

```
mail-spam-detector/
│
├── app.py                # Flask web server & prediction API endpoint (/predict)
├── train_model.py        # ML pipeline script to train model & save pickle files
├── mail_data.csv         # Dataset containing 5,572 labeled email/SMS messages
├── model.pkl             # Trained Logistic Regression model artifact
├── vectorizer.pkl        # Fitted TF-IDF Vectorizer artifact
│
├── templates/
│   └── index.html        # Main HTML layout with semantic structure & metadata
│
├── static/
│   ├── style.css         # Glassmorphism design system & CSS animations
│   └── script.js          # Client-side AJAX prediction & UI interaction script
│
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🐛 Bug Fix Explanation (Jupyter Notebook vs train_model.py)

In the original `Mail_Spam.ipynb`, cell `[41]` contained the following line:
```python
# ❌ INCORRECT (Notebook):
model.fit(X_train_features, X_train)
```
Passing continuous string text (`X_train`) as target `y` resulted in scikit-learn treating each unique sentence as a separate target class, leading to a target shape error and **0.0% evaluation accuracy**.

In `train_model.py`, this was fixed to pass encoded target labels (`Y_train`):
```python
# ✅ FIXED (train_model.py):
model.fit(X_train_features, Y_train)
```
This restored the model to its full **95.34% test accuracy**.

---

## 🛠️ How to Run Locally

### 1. Clone or Open Project Directory
Navigate to the project directory in your terminal:
```bash
cd mail-spam-detector
```

### 2. Set Up Virtual Environment (Optional but Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate on macOS/Linux:
source venv/bin/activate

# Activate on Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the Model (Optional)
The pre-trained `model.pkl` and `vectorizer.pkl` files are already generated. If you wish to retrain from `mail_data.csv`:
```bash
python train_model.py
```
*Output:*
```text
📂 Loading dataset...
   Dataset shape: (5572, 2)
   Train size: 4457  |  Test size: 1115

🔤 Fitting TF-IDF vectorizer...
🤖 Training Logistic Regression model...

✅ Training accuracy : 0.9686
✅ Testing accuracy  : 0.9534

💾 Saved: model.pkl, vectorizer.pkl
```

### 5. Launch the Flask App
```bash
python app.py
```

Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🎯 Usage Guide

1. Open `http://127.0.0.1:5000` in your web browser.
2. Enter or paste any email/message text into the text area.
3. Click **Analyze Email** (or press `Ctrl + Enter` / `Cmd + Enter`).
4. The result card will display whether the email is **Safe (Ham)** or **Spam** along with the model's confidence percentage.
