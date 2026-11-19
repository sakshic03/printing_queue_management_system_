
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/shops")
def shops():
    return render_template("shops.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")
@app.route("/print-options")
def print_options():
    return render_template("print_options.html")
@app.route("/order-summary")
def order_summary():
    return render_template("order_summary.html")
@app.route("/token")
def token():
    return render_template("token.html")
@app.route("/track-order")
def track_order():
    return render_template("track_order.html")


@app.route("/admin")
def admin():
    return render_template("admin_dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
