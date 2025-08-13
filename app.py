from flask import render_template, redirect, url_for, request, Flask, session
from database import pegar_conexao
app = Flask (__name__)
app.secret_key = 'umsegredo'
@app.route('/')
def index():
    if "usuarios" not in session:
        session["usuarios"] = {}
    
    conexao = pegar_conexao()
    comidas = conexao.execute("SELECT * FROM comidas").fetchall()
    conexao.close()
    return render_template('index.html', comidas=comidas)
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == "POST":
        nome = request.form.get("nome")
        valor = request.form.get("valor", type=float)
        pessoas_por_porcao = request.form.get("pessoas_por_porcao", type=int)
        conexao = pegar_conexao()
        conexao.execute(
            "INSERT INTO comidas (nome, valor, pessoas_por_porcao) VALUES (?, ?, ?)",
            (nome, valor, pessoas_por_porcao)
        )
        conexao.commit()
        conexao.close()
        return redirect(url_for("index"))
    return render_template("cadastrar.html")
@app.route("/cadastrar_pedido", methods=["GET", "POST"])
def cadastrar_pedido():
    conexao = pegar_conexao()
    comidas = conexao.execute("SELECT * FROM comidas").fetchall()
    if request.method == "POST":
        cliente = request.form["cliente"]
        comida_id = int(request.form["comida_id"])
        conexao.execute(
            "INSERT INTO pedidos (cliente, comida_id) VALUES (?, ?)",
            (cliente, comida_id)
        )
        conexao.commit()
        conexao.close()
        return redirect(url_for("listar_pedidos"))
    conexao.close()
    return render_template("cadastrar_pedido.html", comidas=comidas)
@app.route("/pedidos")
def listar_pedidos():
    conexao = pegar_conexao()
    pedidos = conexao.execute("""
        SELECT pedidos.id, pedidos.cliente, comidas.nome AS comida_nome
        FROM pedidos
        JOIN comidas ON pedidos.comida_id = comidas.id
    """).fetchall()
    conexao.close()
    return render_template("pedidos.html", pedidos=pedidos)