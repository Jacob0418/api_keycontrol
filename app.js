const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');

const app = express();
app.use(bodyParser.json());

// Crear conexión a la base de datos
function createDbConnection() {
    const connection = mysql.createConnection({
        host: "mysql-keycontrol.alwaysdata.net",
        user: "352642",
        password: "key_control2024",
        database: "keycontrol_iotsm54"
    });
    
    connection.connect(error => {
        if (error) throw error;
        console.log('Database connection successful!');
    });

    return connection;
}

// Rutas para los salones
app.route('/salones')
    .get((req, res) => {
        const connection = createDbConnection();
        connection.query("SELECT * FROM classroom", (error, results) => {
            if (error) throw error;
            res.json(results);
            connection.end();
        });
    })
    .post((req, res) => {
        const { salon } = req.body;
        const connection = createDbConnection();
        connection.query("INSERT INTO classroom (salon) VALUES (?)", [salon], (error, results) => {
            if (error) throw error;
            res.status(201).json({ message: "Salon creado exitosamente", salon });
            connection.end();
        });
    });

// Rutas para las tarjetas
app.route('/tarjetas')
    .get((req, res) => {
        const connection = createDbConnection();
        connection.query("SELECT * FROM cards", (error, results) => {
            if (error) throw error;
            res.json(results);
            connection.end();
        });
    })
    .post((req, res) => {
        const { id, uid, salon_id } = req.body;
        const connection = createDbConnection();
        connection.query("SELECT id FROM cards WHERE id = ?", [id], (error, results) => {
            if (error) throw error;
            if (results.length > 0) {
                res.status(404).json({ error: "Usuario no existe" });
            } else {
                connection.query("INSERT INTO cards (uid, salon_id) VALUES (?, ?)", [uid, salon_id], (error, results) => {
                    if (error) throw error;
                    res.status(201).json({ message: "Tarjeta creada exitosamente", data: req.body });
                });
            }
            connection.end();
        });
    });

    // Endpoint para usuarios
app.route('/usuarios')
.get((req, res) => {
    const connection = createDbConnection();
    connection.query("SELECT st.nombre, gp.grupo, cl.salon FROM students st INNER JOIN groups gp ON gp.id = st.grupo_id INNER JOIN classroom cl ON cl.id = st.grupo_id", (error, results) => {
        if (error) throw error;
        res.json(results);
        connection.end();
    });
})
// .post(async (req, res) => {
//   const { nombre, email } = req.body;
//   const connection = createDbConnection();
//   try {
//     const [result] = await connection.query('INSERT INTO usuarios (nombre, email) VALUES (?, ?)', [nombre, email]);
//     res.status(201).json({ message: "Usuario creado exitosamente", nombre, email });
//   } finally {
//     await connection.end();
//   }
// });

// Endpoint para obtener un usuario por su ID
app.get('/usuarios/:id', async (req, res) => {
    const { id } = req.params;
    console.log("ID recibido:", id); // Verificar que se recibe correctamente el ID
    const connection = createDbConnection();
    connection.query("SELECT st.nombre, gp.grupo, cl.salon FROM students st INNER JOIN groups gp ON gp.id = st.grupo_id INNER JOIN classroom cl ON cl.id = grupo_id WHERE gp.id = ?", [id], (error, results) => {
        if (error) throw error;
        res.json(results);
        connection.end();
    });
}
);

app.get('/acceso', async (req, res) => {
    const connection = createDbConnection();
    connection.query("SELECT st.nombre, gp.grupo, cl.salon, u.uid, DATE_FORMAT(ac.date, '%Y-%m-%d') AS fecha FROM students st INNER JOIN groups gp ON st.grupo_id = gp.id INNER JOIN classroom cl ON cl.id = gp.id INNER JOIN cards u ON u.id = st.id INNER JOIN access_control ac ON ac.information = u.uid;", (error, results)=>{
        if (error) throw error;
        res.json(results);
        connection.end();
    });   
});
app.get('/accesolim', async (req, res) => {
    const connection = createDbConnection();
    connection.query("SELECT st.nombre, gp.grupo, cl.salon, u.uid, DATE_FORMAT(ac.date, '%Y-%m-%d') AS fecha FROM students st INNER JOIN groups gp ON st.grupo_id = gp.id INNER JOIN classroom cl ON cl.id = gp.id INNER JOIN cards u ON u.id = st.id INNER JOIN access_control ac ON ac.information = u.uid ORDER BY ac.date DESC LIMIT 1;    ", (error, results)=>{
        if (error) throw error;
        res.json(results);
        connection.end();
    });   
});

    



// Define otras rutas de manera similar a las anteriores.

const PORT = process.env.PORT || 5000;
const HOST = '192.168.100.11';

app.listen(PORT, HOST, () => {
    console.log(`Server running on http://${HOST}:${PORT}`);
});

