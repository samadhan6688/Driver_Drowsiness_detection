const form = document.getElementById("register-form")

form.addEventListener("submit", async (e) => {
    e.preventDefault()
    const email = document.getElementById("email").value
    const password = document.getElementById("password").value
    const username = document.getElementById("username").value

    const body = {
        email,
        password,
        username
    }

   const res = await fetch("http://localhost:1337/api/auth/local/register", {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
            "Content-Type": "application/json"
        }
    })

    if (res.status === 200) {
        window.location.replace("/login")
    }

    console.log(res)
})