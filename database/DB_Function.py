import sqlite3 as sql

conn = sql.connect('database/Databases.db')
db = conn.cursor()

#Insert data function

def insert_data(name, student_code, subject, math_score=None, phy_score=None, chem_score=None, eng_score=None):
    conn = sql.connect('database/Databases.db')
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

    conn = sql.connect('database/Databases.db')
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

conn.commit()
conn.close()

