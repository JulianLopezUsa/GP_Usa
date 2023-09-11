const sql = require('mssql');

const config = {
    user: 'tu_usuario',
    password: 'tu_contraseña',
    server: 'tu_servidor',
    database: 'nombre_de_tu_base_de_datos',
};

// Conectar a la base de datos
sql.connect(config)
    .then(() => {
        console.log('Conexión a SQL Server exitosa');
    })
    .catch((err) => {
        console.error('Error al conectar a SQL Server', err);
    });
