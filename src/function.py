import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

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

def extract_info_fields(img_gray):
    fields = {
        "name": (236, 357, 499, 55),
        "exam_date": (391, 500, 314, 53),
        "subject": (170, 420, 530, 65),
        "room": (234, 563, 176, 64),
        "seat_code": (569,574,130,49),
    }

    info = {}
    for key, (x, y, w, h) in fields.items():
        roi = img_gray[y:y+h, x:x+w]
        #if roi.size == 0:
        #    info[key] = ""
        #    print(f"Warning: ROI for '{key}' is empty or out of bounds.")
        #    continue                                                       *****
        if roi.ndim == 3:               
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        roi = cv2.GaussianBlur(roi, (3, 3), 0)
        _, roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text = pytesseract.image_to_string(roi, config='--psm 7 -l eng+tha')
        clean_text = text.strip()
        #if not clean_text:
        #    print(f"Warning: No text detected for '{key}'.")               *****
        info[key] = clean_text

    return info

omr_exam_digit_boxes = {
    'exam_digit_1': (127, 803, 42, 489),
    'exam_digit_2': (170, 803, 42, 489),
    'exam_digit_3': (218, 802, 43, 483),
}
omr_student_digit_boxes = {
    'student_digit_1': (291, 801, 42, 484),
    'student_digit_2': (336, 801, 42, 484),
    'student_digit_3': (385, 801, 42, 484),
    'student_digit_4': (432, 801, 42, 484),
    'student_digit_5': (477, 801, 42, 484),
    'student_digit_6': (525, 801, 42, 484),
    'student_digit_7': (570, 801, 42, 484),
    'student_digit_8': (619, 801, 42, 484),
    'student_digit_9': (664, 801, 42, 484),
}

