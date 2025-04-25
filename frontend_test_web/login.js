document.getElementById('loginForm').addEventListener('submit',async (e) => {
    e.preventDefault()

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const messageException = document.getElementById('message');

    try {
        const response = await fetch("http://127.0.0.1:8000/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({email, password})
        });

        const data = await response.json();

        if (response.ok) {
            messageException.textContent = 'Заебись'
            localStorage.setItem('access_token', JSON.stringify(data))
            window.location.href = 'profile.html'
        }
        else {
            messageException.textContent = data.detail || "Ошибка входа";
        }
    }
    catch (error) {
        messageException.textContent = "Сервер не отвечает";
        console.error("Ошибка:", error);
    }
});