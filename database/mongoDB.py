from pymongo import MongoClient

client = MongoClient("mongodb+srv://Cluster40353:pbl1com31@cluster40353.jwnefyf.mongodb.net/")

db = client["Databases"]

account_col = db["account"]
basic_info_col = db["basic_info"]
answer_col = db["answer"]

def insert_account(fName, lName, student_code):
    account_col.update_one(
        {"fName": fName, "lName": lName, "ID": student_code},
        {"$setOnInsert": {"fName": fName, "lName": lName, "ID": student_code}},
        upsert=True
    )

def insert_data(fName, lName, student_code, subject, date, room, seat,math_score=None, phy_score=None, chem_score=None, eng_score=None):
    update_fields = {
        "Date": date,
        "Room": room,
        "Seat": seat,
        "Math_Score": math_score,
        "Phy_Score": phy_score,
        "Chem_Score": chem_score,
        "Eng_Score": eng_score
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
        {"fName": fName, "lName": lName, "ID": student_code, "Date": date, "Room": room, "Seat": seat},
        {"$setOnInsert": {"fName": fName, "lName": lName, "ID": student_code, "Date": date, "Room": room, "Seat": seat},
         "$set": update_fields},
        upsert=True
    )

def insert_answer(fName, lName, student_code, subject, answers):
    if len(answers) != 180:
        raise ValueError("answers must contain exactly 180 elements (36 questions × 5 choices)")

    columns = [f"{i}{letter}" for i in range(1, 37) for letter in ['A', 'B', 'C', 'D', 'E']]

    answer_doc = {
        "fName": fName,
        "lName": lName,
        "ID": student_code,
        "Subject": subject
    }
    for col, ans in zip(columns, answers):
        answer_doc[col] = ans

    answer_col.update_one(
        {"fName": fName, "lName": lName, "ID": student_code, "Subject": subject},
        {"$set": answer_doc},
        upsert=True
    )


