import cv2
import pytesseract
import numpy as np
import function as fn

# Load the answer image
answer = cv2.imread("answer_sheet/answer.jpg", cv2.IMREAD_GRAYSCALE)

# Student answer
student_answer_color = cv2.imread("answer_sheet/20250529110230_002.jpg")
student_answer = cv2.imread("answer_sheet/20250529110230_002.jpg", cv2.IMREAD_GRAYSCALE)

# STEP 1: อ่านคำตอบจากภาพ
user_answers = fn.extract_user_answers(student_answer)

# STEP 2: เฉลย เช่น
correct_answers = fn.extract_user_answers(answer)  

print(user_answers)
print(correct_answers)
 

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

