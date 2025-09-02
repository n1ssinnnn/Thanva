from pymongo import MongoClient
import certifi
import pandas as pd
client = MongoClient("mongodb+srv://Cluster40353:pbl1com31@cluster40353.jwnefyf.mongodb.net/", tlsCAFile=certifi.where())

db = client["Databases"]

basic_info_col = db["basic_info"]
answer_col = db["answer"]

def insert_data(fName, lName, student_code, subject, room, math_score=None, phy_score=None, chem_score=None, eng_score=None):
    update_fields = {
        "Math_Score": math_score,
        "Phy_Score": phy_score,
        "Chem_Score": chem_score,
        "Eng_Score": eng_score,
    }

    if subject == "Mathematics":
        update_fields["Math_Score"] = math_score
    elif subject == "Physics":
        update_fields["Phy_Score"] = phy_score
    elif subject == "Chemistry":
        update_fields["Chem_Score"] = chem_score
    elif subject == "English":
        update_fields["Eng_Score"] = eng_score
    else:
        raise ValueError("Invalid subject.")

    basic_info_col.update_one(
        {"fName": fName, "lName": lName, "ID": student_code, "Room": room},
        {"$setOnInsert": {"fName": fName, "lName": lName, "ID": student_code, "Room": room},
         "$set": update_fields},
        upsert=True
    )

def insert_answer(student_code, subject, answers):
    if len(answers) != 180:
        raise ValueError("answers must contain exactly 180 elements (36 questions × 5 choices)")

    columns = [f"{i}{letter}" for i in range(1, 37) for letter in ['A', 'B', 'C', 'D', 'E']]

    answer_doc = {
        "ID": student_code,
        "Subject": subject
    }
    for col, ans in zip(columns, answers):
        answer_doc[col] = ans

    answer_col.update_one(
        {"ID": student_code, "Subject": subject},
        {"$set": answer_doc},
        upsert=True
    )

def login(fName, lName, student_code):
    account = basic_info_col.find_one({
        "fName": fName,
        "lName": lName,
        "ID": student_code
    })
    
    if account:
        return True  
    else:
        return False 

def get_students_by_room_df(room):
    students = basic_info_col.find({"Room": room})
    
    data = []
    for student in students:
        data.append({
            "fName": student.get("fName"),
            "lName": student.get("lName"),
            "ID": student.get("ID"),
            "Room": student.get("Room"),
            "Math_Score": student.get("Math_Score"),
            "Phy_Score": student.get("Phy_Score"),
            "Chem_Score": student.get("Chem_Score"),
            "Eng_Score": student.get("Eng_Score")
        })
    
    df = pd.DataFrame(data)
    print(df)