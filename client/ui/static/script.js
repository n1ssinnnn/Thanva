// BGM
const audio = document.getElementById('bgm');
audio.volume = 0.025; // ค่าระหว่าง 0.0 (เงียบ) ถึง 1.0 (เต็มเสียง)

window.addEventListener('click', function () {
    const audio = document.getElementById('bgm');
    audio.play();
}, { once: true });

// MENU

//เปิด-ปิดแทบ
document.addEventListener("DOMContentLoaded", function () {
    const menus = ["check", "score", "setting", "credit"];

    function showMenu(menuId) {
        menus.forEach(id => {
            const menu = document.getElementById(id);
            if (menu) {
                menu.classList.add("hidden");
            }
        });

        const toShow = document.getElementById(menuId);
        if (toShow) {
            toShow.classList.remove("hidden");
        }
    }

    document.getElementById("check-button").addEventListener("click", () => {
        showMenu("check");
    });

    document.getElementById("myscore-button").addEventListener("click", () => {
        showMenu("score");
    });

    document.getElementById("setting-button").addEventListener("click", () => {
        showMenu("setting");
    });

    document.getElementById("credit-button").addEventListener("click", () => {
        showMenu("credit");
    });
});
//เสียงกด
document.addEventListener('DOMContentLoaded', function () {
    const selectSound = document.getElementById('sfx-select');
    const clickSound = document.getElementById('sfx-click');
    const menuButtons = document.querySelectorAll('.menu-button');
    selectSound.volume = 0.05;
    clickSound.volume = 0.5;

    menuButtons.forEach(button => {
        // เล่นเสียงตอน select
        button.addEventListener('mouseenter', () => {
            selectSound.currentTime = 0; // รีเซ็ตเสียงก่อนเล่นใหม่
            selectSound.play();
        });

        button.addEventListener('mouseenter', () => {
            const hover = selectSound.cloneNode();
            hover.volume = 0.025;
            hover.play();
        });

        // เล่นเสียงตอนคลิก
        button.addEventListener('click', () => {
            clickSound.currentTime = 0;
            clickSound.play();
        });
    });
});

// CHECK
document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("file-input");
    const uploadedImage = document.getElementById("uploaded-image");
    const confirmButton = document.querySelector(".confirm_button");

    fileInput.addEventListener("change", function () {
        const file = fileInput.files[0];
        if (file && file.type.startsWith("image/")) {
            const reader = new FileReader();

            reader.onload = function (e) {
                uploadedImage.src = e.target.result;
                uploadedImage.classList.remove("hidden");
                confirmButton.classList.remove("hidden");
            };

            reader.readAsDataURL(file);
        } else {
            alert("กรุณาเลือกไฟล์รูปภาพเท่านั้น!");
        }
    });
});

// SCORE
const input = document.getElementById("studentid");
const message = input.value; // inputของuser

document.addEventListener('DOMContentLoaded', function () {
    const studentIdInput = document.getElementById('studentid');
    const confirmButton = document.getElementById('score-confirm');

    studentIdInput.addEventListener('input', function () {
        if (studentIdInput.value.trim() !== "") {
            confirmButton.classList.remove('hidden');
        } else {
            confirmButton.classList.add('hidden');
        }
    });
});
