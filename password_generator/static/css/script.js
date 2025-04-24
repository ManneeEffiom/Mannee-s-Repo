function copyPassword() {
    const password = document.getElementById('password').innerText
    navigator.clipboard.writeText(password).then(() => {
        alert('Password copied!');
    });
}