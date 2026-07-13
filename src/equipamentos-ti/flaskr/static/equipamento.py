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

        nome = request.form["nome"]
        categoria = request.form["categoria"]
        fabricante = request.form["fabricante"]
        patrimonio = request.form["patrimonio"]
        localizacao = request.form["localizacao"]
        status = request.form["status"]

        erro = None

        if not nome:
            erro = "Nome obrigatório."

        if erro is not None:
            flash(erro)

        else:

            db = get_db()

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

        db = get_db()

        db.execute(
            """
            UPDATE equipamento

            SET

            nome=?,
            categoria=?,
            fabricante=?,
            patrimonio=?,
            localizacao=?,
            status=?

            WHERE id=?
            """,

            (
                request.form["nome"],
                request.form["categoria"],
                request.form["fabricante"],
                request.form["patrimonio"],
                request.form["localizacao"],
                request.form["status"],
                id,
            ),
        )

        db.commit()

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
        "DELETE FROM equipamento WHERE id=?",
        (id,),
    )

    db.commit()

    return redirect(url_for("equipamento.index"))