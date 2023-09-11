//Ejecutando funciones
document.getElementById("Iniciar Sesion").addEventListener("click", iniciarSesion);
document.getElementById("Registrar").addEventListener("click", register);
window.addEventListener("resize", anchoPage);

//Declarando variables
var formulario_login = document.querySelector(".loginForm");
var formulario_register = document.querySelector(".formulario");
var contenedor_login_register = document.querySelector(".container-form sign-up");
var caja_trasera_login = document.querySelector(".caja__trasera-login");
var caja_trasera_register = document.querySelector("container-form sign-in");