# 📡 Spam Scanner

A Streamlit web app that scans incoming messages and classifies them as **Spam** or **Ham** using a trained machine learning model — complete with confidence scores and flagged-word highlighting.

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-app-ff4b4b)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- 🔍 **Instant classification** — paste any message and get a Spam/Ham verdict
- 📊 **Confidence score** — shows how sure the model is about its prediction
- 🚩 **Flagged terms** — highlights the specific words that pushed a message toward Spam (when the model supports it)
- 🕓 **Session history** — keeps track of your last few scans
- 🎛️ **Quick examples** — one-click sample messages to demo the app instantly
- 🖥️ **Custom UI** — terminal/scanner-inspired theme, built entirely with Streamlit + custom CSS

## Demo

![Spam Scanner Screenshot](https://github.com/yatharthgour-dot/Spam_detection-model/blob/main/screenshot/Screenshot%202026-06-24%20142803.png)

> Add a screenshot of the running app here — replace `docs/screenshot.png` with your own image.

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [scikit-learn](https://scikit-learn.org/) — model + vectorizer
- [joblib](https://joblib.readthedocs.io/) — model serialization

## Project Structure

```
spam-scanner/
├── app.py                  # Streamlit app
├── requirements.txt        # Python dependencies
├── model/
│   ├── spam_model.pkl       # Trained classifier (not included — add your own)
│   └── vectorizer.pkl       # Fitted text vectorizer (not included — add your own)
└── README.md
```

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/spam-scanner.git
cd spam-scanner
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your trained model

Place your trained model and vectorizer inside the `model/` folder:

```
model/spam_model.pkl
model/vectorizer.pkl
```

These should be created with `joblib.dump()` after training a classifier (e.g. `LogisticRegression`, `MultinomialNB`, or similar) on a vectorized text dataset (e.g. `TfidfVectorizer` or `CountVectorizer`).

### 4. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## How It Works

1. The message you enter is transformed into numeric features using the same vectorizer the model was trained on.
2. The trained model predicts whether the message is **Spam** (`1`) or **Ham** (`0`).
3. If the model exposes word-level weights (e.g. via `coef_` for linear models or `feature_log_prob_` for Naive Bayes), the app surfaces the words in your message that contributed most to a Spam classification.

## Example Messages to Try

**Likely Spam**
- "Congratulations! You've won a FREE iPhone 15. Click here within 24 hours to claim your prize!!!"
- "URGENT: Your account has been suspended. Verify your details now to restore access."

**Likely Ham**
- "Hey, can you send me the slides from yesterday's meeting when you get a chance?"
- "Reminder: dentist appointment tomorrow at 10am."

## Roadmap / Ideas

- [ ] Add model retraining from the UI
- [ ] Support batch scanning via CSV upload
- [ ] Deploy to Streamlit Community Cloud
- [ ] Add unit tests for prediction logic

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to open a PR or issue.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
