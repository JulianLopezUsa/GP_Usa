const $btnSignIn= document.querySelector('.sign-in-btn'),
      $btnSignUp = document.querySelector('.sign-up-btn'),  
      $signUp = document.querySelector('.sign-up'),
      $signIn  = document.querySelector('.sign-in');

document.addEventListener('click', e => {
    if (e.target === $btnSignIn || e.target === $btnSignUp) {
        $signIn.classList.toggle('active');
        $signUp.classList.toggle('active')
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const submitButton = document.getElementById("submit");

    submitButton.addEventListener("click", function () {
        const email = emailInput.value;
        const password = passwordInput.value;

        if (!email || !password) {
            alert("Por favor, complete todos los campos.");
        } else {
            enviarDatosAlServidor(email, password);
        }
    });

    function enviarDatosAlServidor(email, password) {
        // Simula el envío de datos del formulario al servidor
        console.log("Email: " + email);
        console.log("Contraseña: " + password);
    }
});
