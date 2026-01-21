from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# ------------------ MONGODB CONNECTION ------------------

import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)
db = client["password_checker"]

users_collection = db["users"]
dataset_collection = db["dataset"]   # common weak words dataset

# ------------------ RULE BASED CHECK ------------------

def strength_check(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for c in password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Moderate"
    else:
        return "Strong"

# ------------------ DATASET CHECK ------------------

def dataset_check(password):
    password = password.lower()

    for item in dataset_collection.find({}, {"word": 1}):
        if item["word"] in password:
            return True

    return False

# ------------------ PERSONAL INFO CHECK ------------------

def personal_data_check(password, first, last, birth):
    password = password.lower()

    if first and first.lower() in password:
        return True

    if last and last.lower() in password:
        return True

    if birth:
        year = birth.split("-")[0]
        if year in password:
            return True

    return False

# ------------------ ROUTES ------------------

# 🔥 MAIN PAGE → USER DETAIL FORM (Extreme Checker)
@app.route("/", methods=["GET"])
def user_page():
    return render_template("user_detail.html")

# 🔥 USER DETAIL + MODE BASED CHECK
@app.route("/check_user", methods=["POST"])
def check_user():

    first = request.form.get("first_name", "")
    last = request.form.get("last_name", "")
    birth = request.form.get("birth_date", "")
    password = request.form.get("password")
    mode = request.form.get("mode")   # normal / extreme

    rule_strength = strength_check(password)
    final = rule_strength

    if mode == "extreme":
        dataset_match = dataset_check(password)
        personal_match = personal_data_check(password, first, last, birth)

        if dataset_match or personal_match:
            final = "Weak"

    # Save only if not weak
    if final != "Weak":
        users_collection.insert_one({
            "first_name": first,
            "last_name": last,
            "birth_date": birth
        })

    print("Final Strength:", final)

    return render_template("user_detail.html", result=final)

# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(debug=True)
