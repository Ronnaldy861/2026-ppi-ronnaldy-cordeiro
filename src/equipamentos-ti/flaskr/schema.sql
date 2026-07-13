DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS equipamento;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE equipamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    patrimonio TEXT NOT NULL,

    nome TEXT NOT NULL,

    tipo TEXT NOT NULL,

    laboratorio TEXT NOT NULL,

    status TEXT NOT NULL,

    observacao TEXT,

    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    author_id INTEGER NOT NULL,

    FOREIGN KEY(author_id)
        REFERENCES user(id)
);
