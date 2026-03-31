import streamlit as st
import pandas as pd
import numpy as np
import random
import string
import math
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# ==========================================
# PART 1: AIML FUNDAMENTALS (Feature Engineering)
# ==========================================

def calculate_entropy(password):
    """
    Calculates the Shannon Entropy of the password.
    Entropy is a measure of randomness/unpredictability.
    """
    if not password:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(password.count(chr(x))) / len(password)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

def extract_features(password):
    """
    Converts a text password into numerical features for the AI model.
    """
    return [
        len(password),                          # Feature 1: Length
        sum(c.islower() for c in password),     # Feature 2: Lowercase count
        sum(c.isupper() for c in password),     # Feature 3: Uppercase count
        sum(c.isdigit() for c in password),     # Feature 4: Numeric count
        sum(c in string.punctuation for c in password), # Feature 5: Special char count
        calculate_entropy(password)             # Feature 6: Entropy (Math based randomness)
    ]

# ==========================================
# PART 2: TRAINING THE AI MODEL (Simulation)
# ==========================================

@st.cache_resource # Caches the model so we don't retrain on every click
def train_model():
    """
    Generates a synthetic dataset and trains a Random Forest Classifier.
    In a massive production app, you would load a dataset of real leaked passwords.
    Here, we generate patterns to teach the AI what 'good' looks like.
    """
    data = []
    labels = []
    
    # 1. Generate Weak Passwords (short, repetitive, lowercase only)
    for _ in range(500):
        p = "".join(random.choices(string.ascii_lowercase, k=random.randint(4, 8)))
        data.append(extract_features(p))
        labels.append(0) # 0 = Weak

    # 2. Generate Medium Passwords (mixed case, numbers, medium length)
    for _ in range(500):
        p = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(8, 10)))
        data.append(extract_features(p))
        labels.append(1) # 1 = Medium

    # 3. Generate Strong Passwords (long, symbols, high entropy)
    for _ in range(500):
        chars = string.ascii_letters + string.digits + string.punctuation
        p = "".join(random.choices(chars, k=random.randint(12, 16)))
        data.append(extract_features(p))
        labels.append(2) # 2 = Strong

    # Train Model
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(data, labels)
    return clf

# Load the model
model = train_model()

# ==========================================
# PART 3: GENERATOR LOGIC
# ==========================================

def generate_candidate(length=12):
    """Generates a random candidate string."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(chars) for _ in range(length))

def get_ai_prediction(password):
    """Uses the trained model to predict strength."""
    features = np.array([extract_features(password)])
    prediction = model.predict(features)[0]
    return prediction

# ==========================================
# PART 4: SIMPLE UI/UX (Streamlit)
# ==========================================

# Set page config
st.set_page_config(page_title="AI-Guard Password", page_icon="🔒", layout="centered")

# Custom CSS for a clean look
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 20px;
    }
    .result-card {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🔒 AI-Guard Password Generator")
st.write("This tool uses a **Random Forest Machine Learning model** to analyze password complexity features (Entropy, Length, Character types) rather than simple if/else rules.")

# Input Section
length = st.slider("Select Password Length", min_value=6, max_value=24, value=14)

# Action
if st.button("Generate AI-Verified Password"):
    
    # We generate candidates until the AI is satisfied or we hit a limit
    best_password = ""
    best_score = -1
    
    # Attempt to find a strong password
    for _ in range(10): # Try 10 times to find a 'Strong' one
        candidate = generate_candidate(length)
        score = get_ai_prediction(candidate)
        
        if score > best_score:
            best_score = score
            best_password = candidate
        
        if score == 2: # If AI says it's Strong, stop looking
            break

    # Display Result
    st.markdown("---")
    
    color = "red"
    label = "Weak"
    
    if best_score == 1:
        color = "orange"
        label = "Medium"
    elif best_score == 2:
        color = "#2ecc71" # Green
        label = "Strong"
        
    st.markdown(f"""
    <div class="result-card" style="background-color: {color}20; border: 2px solid {color};">
        <h3 style="color:{color};">{label} Password Detected</h3>
        <code style="font-size: 24px; color: black; background: transparent;">{best_password}</code>
    </div>
    """, unsafe_allow_html=True)
    
    # Explainability (Why did the AI choose this?)
    st.subheader("📊 Why does the AI like this?")
    feats = extract_features(best_password)
    col1, col2, col3 = st.columns(3)
    col1.metric("Length", feats[0])
    col2.metric("Special Chars", feats[4])
    col3.metric("Entropy Score", f"{feats[5]:.2f}")

# User Testing Section
st.markdown("---")
st.subheader("🧪 Test Your Own Password")
user_pass = st.text_input("Type a password to see what the AI thinks:", type="password")

if user_pass:
    score = get_ai_prediction(user_pass)
    if score == 0:
        st.error("AI Prediction: WEAK ❌")
    elif score == 1:
        st.warning("AI Prediction: MEDIUM ⚠️")
    else:
        st.success("AI Prediction: STRONG ✅")