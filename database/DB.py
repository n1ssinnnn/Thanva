import sqlite3 as sql

conn = sql.connect('Databases.db')
db = conn.cursor()

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

conn.commit()

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

insert_data("Alice", 101, "Mathematics", math_score=85)
insert_data("Alice", 101, "Physics", phy_score=100)

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
conn.close()

