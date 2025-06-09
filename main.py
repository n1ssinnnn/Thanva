import cv2
import pytesseract
import numpy as np

# Load the answer image
answer = cv2.imread('answer_sheet/answer.jpg')
answer = cv2.cvtColor(answer, cv2.COLOR_BGR2GRAY)

# Student answer
student_answer = cv2.imread('answer_sheet/20250529110230_003.jpg')
student_answer = cv2.cvtColor(student_answer, cv2.COLOR_BGR2GRAY)

# Resize
student_answer = cv2.resize(student_answer, answer.shape[::-1])

# Threshold (Black-White)
_, thresh_ans = cv2.threshold(answer, 127, 255, cv2.THRESH_BINARY_INV)
_, thresh_stu = cv2.threshold(student_answer, 127, 255, cv2.THRESH_BINARY_INV)

# Extract gaps 
def extract_answers(thresh_img, start_x, start_y, bubble_w, bubble_h, vertical_gap, horizontal_gap, columns, rows_per_column):
    """
    ดึงคำตอบทั้งหมดจากภาพ แยกเป็น [ข้อที่][ตัวเลือก A-E]
    เช่น answers[0] = [bubble_A, bubble_B, bubble_C, bubble_D, bubble_E] ของข้อ 1
    """
    all_answers = []

    for col in range(columns):  # 4 คอลัมน์
        for row in range(rows_per_column):  # 9 แถวต่อคอลัมน์
            question_bubbles = []
            y = start_y + row * (bubble_h + vertical_gap)
            x_base = start_x + col * (5 * (bubble_w + horizontal_gap) + 30)  # คอลัมน์ถัดไปเลื่อนไกลกว่าปกติ

            for i in range(5):  # ตัวเลือก A-E
                x = x_base + i * (bubble_w + horizontal_gap)
                bubble = thresh_img[y:y + bubble_h, x:x + bubble_w]
                question_bubbles.append(bubble)

            all_answers.append(question_bubbles)
    
    return all_answers  # list: [[A, B, C, D, E], [A, B, C, D, E], ...]

def detect_answers_grouped(bubble_groups):
    """
    รับ input เป็นคำตอบแบบกลุ่ม [[A, B, C, D, E], ...]
    คืนค่าตัวเลข 0-4 แทน A-E ตามที่ฝนเข้มที่สุด
    """
    answers = []
    for group in bubble_groups:
        blackness = [cv2.countNonZero(b) for b in group]
        selected = np.argmax(blackness)
        answers.append(selected)
    return answers

bubble_groups = extract_answers(
    thresh_img=student_answer,
    start_x=290,
    start_y=115,
    bubble_w=18,
    bubble_h=18,
    vertical_gap=22,
    horizontal_gap=25,
    columns=4,
    rows_per_column=9
)

answer_groups = extract_answers(
    thresh_img=student_answer,
    start_x=290,
    start_y=115,
    bubble_w=18,
    bubble_h=18,
    vertical_gap=22,
    horizontal_gap=25,
    columns=4,
    rows_per_column=9
)

student_answers = detect_answers_grouped(bubble_groups)

# สมมติว่าเฉลยคือข้อนี้
correct_answers = detect_answers_grouped(answer_groups)

score = sum([s == c for s, c in zip(student_answers, correct_answers)])
print(f"คะแนนที่ได้: {score}/36")

cv2.imshow('Answer', answer)
cv2.imshow('Student Answer', student_answer)

cv2.waitKey(0)
cv2.destroyAllWindows()
