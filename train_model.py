"""
train_model.py — Train the spam detection model and save artifacts.

Extracted from Mail_Spam.ipynb with a critical bug fix:
  Original notebook: model.fit(X_train_features, X_train)  ← WRONG
  Fixed version:     model.fit(X_train_features, Y_train)  ← CORRECT

Usage:
    python train_model.py
"""

import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def train():
    # ── 1. Load data ──────────────────────────────────────────────
    print("📂 Loading dataset...")
    mail_dataset = pd.read_csv("mail_data.csv")
    print(f"   Dataset shape: {mail_dataset.shape}")
    print(f"   Null values:\n{mail_dataset.isnull().sum()}\n")

    # ── 2. Label encoding: spam → 0, ham → 1 ─────────────────────
    mail_dataset.loc[mail_dataset["Category"] == "spam", "Category"] = 0
    mail_dataset.loc[mail_dataset["Category"] == "ham", "Category"] = 1

    X = mail_dataset["Message"]
    Y = mail_dataset["Category"]

    # ── 3. Train / test split ─────────────────────────────────────
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=2
    )
    print(f"   Train size: {X_train.shape[0]}  |  Test size: {X_test.shape[0]}\n")

    # ── 4. TF-IDF vectorisation ───────────────────────────────────
    print("🔤 Fitting TF-IDF vectorizer...")
    feature_extraction = TfidfVectorizer(
        min_df=1, stop_words="english", lowercase=True
    )
    X_train_features = feature_extraction.fit_transform(X_train)
    X_test_features = feature_extraction.transform(X_test)

    # Convert labels to int
    Y_train = Y_train.astype(int)
    Y_test = Y_test.astype(int)

    # ── 5. Train Logistic Regression ──────────────────────────────
    print("🤖 Training Logistic Regression model...")
    model = LogisticRegression()
    model.fit(X_train_features, Y_train)  # BUG FIX: was X_train in notebook

    # ── 6. Evaluate ───────────────────────────────────────────────
    train_acc = accuracy_score(Y_train, model.predict(X_train_features))
    test_acc = accuracy_score(Y_test, model.predict(X_test_features))
    print(f"\n✅ Training accuracy : {train_acc:.4f}")
    print(f"✅ Testing accuracy  : {test_acc:.4f}")

    # ── 7. Save artifacts ─────────────────────────────────────────
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open("vectorizer.pkl", "wb") as f:
        pickle.dump(feature_extraction, f)

    print("\n💾 Saved: model.pkl, vectorizer.pkl")
    print("🎉 Training complete!")


if __name__ == "__main__":
    train()
