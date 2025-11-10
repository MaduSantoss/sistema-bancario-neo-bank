import sqlite3

# Conecta ao banco 
connection = sqlite3.connect('banco.db')

# cursor para executar comandos SQL
with connection:
    cursor = connection.cursor()
    
    # CRIA A TABELA DE USUÁRIOS
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        cpf TEXT PRIMARY KEY NOT NULL,
        nome TEXT NOT NULL,
        data_nascimento TEXT NOT NULL,
        endereco TEXT NOT NULL,
        senha TEXT NOT NULL,
        agencia TEXT NOT NULL,
        conta TEXT NOT NULL UNIQUE,
        saldo REAL NOT NULL,
        eh_admin INTEGER NOT NULL DEFAULT 0 
    )
    ''')
    
    # CRIA A TABELA DE EXTRATO
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS extrato (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_cpf TEXT NOT NULL,
        data TEXT NOT NULL,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        FOREIGN KEY (usuario_cpf) REFERENCES usuarios (cpf)
    )
    ''')
    
    print("Tabelas 'usuarios' e 'extrato' criadas (ou já existentes).")

    # INSERE O USUÁRIO ADMIN (SE NÃO EXISTIR)
    try:
        cursor.execute('''
        INSERT INTO usuarios (
            cpf, nome, data_nascimento, endereco, senha, 
            agencia, conta, saldo, eh_admin
        ) 
        VALUES (
            '11122233344', 'Usuário Exemplo (Admin)', '2000-01-01', 
            'Rua Admin, 123', 'admin', '0001', '12345-6', 1500.75, 1
        )
        ''')
        
        cursor.execute("INSERT INTO extrato (usuario_cpf, data, descricao, valor) VALUES (?, ?, ?, ?)",
                       ('11122233344', '28/10/2025', 'Saque Caixa Eletrônico', -100.00))
        cursor.execute("INSERT INTO extrato (usuario_cpf, data, descricao, valor) VALUES (?, ?, ?, ?)",
                       ('11122233344', '27/10/2025', 'Depósito', 350.00))
        
        print("Usuário Admin inserido com sucesso.")
        
    except sqlite3.IntegrityError:
        print("Usuário Admin (CPF 11122233344) ou Conta (12345-6) já existe.")


# Fecha a conexão com o banco de dados
connection.commit()
connection.close()

print("Banco de dados 'banco.db' inicializado.")