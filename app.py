import sqlite3
import random 
from datetime import datetime 
from flask import Flask, render_template, redirect, url_for, request, session, flash, g

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-segura-trocar-depois'
DATABASE = 'banco.db' 

# GERENCIAMENTO DE CONEXÃO COM O BANCO

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """Fecha a conexão com o banco ao final da requisição."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


# ROTAS PÚBLICAS 
@app.route("/")
def login():
    return render_template("login.html")

# Rota /cadastro
@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

# Rota /registrar_usuario (POST)
@app.route("/registrar_usuario", methods=['POST'])
def registrar_usuario():
    nome = request.form['nome']
    cpf = request.form['cpf']
    data_nasc = request.form['data_nascimento']
    endereco = request.form['endereco']
    senha = request.form['senha']
    
    db = get_db_connection()
    
    # Verificar se o CPF já existe
    usuario_existente = db.execute('SELECT 1 FROM usuarios WHERE cpf = ?', (cpf,)).fetchone()
    if usuario_existente:
        flash(f"Erro: O CPF {cpf} já está cadastrado.", "danger")
        return redirect(url_for('cadastro')) 

    # Gerar nova conta
    nova_conta_num = f"{random.randint(10000, 99999)}-{random.randint(0,9)}"
    
    # Inserir no banco de dados
    try:
        db.execute(
            '''INSERT INTO usuarios 
               (cpf, nome, data_nascimento, endereco, senha, agencia, conta, saldo, eh_admin) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (cpf, nome, data_nasc, endereco, senha, "0001", nova_conta_num, 0.0, 0)
        )
        db.commit()
    except sqlite3.IntegrityError:
         flash("Erro: Ocorreu um problema ao criar sua conta.", "danger")
         return redirect(url_for('cadastro'))
    
    flash("Usuário cadastrado com sucesso! Faça o login.", "success")
    return redirect(url_for('login'))


# Rota /autenticar (POST)
@app.route("/autenticar", methods=['POST'])
def autenticar():
    usuario_input = request.form['usuario'] 
    senha_input = request.form['senha']
    
    db = get_db_connection()
    
    # Busca o usuário pelo CPF
    usuario_encontrado = db.execute(
        'SELECT * FROM usuarios WHERE cpf = ?', (usuario_input,)
    ).fetchone()
    
    if usuario_encontrado and usuario_encontrado['senha'] == senha_input:
        session['usuario_cpf'] = usuario_encontrado['cpf']
        return redirect(url_for('dashboard'))
    else:
        flash("Falha no login. CPF ou senha incorretos.", "danger")
        return redirect(url_for('login'))


# Rota /logout 
@app.route("/logout")
def logout():
    session.pop('usuario_cpf', None) 
    flash("Você foi desconectado.", "success") 
    return redirect(url_for("login"))


# ROTAS PROTEGIDAS
# Função auxiliar para obter o usuário logado
def get_usuario_logado():
    if 'usuario_cpf' not in session:
        return None 
    
    db = get_db_connection()
    usuario = db.execute(
        'SELECT * FROM usuarios WHERE cpf = ?', (session['usuario_cpf'],)
    ).fetchone()
    return usuario 


# Rota /dashboard
@app.route("/dashboard")
def dashboard():
    usuario_logado = get_usuario_logado()
    if not usuario_logado:
        flash("Por favor, faça o login para acessar.", "danger") 
        return redirect(url_for('login')) 
    return render_template("dashboard.html", usuario=usuario_logado)

# Rota /depositar
@app.route("/depositar")
def depositar():
    usuario_logado = get_usuario_logado()
    if not usuario_logado:
        flash("Por favor, faça o login para acessar.", "danger") 
        return redirect(url_for('login'))
    return render_template("depositar.html", usuario=usuario_logado)

# Rota /sacar
@app.route("/sacar")
def sacar():
    usuario_logado = get_usuario_logado()
    if not usuario_logado:
        flash("Por favor, faça o login para acessar.", "danger") 
        return redirect(url_for('login'))
    return render_template("sacar.html", usuario=usuario_logado)


# Rota /extrato
@app.route("/extrato")
def extrato():
    usuario_logado = get_usuario_logado()
    if not usuario_logado:
        flash("Por favor, faça o login para acessar.", "danger") 
        return redirect(url_for('login'))
    
    db = get_db_connection()
    dados_extrato = db.execute(
        'SELECT * FROM extrato WHERE usuario_cpf = ? ORDER BY id DESC', 
        (usuario_logado['cpf'],)
    ).fetchall() 
    
    return render_template("extrato.html", usuario=usuario_logado, extrato=dados_extrato)


# Rota / Admin
@app.route("/admin/listar_contas")
def admin_listar_contas():
    usuario_logado = get_usuario_logado()
    
    if not usuario_logado:
        flash("Por favor, faça o login para acessar.", "danger")
        return redirect(url_for('login'))
    if not usuario_logado['eh_admin']:
        flash("Acesso negado: Você não tem permissão de admin.", "danger")
        return redirect(url_for('dashboard')) 
    
    db = get_db_connection()
    dados_todas_as_contas = db.execute(
        'SELECT agencia, conta, nome AS titular, saldo FROM usuarios'
    ).fetchall()

    return render_template(
        "admin_listar_contas.html", 
        usuario=usuario_logado, 
        contas=dados_todas_as_contas
    )


# ROTAS DE TRANSAÇÕES
@app.route("/realizar_deposito", methods=['POST'])
def realizar_deposito():
    usuario_logado = get_usuario_logado()
    if not usuario_logado:
        return redirect(url_for('login'))
    
    try:
        valor_deposito = float(request.form['valor'])
    except ValueError:
        flash("Valor de depósito inválido.", "danger")
        return redirect(url_for('depositar')) 

    if valor_deposito <= 0:
        flash("O valor do depósito deve ser positivo.", "danger")
        return redirect(url_for('depositar'))
    
    db = get_db_connection()
    data_hoje = datetime.now().strftime('%d/%m/%Y')
    cpf_logado = usuario_logado['cpf']
    
    # Atualiza o saldo em 'usuarios'
    db.execute(
        'UPDATE usuarios SET saldo = saldo + ? WHERE cpf = ?',
        (valor_deposito, cpf_logado)
    )
    # Insere o registro na tabela 'extrato'
    db.execute(
        'INSERT INTO extrato (usuario_cpf, data, descricao, valor) VALUES (?, ?, ?, ?)',
        (cpf_logado, data_hoje, 'Depósito', valor_deposito)
    )
    db.commit() 

    flash(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso!", "success")
    return redirect(url_for('dashboard'))


@app.route("/realizar_saque", methods=['POST'])
def realizar_saque():
    usuario_logado = get_usuario_logado()
    if not usuario_logado:
        return redirect(url_for('login'))
    
    try:
        valor_saque = float(request.form['valor'])
    except ValueError:
        flash("Valor de saque inválido.", "danger")
        return redirect(url_for('sacar'))

    if valor_saque <= 0:
        flash("O valor do saque deve ser positivo.", "danger")
        return redirect(url_for('sacar'))
        
    # Valida se há saldo suficiente 
    if valor_saque > usuario_logado['saldo']:
        flash("Saldo insuficiente. Você não pode sacar este valor.", "danger")
        return redirect(url_for('sacar'))
        
    db = get_db_connection()
    data_hoje = datetime.now().strftime('%d/%m/%Y')
    cpf_logado = usuario_logado['cpf']

    # Atualizar o saldo
    db.execute(
        'UPDATE usuarios SET saldo = saldo - ? WHERE cpf = ?',
        (valor_saque, cpf_logado)
    )
    # Adicionar ao extrato (valor negativo)
    db.execute(
        'INSERT INTO extrato (usuario_cpf, data, descricao, valor) VALUES (?, ?, ?, ?)',
        (cpf_logado, data_hoje, 'Saque', -valor_saque)
    )
    db.commit()
    
    flash(f"Saque de R$ {valor_saque:.2f} realizado com sucesso!", "success")
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(debug=True)