const express = require('express');
const mysql = require('mysql');
const app = express();

const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'safa_db'
});

db.connect((err) => {
    if (err) throw err;
    console.log('Database connected!');
});

app.get('/warung', (req, res) => {
    const sql = 'SELECT * FROM warung';
    db.query(sql, (err, result) => {
        if (err) throw err;
        res.send(result);
    });
});

app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});
