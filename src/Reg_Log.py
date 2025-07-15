import sqlite3 as sql

conn = sql.connect('database/Databases.db')
db = conn.cursor()

def register(name, student_code, password):
    conn = sql.connect("database/Databases.db")
    db = conn.cursor()

    # ตรวจสอบว่า student_code นี้มีอยู่แล้วหรือยัง
    db.execute("SELECT * FROM account WHERE Student_code = ?", (student_code,))
    existing = db.fetchone()

    if existing:
        print("❌ Error: Student code already registered!")
    else:
        try:
            db.execute(
                "INSERT INTO account (Name, Student_code, Password) VALUES (?, ?, ?)",
                (name, student_code, password)
            )
            conn.commit()
            print("✅ Register success!")
        except sql.IntegrityError as e:
            print("❌ Integrity Error:", e)
    conn.close()

def login(identifier, password):

        # Identifier need to be string format

    conn = sql.connect("database/Databases.db")
    db = conn.cursor()
    
    # ลองใช้ identifier เป็น Student_code (เช็คว่าเป็นตัวเลขหรือไม่)
    if identifier.isdigit():
        db.execute(
            "SELECT * FROM account WHERE Student_code = ? AND Password = ?",
            (int(identifier), password)
        )
    else:
        db.execute(
            "SELECT * FROM account WHERE Name = ? AND Password = ?",
            (identifier, password)
        )

    user = db.fetchone()
    conn.close()

    if user:
        print(f"✅ Login successful! Welcome, {user[0]} (code: {user[1]})")
    else:
        print("❌ Login failed: Incorrect username/code or password")