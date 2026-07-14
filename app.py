from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

app = Flask(__name__)
app.secret_key = "EduAgent2026"

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Database
db.init_app(app)

# Create Database Tables
with app.app_context():
    db.create_all()

# ---------------- Routes ----------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session["user_id"] = user.id
            session["user_name"] = user.name

            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match!"

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already exists!"

        hashed_password = generate_password_hash(password)

        new_user = User(
          name=name,
        email=email,
          password=hashed_password
         )

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


# ----------------------------------------

if __name__ == "__main__":
    app.run(debug=True)    