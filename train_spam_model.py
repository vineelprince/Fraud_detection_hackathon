import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Load dataset
data = pd.read_csv("spam.csv", encoding="latin-1")

# Rename columns
data = data[["v1", "v2"]]
data.columns = ["label", "text"]

# Convert labels
data["label"] = data["label"].map({"ham": 0, "spam": 1})

X = data["text"]
y = data["label"]

# Vectorization
vectorizer = TfidfVectorizer(stop_words="english")
X_vec = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression()
model.fit(X_vec, y)

# Save model
joblib.dump(model, "spam_model.pkl")
joblib.dump(vectorizer, "spam_vectorizer.pkl")

print("✅ Spam model trained and saved successfully")

