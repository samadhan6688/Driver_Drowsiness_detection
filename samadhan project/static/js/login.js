const form = document.getElementById("login-form")

form.addEventListener("submit", async (e) => {
    e.preventDefault()
    const email = document.getElementById("email").value
    const password = document.getElementById("password").value

    const body = {
        identifier: email,
        password
    }

   const res = await fetch("http://localhost:1337/api/auth/local", {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
            "Content-Type": "application/json"
        }
    })

    if (res.status === 200) {
        window.location.replace("/index2")
    }

    console.log(res)
})