def extract_written_numbers_fields(img_input): 
    # แปลงเป็น grayscale ถ้ายังไม่ใช่
    if img_input.ndim == 3:
        img_gray = cv2.cvtColor(img_input, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img_input.copy()

    number_fields = {
        "exam_digit_1": (124, 727, 41, 63),
        "exam_digit_2": (170, 726, 41, 63),
        "exam_digit_3": (220, 726, 41, 63),
        "student_digit_1": (288, 726, 41, 63),
        "student_digit_2": (335, 726, 41, 63),
        "student_digit_3": (382, 726, 41, 63),
        "student_digit_4": (429, 726, 41, 63),
        "student_digit_5": (475, 726, 41, 63),
        "student_digit_6": (523, 726, 41, 63),
        "student_digit_7": (569, 726, 41, 63),
        "student_digit_8": (616, 726, 41, 63),
        "student_digit_9": (663, 726, 41, 63)
    }



    digits = {}
    for key, (x, y, w, h) in number_fields.items():
        roi = img_gray[y:y+h, x:x+w]
        #if roi.size == 0:
        #   print(f"Warning: ROI for '{key}' is empty or out of bounds.")
        #    digits[key] = "?"
        #    continue                                                          *****
        roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        roi = cv2.GaussianBlur(roi, (3, 3), 0)
        _, roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # cv2.imwrite(f"debug_{key}.png", roi)  # สำหรับ debug
        text = pytesseract.image_to_string(
            roi,
            config='--psm 10 -l eng --oem 3 -c tessedit_char_whitelist=0123456789'
        )
        value = text.strip()
        #if not value:
        #   print(f"Warning: No digit detected for '{key}'.")           *****
        digits[key] = value if value else "?"

    exam_number = ''.join([digits.get(f'exam_digit_{i}', '?') for i in range(1, 4)])
    student_code = ''.join([digits.get(f'student_digit_{i}', '?') for i in range(1, 10)])

    omr_exam_digits = extract_omr_digits(img_gray, omr_exam_digit_boxes, min_fill_ratio=0.3)
    omr_student_digits = extract_omr_digits(img_gray, omr_student_digit_boxes, min_fill_ratio=0.3)
    omr_exam_number = ''.join([omr_exam_digits.get(f'exam_digit_{i}', '?') for i in range(1, 4)])
    omr_student_code = ''.join([omr_student_digits.get(f'student_digit_{i}', '?') for i in range(1, 10)])

    return {
        "รหัสวิชา": omr_exam_number,           # ใช้ค่าจาก OMR
        "รหัสประจำตัวผู้สอบ": omr_student_code,           # ใช้ค่าจาก OMR
        "รหัสวิชา_OCR": exam_number,           # เก็บค่า OCR เดิมไว้
        "รหัสประจำตัวผู้สอบ_OCR": student_code            # เก็บค่า OCR เดิมไว้
    }

def extract_omr_digits(img_gray, digit_boxes, threshold=150, min_fill_ratio=0.2):
    digits = {}
    for key, (x, y, w, h) in digit_boxes.items():
        cell_height = h // 10
        max_fill, selected_digit = 0, None
        for i in range(10):
            y_i = y + i * cell_height
            roi = img_gray[y_i:y_i + cell_height, x:x + w]
            _, binary = cv2.threshold(roi, threshold, 255, cv2.THRESH_BINARY_INV)
            fill = cv2.countNonZero(binary)
            if fill > max_fill:
                max_fill = fill
                selected_digit = i
        # ถ้า max_fill น้อยกว่าค่าที่กำหนด (เช่น ไม่มีฝนจริง)
        if max_fill < (w * cell_height * min_fill_ratio):
            digits[key] = ""
        else:
            digits[key] = str(selected_digit)
    return digits


def merge_omr_ocr_field(omr: str, ocr: str) -> str:
    # ถ้า ocr เป็น ? ให้เว้นว่าง ไม่เติมเลข omr
    result = ""
    for o, c in zip(omr, ocr):
        if c == "?":
            continue  # ข้ามหลักที่เป็น ?
        else:
            result += c
    # ถ้า ocr สั้นกว่า omr
    if len(omr) > len(ocr):
        result += omr[len(ocr):]
    return result

def get_final_written_numbers(img_input):
    written_numbers = extract_written_numbers_fields(img_input)
    final = {}
    # รหัสวิชา: ใช้ OMR ทั้งหมด
    final["รหัสวิชา"] = written_numbers.get("รหัสวิชา", "")
    # รหัสประจำตัวผู้สอบ: ตัดหลักซ้ายสุด
    omr_student = written_numbers.get("รหัสประจำตัวผู้สอบ", "")
    final["รหัสประจำตัวผู้สอบ"] = omr_student[1:] if len(omr_student) > 1 else ""
    return final

def scan_digits_from_boxes(img_gray, boxes_dict, num_choices=10, threshold=150):
    digits = []
    for key in sorted(boxes_dict.keys()):
        x, y, w, h = boxes_dict[key]
        cell_height = h // num_choices
        max_fill, selected_digit = 0, 0

        for i in range(num_choices):
            y_i = y + i * cell_height
            roi = img_gray[y_i:y_i + cell_height, x:x + w]
            _, binary = cv2.threshold(roi, threshold, 255, cv2.THRESH_BINARY_INV)
            fill = cv2.countNonZero(binary)

            if fill > max_fill and fill > (w * cell_height * 0.5):
                max_fill = fill
                selected_digit = i

        digits.append(str(selected_digit))

    return ''.join(digits)

def clean_exam_info(text: str) -> str:
    # ลบ { } ;
    return text.replace('{', '').replace('}', '').replace(';', '').replace('|', '').strip()

def extract_student_info(img_gray):
    info = extract_info_fields(img_gray)
    return {
        "ชื่อผู้สอบ": info.get("name", ""),
        "วิชา": info.get("subject", ""),
        "วันที่สอบ": info.get("exam_date", ""),
        "ห้องสอบ": info.get("room", ""),
    }

# โหลดภาพ
def load_extract_anwers(student_path, answer_path):

    student_answer = cv2.imread(student_path, cv2.IMREAD_GRAYSCALE)
    answer = cv2.imread(answer_path, cv2.IMREAD_GRAYSCALE)

    if student_answer is None:
        raise ValueError(f"❌ Failed to load student image at path: {student_path}")
    if answer is None:
        raise ValueError(f"❌ Failed to load answer image at path: {answer_path}")

    user_answers = extract_user_answers(student_answer)
    correct_answers = extract_user_answers(answer)

    return user_answers, correct_answers


