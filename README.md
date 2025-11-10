# 🏦 NeoBank - Sistema Bancário Simples com Flask

Este projeto é uma simulação completa de um sistema bancário digital, apelidado de **NeoBank**. O sistema foi construído do zero utilizando **Python** com o micro-framework **Flask** para o back-end, **SQLite** para a persistência de dados e **HTML/CSS puro** para um front-end moderno e responsivo.

O design se destaca pelo uso de **Glassmorphism** (efeito de vidro fosco), um fundo de gradiente animado e um layout "split-screen" para as telas de autenticação.


## ✨ Funcionalidades

* **Autenticação de Usuário:**
    * Sistema de **Cadastro** (CREATE) para novos clientes.
    * Sistema de **Login** (READ) com validação de CPF e senha.
    * Gerenciamento de **Sessão** (o usuário permanece logado).
    * Função de **Logout**.

* **Operações Financeiras:**
    * **Depositar** (UPDATE) valores na conta.
    * **Sacar** (UPDATE) valores, com validação de saldo disponível.
    * **Extrato** (READ) detalhado com histórico de transações.

* **Segurança e Níveis de Acesso:**
    * **Rotas Protegidas:** O dashboard e as páginas de operações só são acessíveis após o login.
    * **Nível de Admin:** Usuários com a flag `eh_admin` têm acesso a um painel administrativo.
    * **Painel Admin:** Uma rota exclusiva (`/admin/listar_contas`) que lista todos os usuários e seus respectivos saldos no banco.

* **Interface e UX:**
    * **Design Moderno:** Interface escura (Dark Mode) com tema preto e rosa, usando "Glassmorphism".
    * **Feedback ao Usuário:** Mensagens "flash" (ex: "Depósito realizado com sucesso!", "Saldo insuficiente.") para todas as ações.
    * **Fundo Animado:** Gradiente sutil em movimento nas telas de login e cadastro.

* **Banco de Dados:**
    * **Persistência de Dados:** Uso do **SQLite** para que usuários, saldos e extratos sobrevivam a reinicializações do servidor.
    * **Relacionamento:** A tabela `extrato` é ligada à tabela `usuarios` por uma Chave Estrangeira (`FOREIGN KEY`), garantindo a integridade dos dados.

---

## 🛠️ Tecnologias Utilizadas

* **Back-end:**
    * **Python 3**
    * **Flask** (Para roteamento, lógica de servidor, gerenciamento de sessão e renderização de templates Jinja2)
* **Banco de Dados:**
    * **SQLite 3** (Armazenamento de dados local baseado em arquivo)
* **Front-end:**
    * **HTML5**
    * **CSS3** (Variáveis CSS, Animações `@keyframes`, Layout Flexbox/Grid, Efeito Backdrop Filter)

---

## 🚀 Como Executar o Projeto Localmente

Siga os passos abaixo para rodar o NeoBank na sua máquina.

### 1. Pré-requisitos

* É necessário ter o [Python 3](https://www.python.org/downloads/) instalado em sua máquina.

### 2. Instalação

1.  Clone este repositório:
    ```bash
    git clone https://github.com/MaduSantoss/sistema_bancario-neo_bank.git
    cd SEU-REPOSITORIO
    ```

2.  (Opcional, mas recomendado) Crie e ative um ambiente virtual:
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Instale a única dependência (Flask):
    ```bash
    pip install Flask
    ```

### 3. Inicialização do Banco de Dados

**Atenção:** Este passo só precisa ser executado **uma única vez**.

Rode o script `init_db.py` para criar o arquivo `banco.db` e inserir o usuário administrador padrão:

```bash
python init_db.py
```

### 4. Execução da Aplicação

1.  Inicie o servidor Flask:
    ```bash
    python app.py
    ```

2.  Abra seu navegador e acesse:
    `http://127.0.0.1:5000/`

---

## 👤 Credenciais de Teste (Admin)

Use as credenciais abaixo (criadas pelo `init_db.py`) para acessar o painel de administrador:

* **Usuário (CPF):** `11122233344`
* **Senha:** `admin`
