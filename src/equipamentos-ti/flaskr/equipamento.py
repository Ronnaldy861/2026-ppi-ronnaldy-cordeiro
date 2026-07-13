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
import sqlite3

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
            e.usuario_id,
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
            erro = "O patrimônio é obrigatório."

        elif not localizacao:
            erro = "A localização é obrigatória."

        if erro is not None:

            flash(erro)

        else:

            db = get_db()

            try:

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

                    VALUES (?, ?, ?, ?, ?, ?, ?)
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

            except sqlite3.IntegrityError:

                flash("Já existe um equipamento com esse patrimônio.")

            else:

                flash("Equipamento cadastrado com sucesso!")

                return redirect(url_for("equipamento.index"))

    return render_template("equipamento/create.html")


def get_equipamento(id, check_author=True):

    equipamento = get_db().execute(
        """
        SELECT
            e.*,
            u.username

        FROM equipamento e

        JOIN user u
            ON e.usuario_id = u.id

        WHERE e.id = ?
        """,
        (id,),
    ).fetchone()

    if equipamento is None:
        abort(404)

    if check_author and equipamento["usuario_id"] != g.user["id"]:
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

        if erro is not None:

            flash(erro)

        else:

            db = get_db()

            try:

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

            except sqlite3.IntegrityError:

                flash("Já existe um equipamento com esse patrimônio.")

            else:

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

    flash("Equipamento excluído com sucesso!")

    return redirect(url_for("equipamento.index"))