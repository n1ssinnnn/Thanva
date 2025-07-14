import cv2
import pytesseract
import numpy as np
import Function.function as fn

answer_img_path = "answer_sheet/20250529110230_002.jpg"
student_img_path = "answer_sheet/20250529110230_001.jpg"

student_answer_color = cv2.imread(student_img_path)

user_answers, correct_answers = fn.load_extract_anwers(student_img_path, answer_img_path)

print(user_answers)
print(correct_answers)
 
flags = fn.grade_answers(user_answers, correct_answers)

final_img = fn.highlight_per_question_by_answer(student_answer_color, flags)

score, results = fn.score_answers_by_group(user_answers, correct_answers)
print("คะแนน:", score)

cv2.imshow("Result", final_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
