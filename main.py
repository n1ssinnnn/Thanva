import cv2
import pytesseract
import numpy as np
import src.function as fn
import src.Reg_Log as rl

# Path
answer_img_path = "answer_sheet/20250529110230_002.jpg"
student_img_path = "answer_sheet/20250529110230_014.jpg"

# โหลดภาพสี (ไว้ไฮไลท์)
student_answer_color = cv2.imread(student_img_path)

# อ่านคำตอบจาก user,correct
user_answers, correct_answers = fn.load_extract_anwers(student_img_path, answer_img_path)

print(user_answers)
print(correct_answers)

# STEP 3: ตรวจคำตอบ
flags = fn.grade_answers(user_answers, correct_answers)
# print("Flags:", flags)

# STEP 4: Highlight
final_img = fn.highlight_per_question_by_answer(student_answer_color, flags)

score, results = fn.score_answers_by_group(user_answers, correct_answers)
print("คะแนน:", score)

student_info = fn.extract_student_info(student_answer_color)
for key, value in student_info.items():
    if key in ["วิชา", "ห้องสอบ", "ชื่อผู้สอบ"]:
        value = fn.clean_exam_info(value)
    print(f"{key}: {value}")

#print("รหัสวิชา (OMR):", written_numbers["รหัสวิชา"])
#print("รหัสประจำตัวผู้สอบ (OMR):", written_numbers["รหัสประจำตัวผู้สอบ"])
#print("รหัสวิชา (OCR):", written_numbers["รหัสวิชา_OCR"])
#print("รหัสประจำตัวผู้สอบ (OCR):", written_numbers["รหัสประจำตัวผู้สอบ_OCR"])

written_numbers = fn.extract_written_numbers_fields(student_answer_color)
final_numbers = fn.get_final_written_numbers(student_answer_color)
# กรองสัญลักษณ์ออก
exam_code = fn.clean_exam_info(final_numbers["รหัสวิชา"])
student_code = fn.clean_exam_info(final_numbers["รหัสประจำตัวผู้สอบ"])
seat_code = student_code[-2:] if len(student_code) >= 2 else student_code
print("เลขที่นั่งสอบ:", "A" + seat_code)
print("รหัสวิชา:", exam_code)
print("รหัสประจำตัวผู้สอบ:", student_code)

cv2.imshow("Result", final_img)
cv2.waitKey(0)
cv2.destroyAllWindows()