CREATE TABLE tg_prime.tb_Usuarios (
    ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    Nombre NVARCHAR(255),
    Email_Usa NVARCHAR(255),
    Email_alterno NVARCHAR(255),
    Telefono NVARCHAR(15),
    Programa NVARCHAR(255),
    Rol NVARCHAR(255),
    Salt VARBINARY(16), -- Campo para la sal
    HashContraseña VARBINARY(64) -- Campo para el hash de la contraseña
);
