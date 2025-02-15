document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".ajax-form");
    if (!form) return;

    const phoneInput = document.getElementById("phone");

    if (phoneInput) {
        phoneInput.addEventListener("input", function () {
            let value = phoneInput.value.replace(/\D/g, ""); // Убираем все нецифровые символы

            if (!value.startsWith("998")) {
                value = "998"; // Если удалили всё, оставляем только код страны
            }

            if (value.length > 12) {
                value = value.slice(0, 12); // Ограничиваем длину
            }

            // Форматируем номер
            let formattedValue = "+998 ";
            if (value.length > 3) formattedValue += "(" + value.slice(3, 5);
            if (value.length > 5) formattedValue += ") " + value.slice(5, 8);
            if (value.length > 8) formattedValue += "-" + value.slice(8, 10);
            if (value.length > 10) formattedValue += "-" + value.slice(10, 12);

            phoneInput.value = formattedValue;
        });

        phoneInput.addEventListener("keydown", function (event) {
            // Блокируем удаление "+998 " при нажатии Backspace или Delete
            if ((phoneInput.value === "+998 " || phoneInput.value === "+998 (") &&
                (event.key === "Backspace" || event.key === "Delete")) {
                event.preventDefault();
            }
        });
    }


    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Отменяем стандартное поведение формы

        const rawPhone = phoneInput ? phoneInput.value.replace(/\D/g, "") : "";

        // Собираем данные формы
        const formData = {
            username: form.username.value,
            phone: rawPhone, // Отправляем номер без форматирования
            password: form.password.value,
            date_of_birth: form.date_of_birth ? form.date_of_birth.value : null,
            subject: form.subject ? form.subject.value : null,
            experience_years: form.experience_years ? form.experience_years.value : null
        };

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
                form.reset();
            } else {
                messageBox.textContent = result.detail || "Ошибка при регистрации.";
                messageBox.style.color = "red";
            }
        } catch (error) {
            messageBox.textContent = "Произошла ошибка при отправке формы.";
            messageBox.style.color = "red";
            console.error("Ошибка:", error);
        }
    });
});
