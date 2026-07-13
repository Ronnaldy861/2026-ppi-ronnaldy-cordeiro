from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("equipamento", __name__)


@bp.route("/")
def index():

    db = get_db()

    equipamentos = db.execute(
        """
        SELECT
            e.id,
            e.nome,
            e.categoria,
            e.fabricante,
            e.patrimonio,
            e.localizacao,
            e.status,
            u.username

        FROM equipamento e

        JOIN user u
            ON e.usuario_id = u.id

        ORDER BY e.nome
        """
    ).fetchall()

    return render_template(
        "equipamento/index.html",
        equipamentos=equipamentos,
    )


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():

    if request.method == "POST":

        nome = request.form["nome"].strip()
        categoria = request.form["categoria"].strip()
        fabricante = request.form["fabricante"].strip()
        patrimonio = request.form["patrimonio"].strip()
        localizacao = request.form["localizacao"].strip()
        status = request.form["status"]

        erro = None

        if not nome:
            erro = "O nome do equipamento é obrigatório."

        elif not categoria:
            erro = "A categoria é obrigatória."

        elif not fabricante:
            erro = "O fabricante é obrigatório."

        elif not patrimonio:
            erro = "O número de patrimônio é obrigatório."

        elif not localizacao:
            erro = "A localização é obrigatória."

        db = get_db()

        patrimonio_existente = db.execute(
            """
            SELECT id
            FROM equipamento
            WHERE patrimonio = ?
            """,
            (patrimonio,),
        ).fetchone()

        if patrimonio_existente is not None:
            erro = "Já existe um equipamento com esse patrimônio."

        if erro is not None:

            flash(erro)

        else:

            db.execute(
                """
                INSERT INTO equipamento
                (
                    nome,
                    categoria,
                    fabricante,
                    patrimonio,
                    localizacao,
                    status,
                    usuario_id
                )

                VALUES
                (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    nome,
                    categoria,
                    fabricante,
                    patrimonio,
                    localizacao,
                    status,
                    g.user["id"],
                ),
            )

            db.commit()

            flash("Equipamento cadastrado com sucesso!")

            return redirect(url_for("equipamento.index"))

    return render_template("equipamento/create.html")


def get_equipamento(id):

    equipamento = get_db().execute(
        """
        SELECT *
        FROM equipamento
        WHERE id = ?
        """,
        (id,),
    ).fetchone()

    if equipamento is None:
        abort(404)

    if equipamento["usuario_id"] != g.user["id"]:
        abort(403)

    return equipamento


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):

    equipamento = get_equipamento(id)

    if request.method == "POST":

        nome = request.form["nome"].strip()
        categoria = request.form["categoria"].strip()
        fabricante = request.form["fabricante"].strip()
        patrimonio = request.form["patrimonio"].strip()
        localizacao = request.form["localizacao"].strip()
        status = request.form["status"]

        erro = None

        if not nome:
            erro = "O nome é obrigatório."

        elif not patrimonio:
            erro = "O patrimônio é obrigatório."

        db = get_db()

        patrimonio_existente = db.execute(
            """
            SELECT id
            FROM equipamento
            WHERE patrimonio = ?
            AND id != ?
            """,
            (
                patrimonio,
                id,
            ),
        ).fetchone()

        if patrimonio_existente:
            erro = "Este patrimônio já está cadastrado."

        if erro is not None:

            flash(erro)

        else:

            db.execute(
                """
                UPDATE equipamento

                SET
                    nome = ?,
                    categoria = ?,
                    fabricante = ?,
                    patrimonio = ?,
                    localizacao = ?,
                    status = ?

                WHERE id = ?
                """,
                (
                    nome,
                    categoria,
                    fabricante,
                    patrimonio,
                    localizacao,
                    status,
                    id,
                ),
            )

            db.commit()

            flash("Equipamento atualizado com sucesso!")

            return redirect(url_for("equipamento.index"))

    return render_template(
        "equipamento/update.html",
        equipamento=equipamento,
    )


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):

    get_equipamento(id)

    db = get_db()

    db.execute(
        "DELETE FROM equipamento WHERE id = ?",
        (id,),
    )

    db.commit()

    flash("Equipamento removido com sucesso!")

    return redirect(url_for("equipamento.index"))