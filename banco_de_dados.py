import sqlite3

class BancoDeDados:
    @staticmethod
    def conectarAoBanco():
        try:
            bd = sqlite3.connect('kanbanana.db', check_same_thread=False)
            c = bd.cursor()
            # Tabela de Usuários
            c.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario VARCHAR(255) NOT NULL UNIQUE,
                    senha VARCHAR(255) NOT NULL
                )
            ''')
            # Tabela de Tarefas
            c.execute('''
                CREATE TABLE IF NOT EXISTS tarefas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario VARCHAR(255) NOT NULL,
                    descricao VARCHAR(255) NOT NULL,
                    concluida BOOLEAN NOT NULL DEFAULT 0,
                    FOREIGN KEY(usuario) REFERENCES usuarios(usuario)
                )
            ''')
            return bd, c
        except Exception as e:
            print(e)

    @staticmethod
    def obterTarefas(bd, usuario):
        query = "SELECT id, descricao, concluida FROM tarefas WHERE usuario = ?"
        c = bd.cursor()
        c.execute(query, (usuario,))
        return c.fetchall()

    @staticmethod
    def adicionarTarefa(bd, usuario, descricao):
        query = "INSERT INTO tarefas (usuario, descricao, concluida) VALUES (?, ?, ?)"
        c = bd.cursor()
        c.execute(query, (usuario, descricao, False))
        bd.commit()

    @staticmethod
    def atualizarTarefa(bd, tarefa_id, descricao, concluida):
        query = "UPDATE tarefas SET descricao = ?, concluida = ? WHERE id = ?"
        c = bd.cursor()
        c.execute(query, (descricao, concluida, tarefa_id))
        bd.commit()

    @staticmethod
    def removerTarefa(bd, tarefa_id):
        query = "DELETE FROM tarefas WHERE id = ?"
        c = bd.cursor()
        c.execute(query, (tarefa_id,))
        bd.commit()

    @staticmethod
    def inserirUsuario(bd, usuario, senha):
        query = "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)"
        c = bd.cursor()
        c.execute(query, (usuario, senha))
        bd.commit()

    @staticmethod
    def verificarUsuario(bd, usuario):
        query = "SELECT * FROM usuarios WHERE usuario = ?"
        c = bd.cursor()
        c.execute(query, (usuario,))
        usuario_encontrado = c.fetchone()
        return usuario_encontrado is not None

    @staticmethod
    def verificarCredenciais(bd, usuario, senha):
        query = "SELECT * FROM usuarios WHERE usuario = ? AND senha = ?"
        c = bd.cursor()
        c.execute(query, (usuario, senha))
        usuario_encontrado = c.fetchone()
        return usuario_encontrado is not None
