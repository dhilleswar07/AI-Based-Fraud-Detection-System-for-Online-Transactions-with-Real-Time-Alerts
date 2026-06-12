<<<<<<< HEAD
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_mail import Mail, Message
from datetime import datetime


import sqlite3
import joblib
import pandas as pd
import random
import traceback

app = Flask(__name__)
app.secret_key = "super_secret"

# -----------------------------
# LOAD MODEL & SCALER
# -----------------------------
model = joblib.load("fraud_model.pkl")
scaler = joblib.load("scaler.pkl")

# -----------------------------
# LOAD DATASET FOR SIMULATION
# -----------------------------
dataset = pd.read_csv("creditcard.csv")

if "Class" in dataset.columns:
    dataset = dataset.drop("Class", axis=1)

if "Time" in dataset.columns:
    dataset = dataset.drop("Time", axis=1)

# -----------------------------
# EMAIL CONFIG
# -----------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "realtime.fraud.alerts@gmail.com"
app.config['MAIL_PASSWORD'] = "swshnjmydqgxjqhu"
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)

# -----------------------------
# INITIALIZE DATABASE
# -----------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            ip TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -----------------------------
# LOGIN SYSTEM
# -----------------------------
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "dhilleswar07" and request.form["password"] == "vijay@2005":
            login_user(User(1))
            return redirect("/dashboard")
    return render_template("login.html")

# -----------------------------
# DASHBOARD
# -----------------------------
@app.route("/dashboard", methods=["GET","POST"])
@login_required
def dashboard():
    if request.method == "POST":
        amount = float(request.form["amount"])
        ip = request.remote_addr

        random_row = dataset.sample(n=1).copy()
        random_row["Amount"] = amount

        df_scaled = scaler.transform(random_row)

        pred = model.predict(df_scaled)[0]
        probability = model.predict_proba(df_scaled)[0][1]

        # pred = 1
        # probability = 0.91
        
        fraud_percent = round(probability * 100, 2)

        if fraud_percent < 30:
            risk_level = "LOW"
        elif fraud_percent < 70:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        status = "FRAUD" if pred == 1 else "SAFE"

        # -----------------------------
        # SEND EMAIL IF FRAUD
        # -----------------------------

        if status == "FRAUD":
            try:
                print("Attempting to send styled fraud email...")

                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                msg = Message(
                    subject="🚨 Fraud Alert – High Risk Transaction Detected",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=["dhilleswarjogivijay@gmail.com"]
                )

                msg.html = f"""
                <div style="background:#111; padding:40px; font-family:Arial, sans-serif; color:#fff;">
                    <div style="max-width:500px; margin:auto; background:#1c1c1c; padding:30px; border-radius:12px; box-shadow:0 0 20px rgba(255,0,0,0.3);">
                        
                        <h2 style="color:#ff4d4d; text-align:center;">
                            🚨 Fraud Alert Notification
                        </h2>

                        <p style="color:#ccc; text-align:center;">
                            A high-risk transaction has been detected by the AI monitoring system.
                        </p>

                        <hr style="border:0; border-top:1px solid #333; margin:20px 0;">

                        <table width="100%" style="color:#fff; font-size:15px;">
                            <tr>
                                <td><strong>Amount</strong></td>
                                <td style="text-align:right;">₹{amount}</td>
                            </tr>
                            <tr>
                                <td><strong>Fraud Probability</strong></td>
                                <td style="text-align:right;">{fraud_percent}%</td>
                            </tr>
                            <tr>
                                <td><strong>Risk Level</strong></td>
                                <td style="text-align:right; color:#ff4d4d; font-weight:bold;">
                                    {risk_level}
                                </td>
                            </tr>
                            <tr>
                                <td><strong>IP Address</strong></td>
                                <td style="text-align:right;">{ip}</td>
                            </tr>
                            <tr>
                                <td><strong>Time</strong></td>
                                <td style="text-align:right;">{current_time}</td>
                            </tr>
                        </table>

                        <hr style="border:0; border-top:1px solid #333; margin:20px 0;">

                        <p style="color:#aaa; font-size:14px;">
                            This transaction has been automatically flagged for security review.
                        </p>

                        <p style="color:#777; font-size:13px; margin-top:30px;">
                            AI Fraud Detection System<br>
                            Real-Time Monitoring Engine
                        </p>

                    </div>
                </div>
                """

                mail.send(msg)
                print("Styled fraud email sent successfully!")

            except Exception as e:
                import traceback
                traceback.print_exc()

        # SAVE TO DATABASE
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO transactions (amount, ip, status) VALUES (?, ?, ?)",
            (amount, ip, status)
        )
        conn.commit()
        conn.close()

        return render_template(
            "dashboard.html",
            status=status,
            fraud_percent=fraud_percent,
            risk_level=risk_level
        )

    return render_template("dashboard.html", status=None)

