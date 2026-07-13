# Sistema de Cadastro de Equipamentos de TI

Aplicação desenvolvida em Flask para a disciplina de Programação para Internet.

## Funcionalidades

- Cadastro de usuários
- Login e Logout
- Cadastro de equipamentos
- Listagem de equipamentos
- Atualização de equipamentos
- Exclusão de equipamentos

## Tecnologias

- Python 3
- Flask
- SQLite
- HTML
- CSS

## Estrutura

O projeto segue a organização apresentada no Tutorial Oficial do Flask.

## Como executar

Criar ambiente virtual:

```bash
python -m venv .venv
```

Ativar ambiente:

```bash
source .venv/bin/activate
```

Instalar Flask:

```bash
pip install flask
```

Inicializar banco:

```bash
flask --app flaskr init-db
```

Executar:

```bash
flask --app flaskr run --debug
```