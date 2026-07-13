DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS equipamento;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE equipamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    fabricante TEXT NOT NULL,
    patrimonio TEXT UNIQUE NOT NULL,
    localizacao TEXT NOT NULL,
    status TEXT NOT NULL,
    usuario_id INTEGER NOT NULL,

    FOREIGN KEY (usuario_id)
        REFERENCES user(id)
);

    FOREIGN KEY (usuario_id)
        REFERENCES user(id)
);