# -----------------------------
# MANUAL FEATURE PREDICTION
# -----------------------------
@app.route("/manual_predict", methods=["GET", "POST"])
@login_required
def manual_predict():
    autofill = None
    status = None
    fraud_percent = None
    risk_level = None

    if request.method == "POST":
        feature_cols = list(dataset.columns)
        input_values = [float(request.form.get(col, 0)) for col in feature_cols]

        input_df = pd.DataFrame([input_values], columns=feature_cols)
        scaled_data = scaler.transform(input_df)

        pred = model.predict(scaled_data)[0]
        probability = model.predict_proba(scaled_data)[0][1]

        fraud_percent = round(probability * 100, 2)
        status = "FRAUD" if pred == 1 else "SAFE"

        if fraud_percent < 30:
            risk_level = "LOW"
        elif fraud_percent < 70:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        # Send email if fraud (manual page)

        if status == "FRAUD":
            try:
                print("Attempting to send styled fraud email...")

                # ✅ Define missing variables
                amount = float(request.form.get("Amount", 0))
                ip = request.remote_addr
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                msg = Message(
                    subject="🚨 Fraud Alert – High Risk Transaction Detected",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=["dhilleswarjogivijay@gmail.com"]
                )

                msg.html = f"""
                <div style="background:#111; padding:40px; font-family:Arial, sans-serif; color:#fff;">
                    <div style="max-width:500px; margin:auto; background:#1c1c1c; padding:30px; border-radius:12px;">
                        <h2 style="color:#ff4d4d; text-align:center;">
                            🚨 Fraud Alert Notification
                        </h2>

                        <p style="color:#ccc; text-align:center;">
                            A high-risk transaction has been detected.
                        </p>

                        <table width="100%" style="color:#fff; font-size:15px;">
                            <tr>
                                <td><strong>Amount</strong></td>
                                <td style="text-align:right;">₹{amount}</td>
                            </tr>
                            <tr>
                                <td><strong>Fraud Probability</strong></td>
                                <td style="text-align:right;">{fraud_percent}%</td>
                            </tr>
                            <tr>
                                <td><strong>Risk Level</strong></td>
                                <td style="text-align:right; color:#ff4d4d; font-weight:bold;">
                                    {risk_level}
                                </td>
                            </tr>
                            <tr>
                                <td><strong>IP Address</strong></td>
                                <td style="text-align:right;">{ip}</td>
                            </tr>
                            <tr>
                                <td><strong>Time</strong></td>
                                <td style="text-align:right;">{current_time}</td>
                            </tr>
                        </table>
                    </div>
                </div>
                """

                mail.send(msg)
                print("Styled fraud email sent successfully!")

            except Exception as e:
                traceback.print_exc()

    return render_template(
        "manual_predict.html",
        autofill=autofill,
        status=status,
        fraud_percent=fraud_percent,
        risk_level=risk_level
    )

# -----------------------------
# AUTO FILL
# -----------------------------
@app.route("/auto_fill")
@login_required
def auto_fill():
    full_dataset = pd.read_csv("creditcard.csv")

    fraud_rows = full_dataset[full_dataset['Class'] == 1]
    safe_rows = full_dataset[full_dataset['Class'] == 0]

    row = fraud_rows.sample(n=1) if random.random() < 0.5 else safe_rows.sample(n=1)

    for col in ['Class', 'Time']:
        if col in row.columns:
            row = row.drop(col, axis=1)

    feature_dict = row.to_dict(orient="records")[0]

    return render_template("manual_predict.html", autofill=feature_dict)

# -----------------------------
# ADMIN PANEL
# -----------------------------
@app.route("/admin")
@login_required
def admin():

    filter_type = request.args.get("filter")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if filter_type == "fraud":
        c.execute("SELECT * FROM transactions WHERE status='FRAUD'")
    elif filter_type == "safe":
        c.execute("SELECT * FROM transactions WHERE status='SAFE'")
    else:
        c.execute("SELECT * FROM transactions")

    data = c.fetchall()
    conn.close()

    total = len(data)
    fraud_count = len([row for row in data if row[3] == "FRAUD"])
    safe_count = total - fraud_count
    fraud_percent = round((fraud_count / total) * 100, 2) if total > 0 else 0

    try:
        metrics = joblib.load("model_metrics.pkl")
    except:
        metrics = {
            "accuracy": 0,
            "precision": 0,
            "recall": 0,
            "f1": 0
        }

    fraud_chart_data = {
        "fraud": fraud_count,
        "safe": safe_count
    }

    return render_template(
        "admin.html",
        data=data,
        total=total,
        fraud_count=fraud_count,
        safe_count=safe_count,
        fraud_percent=fraud_percent,
        fraud_chart_data=fraud_chart_data,
        metrics=metrics
    )

# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
=======
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_mail import Mail, Message
from datetime import datetime


import sqlite3
import joblib
import pandas as pd
import random
import traceback

app = Flask(__name__)
app.secret_key = "super_secret"

# -----------------------------
# LOAD MODEL & SCALER
# -----------------------------
model = joblib.load("fraud_model.pkl")
scaler = joblib.load("scaler.pkl")

# -----------------------------
# LOAD DATASET FOR SIMULATION
# -----------------------------
dataset = pd.read_csv("creditcard.csv")

if "Class" in dataset.columns:
    dataset = dataset.drop("Class", axis=1)

if "Time" in dataset.columns:
    dataset = dataset.drop("Time", axis=1)

# -----------------------------
# EMAIL CONFIG
# -----------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "realtime.fraud.alerts@gmail.com"
app.config['MAIL_PASSWORD'] = "*****************************"
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)

# -----------------------------
# INITIALIZE DATABASE
# -----------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            ip TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -----------------------------
# LOGIN SYSTEM
# -----------------------------
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "dhilleswar07" and request.form["password"] == "***********":
            login_user(User(1))
            return redirect("/dashboard")
    return render_template("login.html")

# -----------------------------
# DASHBOARD
# -----------------------------
@app.route("/dashboard", methods=["GET","POST"])
@login_required
def dashboard():
    if request.method == "POST":
        amount = float(request.form["amount"])
        ip = request.remote_addr

        random_row = dataset.sample(n=1).copy()
        random_row["Amount"] = amount

        df_scaled = scaler.transform(random_row)

        pred = model.predict(df_scaled)[0]
        probability = model.predict_proba(df_scaled)[0][1]

        # pred = 1
        # probability = 0.91
        
        fraud_percent = round(probability * 100, 2)

        if fraud_percent < 30:
            risk_level = "LOW"
        elif fraud_percent < 70:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        status = "FRAUD" if pred == 1 else "SAFE"

        # -----------------------------
        # SEND EMAIL IF FRAUD
        # -----------------------------

        if status == "FRAUD":
            try:
                print("Attempting to send styled fraud email...")

                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                msg = Message(
                    subject="🚨 Fraud Alert – High Risk Transaction Detected",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=["dhilleswarjogivijay@gmail.com"]
                )

                msg.html = f"""
                <div style="background:#111; padding:40px; font-family:Arial, sans-serif; color:#fff;">
                    <div style="max-width:500px; margin:auto; background:#1c1c1c; padding:30px; border-radius:12px; box-shadow:0 0 20px rgba(255,0,0,0.3);">
                        
                        <h2 style="color:#ff4d4d; text-align:center;">
                            🚨 Fraud Alert Notification
                        </h2>

                        <p style="color:#ccc; text-align:center;">
                            A high-risk transaction has been detected by the AI monitoring system.
                        </p>

                        <hr style="border:0; border-top:1px solid #333; margin:20px 0;">

                        <table width="100%" style="color:#fff; font-size:15px;">
                            <tr>
                                <td><strong>Amount</strong></td>
                                <td style="text-align:right;">₹{amount}</td>
                            </tr>
                            <tr>
                                <td><strong>Fraud Probability</strong></td>
                                <td style="text-align:right;">{fraud_percent}%</td>
                            </tr>
                            <tr>
                                <td><strong>Risk Level</strong></td>
                                <td style="text-align:right; color:#ff4d4d; font-weight:bold;">
                                    {risk_level}
                                </td>
                            </tr>
                            <tr>
                                <td><strong>IP Address</strong></td>
                                <td style="text-align:right;">{ip}</td>
                            </tr>
                            <tr>
                                <td><strong>Time</strong></td>
                                <td style="text-align:right;">{current_time}</td>
                            </tr>
                        </table>

                        <hr style="border:0; border-top:1px solid #333; margin:20px 0;">

                        <p style="color:#aaa; font-size:14px;">
                            This transaction has been automatically flagged for security review.
                        </p>

                        <p style="color:#777; font-size:13px; margin-top:30px;">
                            AI Fraud Detection System<br>
                            Real-Time Monitoring Engine
                        </p>

                    </div>
                </div>
                """

                mail.send(msg)
                print("Styled fraud email sent successfully!")

            except Exception as e:
                import traceback
                traceback.print_exc()

        # SAVE TO DATABASE
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO transactions (amount, ip, status) VALUES (?, ?, ?)",
            (amount, ip, status)
        )
        conn.commit()
        conn.close()

        return render_template(
            "dashboard.html",
            status=status,
            fraud_percent=fraud_percent,
            risk_level=risk_level
        )

    return render_template("dashboard.html", status=None)

