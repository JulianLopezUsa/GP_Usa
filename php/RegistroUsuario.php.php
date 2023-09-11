<?php

    include 'conexion.php';

    $nombreC = $_POST['nombreC']
    $emailU = $_POST['CorreoUSA']
    $emailA = $_POST['CorreoA']
    $telefono = $_POST['telefono']
    $programa = $_POST['programa']
    $contrasena = $_POST['contrasena']


    $query = "INSERT INTO `tb_usuarios`(`Nombre`, `Email_Usa`, `Email_alterno`, `Telefono`, `Programa`, `Rol`, `Salt`, `HashContraseña`) 
    VALUES (' $nombreC','$CorreoUSA','$CorreoA','$telefono','$programa','Estudiante','$contrasena')";

    $ejecutar = mysqli_query($conexion,$query);

?>