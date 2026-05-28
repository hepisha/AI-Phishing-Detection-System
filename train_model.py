import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

print("=" * 50)
print("  AI Phishing Detection - Model Training")
print("=" * 50)

# Load dataset
df = pd.read_csv("dataset/sample_emails.csv")
print(f"\n[+] Dataset loaded: {len(df)} samples")
print(f"    - Phishing emails : {len(df[df['label']==1])}")
print(f"    - Legitimate emails: {len(df[df['label']==0])}")

# Features and labels
X = df["text"]
y = df["label"]

# Convert text to numerical vectors using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
X_vectorized = vectorizer.fit_transform(X)
print(f"\n[+] TF-IDF Vectorization complete")
print(f"    - Vocabulary size: {len(vectorizer.vocabulary_)} words")

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=42
)
print(f"\n[+] Dataset split:")
print(f"    - Training samples : {X_train.shape[0]}")
print(f"    - Testing samples  : {X_test.shape[0]}")

# Train Logistic Regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
print(f"\n[+] Model trained: Logistic Regression")

# Test accuracy
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"\n[+] Model Performance:")
print(f"    - Accuracy: {accuracy * 100:.2f}%")
print(f"\n[+] Classification Report:")
print(classification_report(y_test, predictions, target_names=["Legitimate", "Phishing"]))

# Save model and vectorizer
joblib.dump(model, "phishing_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("[+] Model saved     : phishing_model.pkl")
print("[+] Vectorizer saved: vectorizer.pkl")
print("\n[✓] Training Complete! Run: streamlit run app.py")
print("=" * 50)
