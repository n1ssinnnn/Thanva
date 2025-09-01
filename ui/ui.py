from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("login"))  # เปลี่ยนหน้าแรกให้พาไปหน้า login

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # ดึงค่าจากฟอร์ม
        username = request.form["username"]
        password = request.form["password"]
        # TODO: ตรวจสอบผู้ใช้
        return redirect(url_for("home"))  # หรือไปหน้าอื่นหลัง Login
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
