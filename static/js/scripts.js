document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".ajax-form");
    if (!form) return;

    // Проверяем, есть ли поле для телефона (регистрация)
    const phoneInput = document.getElementById("phone");

    // Обработка телефона (только для регистрации)
    if (phoneInput) {
        phoneInput.addEventListener("input", function () {
            let value = phoneInput.value.replace(/\D/g, "");

            if (!value.startsWith("998")) {
                value = "998";
            }

            if (value.length > 12) {
                value = value.slice(0, 12);
            }

            let formattedValue = "+998 ";
            if (value.length > 3) formattedValue += "(" + value.slice(3, 5);
            if (value.length > 5) formattedValue += ") " + value.slice(5, 8);
            if (value.length > 8) formattedValue += "-" + value.slice(8, 10);
            if (value.length > 10) formattedValue += "-" + value.slice(10, 12);

            phoneInput.value = formattedValue;
        });

        phoneInput.addEventListener("keydown", function (event) {
            if ((phoneInput.value === "+998 " || phoneInput.value === "+998 (") &&
                (event.key === "Backspace" || event.key === "Delete")) {
                event.preventDefault();
            }
        });
    }

    // Обработка отправки формы
    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        // Подготовка данных для отправки
        const formData = {
            username: form.username.value,
            password: form.password.value
        };

        // Если это регистрация, добавляем телефон и предмет
        if (phoneInput) {
            formData.phone = phoneInput.value.replace(/\D/g, "");
            formData.subject = form.subject.value;  // Добавляем предмет
        }

        console.log("Отправляем JSON:", JSON.stringify(formData));

        const messageBox = form.querySelector(".message");

        try {
            const response = await fetch(form.action, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();
            console.log("Ответ сервера:", result);

            if (response.ok) {
                messageBox.textContent = result.message;
                messageBox.style.color = "green";

                // Перенаправление после успешной регистрации или входа
                if (window.location.pathname === "/register") {
                    setTimeout(() => {
                        window.location.href = "/login";
                    }, 1500);
                } else if (window.location.pathname === "/login") {
                    setTimeout(() => {
                        window.location.href = "/parent/account";
                    }, 1500);
                }
            } else {
                messageBox.textContent = result.detail || "Ошибка.";
                messageBox.style.color = "red";
            }
        } catch (error) {
            messageBox.textContent = "Произошла ошибка при отправке формы.";
            messageBox.style.color = "red";
            console.error("Ошибка:", error);
        }
    });
});