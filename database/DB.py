import sqlite3 as sql

conn = sql.connect('Databases.db')
db = conn.cursor()

# Create tables

db.execute('''CREATE TABLE IF NOT EXISTS account (
    Name TEXT NOT NULL,
    Student_code INTEGER NOT NULL,
    Password INTEGER,
    UNIQUE(Name, Student_code, Password)
)''')

db.execute('''CREATE TABLE IF NOT EXISTS basic_info (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Student_code INTEGER NOT NULL,
    Math_Score INTEGER,
    Phy_Score INTEGER,
    Chem_Score INTEGER,
    Eng_Score INTEGER,
    UNIQUE(Name, Student_code)
)''')

columns = []
for i in range(1, 37):
    for letter in ['A', 'B', 'C', 'D', 'E']:
        col_name = f'"{i}{letter}" INTEGER'
        columns.append(col_name)

column_definitions = ",\n    ".join(columns)

db.execute(f'''CREATE TABLE IF NOT EXISTS answer (
    Name TEXT NOT NULL,
    Student_code INTEGER NOT NULL,
    Subject TEXT NOT NULL,
    {column_definitions},
    UNIQUE(Name, Student_code, Subject),
    FOREIGN KEY (Name, Student_code) REFERENCES basic_info(Name, Student_code)
)''')

conn.commit()

#Insert data function

def insert_data(name, student_code, subject, math_score=None, phy_score=None, chem_score=None, eng_score=None):
    conn = sql.connect('Databases.db')
    db = conn.cursor()

    db.execute("INSERT OR IGNORE INTO basic_info (Name, Student_code) VALUES (?, ?)", (name, student_code))

    if subject == 'Mathematics':
        db.execute("UPDATE basic_info SET Math_Score = ? WHERE Name = ? AND Student_code = ?", (math_score, name, student_code))
    elif subject == 'Physics':
        db.execute("UPDATE basic_info SET Phy_Score = ? WHERE Name = ? AND Student_code = ?", (phy_score, name, student_code))
    elif subject == 'Chemistry':
        db.execute("UPDATE basic_info SET Chem_Score = ? WHERE Name = ? AND Student_code = ?", (chem_score, name, student_code))
    elif subject == 'English':
        db.execute("UPDATE basic_info SET Eng_Score = ? WHERE Name = ? AND Student_code = ?", (eng_score, name, student_code))
    else:
        raise ValueError("Invalid subject.")

    conn.commit()

def insert_answer(name, student_code, subject, answers):
    if len(answers) != 180:
        raise ValueError("answers must contain exactly 180 elements (36 questions × 5 choices)")

    conn = sql.connect('Databases.db')
    db = conn.cursor()

    # Generate column names: "1A", "1B", ..., "36E"
    columns = [f'"{i}{letter}"' for i in range(1, 37) for letter in ['A', 'B', 'C', 'D', 'E']]

    # Insert: try to insert new row (will be ignored if already exists)
    all_columns = ['Name', 'Student_code', 'Subject'] + columns
    placeholders = ', '.join(['?'] * len(all_columns))
    insert_query = f'''
        INSERT OR IGNORE INTO answer ({', '.join(all_columns)})
        VALUES ({placeholders})
    '''
    db.execute(insert_query, [name, student_code, subject] + answers)

    # Update: update row if it already exists
    set_clause = ', '.join([f'{col} = ?' for col in columns])
    update_query = f'''
        UPDATE answer SET {set_clause}
        WHERE Name = ? AND Student_code = ? AND Subject = ?
    '''
    db.execute(update_query, answers + [name, student_code, subject])

    conn.commit()
    conn.close()

def register(name, student_code, password):
    conn = sql.connect("Databases.db")
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
    conn = sql.connect("Databases.db")
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


conn.commit()
conn.close()

