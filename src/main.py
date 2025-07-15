import cv2
import pytesseract
import numpy as np
from src import function as fn
from database import DB as db

# Path
answer_img_path = "answer_sheet/20250529110230_002.jpg"
student_img_path = "answer_sheet/20250529110230_001.jpg"

# โหลดภาพสี (ไว้ไฮไลท์)
student_answer_color = cv2.imread(student_img_path)

# อ่านคำตอบจาก user,correct
user_answers, correct_answers = fn.load_extract_anwers(student_img_path, answer_img_path)

# print(user_answers)
# print(correct_answers)
 

# STEP 3: ตรวจคำตอบ
flags = fn.grade_answers(user_answers, correct_answers)
# print("Flags:", flags)

# STEP 4: Highlight
final_img = fn.highlight_per_question_by_answer(student_answer_color, flags)

score, results = fn.score_answers_by_group(user_answers, correct_answers)
print("คะแนน:", score)
# print("ผลแต่ละข้อ:", results)

# แสดงผล
cv2.imshow("Result", final_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
