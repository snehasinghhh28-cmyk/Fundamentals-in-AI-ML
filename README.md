# Fundamentals-in-AI-ML
AI-Guard Password Generator is a Streamlit-based web app that uses a Random Forest machine learning model to generate and evaluate password strength.   It analyzes features like length, character types, and entropy to classify passwords as weak, medium, or strong.
> Xhit Sin:
# 🔒 AI-Guard Password Generator

AI-Guard Password Generator is a Streamlit-based web application that uses a Random Forest Machine Learning model to generate and evaluate passwords. Unlike traditional password checkers that only depend on fixed rules such as *“must contain a number”* or *“must include a special character,”* this project uses feature engineering and AI prediction to classify passwords as Weak, Medium, or Strong.

The main purpose of this project is to demonstrate how Artificial Intelligence, Machine Learning, Mathematics, and Cybersecurity concepts can work together in one practical application. It is especially useful for students, beginners, and developers who want to understand how password analysis can move beyond simple rule-based validation.

## ✨ Key Features

- AI-based password strength detection
- Random password generation
- Feature extraction from passwords
- Entropy-based randomness analysis
- Interactive Streamlit user interface
- Custom password testing section

## ⚙️ How the Project Works

The application is divided into several logical parts:

### 1. Feature Engineering
The function extract_features(password) converts each password into numerical values so that the machine learning model can understand it. These features include:

- Length of the password
- Count of lowercase letters
- Count of uppercase letters
- Count of digits
- Count of special characters
- Shannon Entropy

Since machine learning models cannot directly understand raw text like humans do, converting the password into meaningful numerical features is an important first step.

### 2. Entropy Calculation
The function calculate_entropy(password) computes the Shannon Entropy of a password.

Entropy is a mathematical measure of randomness or unpredictability.  
A password with repeated characters or simple patterns will usually have low entropy, while a password containing diverse and unpredictable characters will have higher entropy.

For example:

- password123 → lower entropy
- T#9k!Q2@Lp$7 → higher entropy

This makes entropy a very useful feature when training a password strength model.

### 3. Model Training
The train_model() function creates a synthetic dataset and trains a RandomForestClassifier.

The dataset contains three categories:

- Weak passwords: short, lowercase-only passwords
- Medium passwords: moderate-length passwords with letters and digits
- Strong passwords: longer passwords with letters, numbers, and symbols

Each generated password is passed through the feature extraction process, and then labeled as:

- 0 = Weak
- 1 = Medium
- 2 = Strong

The model learns patterns from these examples and later predicts the strength of new passwords.

### 4. Password Generation
The function generate_candidate(length) creates random password candidates using:

- Uppercase letters
- Lowercase letters
- Digits
- Special characters

The app generates multiple candidates and sends each one to the AI model for evaluation. If the model predicts a password as Strong, the app selects it immediately. Otherwise, it keeps the best available result.

### 5. User Interface with Streamlit
The project uses Streamlit to provide a clean and interactive web interface.  
Users can:

- Select a password length using a slider
- Generate an AI-verified password
- View the strength result in a styled card
- See explainable metrics like:
  - Length
  - Special character count
  - Entropy score
- Test their own passwords in the “Test Your Own Password” section

This makes the application both practical and easy to understand.

## 🧠 Why Use AI Instead of Only Rules?

Traditional password validation systems often use simple conditions such as:

- Minimum 8 characters
- At least one uppercase letter
- At least one digit
- At least one special character

While these rules are helpful, they do not always reflect actual password strength.  
For example, a password like Password1! may satisfy many rules but is still predictable.

> Xhit Sin:
This project uses Machine Learning to analyze multiple features together and make a smarter decision. The AI model learns from examples instead of relying only on fixed if/else conditions.

## 🛠 Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Random
- String
- Math

## ▶️ How to Run the Project

### 1. Install the required libraries
```bash
pip install streamlit pandas numpy scikit-learn
