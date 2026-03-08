import pandas as pd
import os
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MultiLabelBinarizer

# -----------------------------
# Project directory
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dataset_path = os.path.join(BASE_DIR, "dataset", "symptoms_dataset.csv")

print("Dataset path:", dataset_path)

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(dataset_path)

print("Dataset loaded successfully")

# -----------------------------
# Extract symptoms columns
# -----------------------------
symptom_columns = df.columns[1:]

# Convert symptoms into list
symptoms = df[symptom_columns].values.tolist()

# Remove empty values
symptoms = [[s for s in row if pd.notna(s)] for row in symptoms]

# -----------------------------
# Convert symptoms -> binary
# -----------------------------
mlb = MultiLabelBinarizer()

X = mlb.fit_transform(symptoms)

y = df["Disease"]

print("Total symptoms detected:", len(mlb.classes_))

# -----------------------------
# Train model
# -----------------------------
model = DecisionTreeClassifier()

model.fit(X, y)

print("Model training complete")

# -----------------------------
# Save model
# -----------------------------
models_dir = os.path.join(BASE_DIR, "models")

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

model_file = os.path.join(models_dir, "disease_model.pkl")
encoder_file = os.path.join(models_dir, "symptom_encoder.pkl")

joblib.dump(model, model_file)
joblib.dump(mlb, encoder_file)

print("✅ Model saved:", model_file)
print("✅ Encoder saved:", encoder_file)