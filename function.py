import cv2
import numpy as np

# ขนาดและช่องว่าง
bubble_w = 36
bubble_h = 36
col_gap_minor = 8
row_gap_minor = 8

# กำหนดตำแหน่งของ column ใหญ่
major_column_positions = [
    (812, 139),
    (1480, 137),
    (2148, 136),
    (2814, 133)
]

# offset ในแนว y ของแต่ละ major row
major_row_offsets = [0, 249, 498, 746, 995, 1243, 1491, 1739, 1988]

def extract_user_answers(img_gray, threshold=150):
    answers = []

    for col_major in range(4):
        start_x, base_y = major_column_positions[col_major]

        for row_major in range(9):
            start_y = base_y + major_row_offsets[row_major]

            for row_minor in range(5):
                max_fill = 0
                answer_idx = 0  # ไม่ตอบ

                for col_minor in range(13):
                    x = int(start_x + col_minor * (bubble_w + col_gap_minor))
                    y = int(start_y + row_minor * (bubble_h + row_gap_minor))

                    roi = img_gray[y:y + bubble_h, x:x + bubble_w]
                    _, thresh = cv2.threshold(roi, threshold, 255, cv2.THRESH_BINARY_INV)
                    filled = cv2.countNonZero(thresh)

                    if filled > max_fill and filled > bubble_w * bubble_h * 0.5:
                        max_fill = filled
                        answer_idx = col_minor + 1  # ตอบข้อที่ n

                answers.append(answer_idx)

    return answers


def grade_answers(user_answers, correct_answers):
    assert len(user_answers) == len(correct_answers)
    return [u == c for u, c in zip(user_answers, correct_answers)]


def highlight_per_question_by_answer(img_color, correct_flags):
    img_overlay = img_color.copy()
    idx = 0

    for col_major in range(4):
        start_x, base_y = major_column_positions[col_major]

        for row_major in range(9):
            start_y = base_y + major_row_offsets[row_major]

            for row_minor in range(5):
                if idx >= len(correct_flags):
                    break

                # Highlight เฉพาะช่วงคำตอบ 13 bubble ต่อ minor row
                x1 = int(start_x)
                y1 = int(start_y + row_minor * (bubble_h + row_gap_minor))
                x2 = x1 + 13 * (bubble_w + col_gap_minor) - col_gap_minor
                y2 = y1 + bubble_h

                color = (0, 255, 0) if correct_flags[idx] else (0, 0, 255)
                cv2.rectangle(img_overlay, (x1, y1), (x2, y2), color, -1)
                idx += 1

    # โปร่งใส: เห็นตัวอักษรข้างหลัง
    cv2.addWeighted(img_overlay, 0.4, img_color, 0.6, 0, img_color)
    return img_color

def score_answers_by_group(user_answers, correct_answers):
    assert len(user_answers) == len(correct_answers)
    assert len(user_answers) % 5 == 0  # ต้องหาร 5 ลงตัว

    total_questions = len(user_answers) // 5
    score = 0
    results = []  # เก็บ True/False ของแต่ละกลุ่ม 5 ช่อง

    for i in range(total_questions):
        u_group = user_answers[i*5:(i+1)*5]
        c_group = correct_answers[i*5:(i+1)*5]

        if all(u == 0 for u in u_group):
            # ข้อนี้ไม่นับคะแนน
            results.append(None)
        elif u_group == c_group:
            score += 1
            results.append(True)
        else:
            results.append(False)

    return score, results