# -----------------------------
# MANUAL FEATURE PREDICTION
# -----------------------------
@app.route("/manual_predict", methods=["GET", "POST"])
@login_required
def manual_predict():
    autofill = None
    status = None
    fraud_percent = None
    risk_level = None

    if request.method == "POST":
        feature_cols = list(dataset.columns)
        input_values = [float(request.form.get(col, 0)) for col in feature_cols]

        input_df = pd.DataFrame([input_values], columns=feature_cols)
        scaled_data = scaler.transform(input_df)

        pred = model.predict(scaled_data)[0]
        probability = model.predict_proba(scaled_data)[0][1]

        fraud_percent = round(probability * 100, 2)
        status = "FRAUD" if pred == 1 else "SAFE"

        if fraud_percent < 30:
            risk_level = "LOW"
        elif fraud_percent < 70:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        # Send email if fraud (manual page)

        if status == "FRAUD":
            try:
                print("Attempting to send styled fraud email...")

                # ✅ Define missing variables
                amount = float(request.form.get("Amount", 0))
                ip = request.remote_addr
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                msg = Message(
                    subject="🚨 Fraud Alert – High Risk Transaction Detected",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=["dhilleswarjogivijay@gmail.com"]
                )

                msg.html = f"""
                <div style="background:#111; padding:40px; font-family:Arial, sans-serif; color:#fff;">
                    <div style="max-width:500px; margin:auto; background:#1c1c1c; padding:30px; border-radius:12px;">
                        <h2 style="color:#ff4d4d; text-align:center;">
                            🚨 Fraud Alert Notification
                        </h2>

                        <p style="color:#ccc; text-align:center;">
                            A high-risk transaction has been detected.
                        </p>

                        <table width="100%" style="color:#fff; font-size:15px;">
                            <tr>
                                <td><strong>Amount</strong></td>
                                <td style="text-align:right;">₹{amount}</td>
                            </tr>
                            <tr>
                                <td><strong>Fraud Probability</strong></td>
                                <td style="text-align:right;">{fraud_percent}%</td>
                            </tr>
                            <tr>
                                <td><strong>Risk Level</strong></td>
                                <td style="text-align:right; color:#ff4d4d; font-weight:bold;">
                                    {risk_level}
                                </td>
                            </tr>
                            <tr>
                                <td><strong>IP Address</strong></td>
                                <td style="text-align:right;">{ip}</td>
                            </tr>
                            <tr>
                                <td><strong>Time</strong></td>
                                <td style="text-align:right;">{current_time}</td>
                            </tr>
                        </table>
                    </div>
                </div>
                """

                mail.send(msg)
                print("Styled fraud email sent successfully!")

            except Exception as e:
                traceback.print_exc()

    return render_template(
        "manual_predict.html",
        autofill=autofill,
        status=status,
        fraud_percent=fraud_percent,
        risk_level=risk_level
    )

# -----------------------------
# AUTO FILL
# -----------------------------
@app.route("/auto_fill")
@login_required
def auto_fill():
    full_dataset = pd.read_csv("creditcard.csv")

    fraud_rows = full_dataset[full_dataset['Class'] == 1]
    safe_rows = full_dataset[full_dataset['Class'] == 0]

    row = fraud_rows.sample(n=1) if random.random() < 0.5 else safe_rows.sample(n=1)

    for col in ['Class', 'Time']:
        if col in row.columns:
            row = row.drop(col, axis=1)

    feature_dict = row.to_dict(orient="records")[0]

    return render_template("manual_predict.html", autofill=feature_dict)

# -----------------------------
# ADMIN PANEL
# -----------------------------
@app.route("/admin")
@login_required
def admin():

    filter_type = request.args.get("filter")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if filter_type == "fraud":
        c.execute("SELECT * FROM transactions WHERE status='FRAUD'")
    elif filter_type == "safe":
        c.execute("SELECT * FROM transactions WHERE status='SAFE'")
    else:
        c.execute("SELECT * FROM transactions")

    data = c.fetchall()
    conn.close()

    total = len(data)
    fraud_count = len([row for row in data if row[3] == "FRAUD"])
    safe_count = total - fraud_count
    fraud_percent = round((fraud_count / total) * 100, 2) if total > 0 else 0

    try:
        metrics = joblib.load("model_metrics.pkl")
    except:
        metrics = {
            "accuracy": 0,
            "precision": 0,
            "recall": 0,
            "f1": 0
        }

    fraud_chart_data = {
        "fraud": fraud_count,
        "safe": safe_count
    }

    return render_template(
        "admin.html",
        data=data,
        total=total,
        fraud_count=fraud_count,
        safe_count=safe_count,
        fraud_percent=fraud_percent,
        fraud_chart_data=fraud_chart_data,
        metrics=metrics
    )

# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 996f1842a995ae8a2e317166d8f70013db368487
