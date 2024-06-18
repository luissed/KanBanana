import sqlite3
from datetime import date

class BancoDeDados:
    """
    Classe para gerenciar o banco de dados SQLite, incluindo a criação de tabelas e operações CRUD(CREATE, UPDATE e DELETE).
    """

    @staticmethod
    def _conectar_ao_banco()-> tuple:
        """
        Conecta ao Banco de Dados SQLite e cria as tabelas 'usuarios' e 'tarefas'.
        """
        try:    
            bd = sqlite3.connect('../kanbanana.db', check_same_thread=False)
            c = bd.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario VARCHAR(255) NOT NULL UNIQUE,
                    senha VARCHAR(255) NOT NULL
                )
            ''')
            c.execute('''
                CREATE TABLE IF NOT EXISTS tarefas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    descricao VARCHAR(255) NOT NULL,
                    data DATE NOT NULL,
                    concluida BOOLEAN NOT NULL DEFAULT 0,
                    em_andamento BOOLEAN NOT NULL DEFAULT 0,
                    atrasada BOOLEAN NOT NULL DEFAULT 0,
                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
                )
            ''')
            return bd, c
        except Exception as e:
            print(e)

    @staticmethod
    def obter_tarefas(bd: sqlite3.Connection, usuario_id: int) -> list:
        """
        Obtém todas as tarefas do usuário especificado e retorna os detalhes das tarefas.
        """
        query = "SELECT id, descricao, data, concluida, em_andamento, atrasada FROM tarefas WHERE usuario_id = ?"
        c = bd.cursor()
        c.execute(query, (usuario_id,))
        tarefas = c.fetchall()
        c.close()
        return tarefas

    @staticmethod
    def adicionar_tarefa(bd: sqlite3.Connection, usuario_id: int, descricao: str, data: date) -> None:
        """
        Adiciona uma nova tarefa na tabela de tarefas.
        """
        query = "INSERT INTO tarefas (usuario_id, descricao, data, concluida, em_andamento, atrasada) VALUES (?, ?, ?, ?, ?, ?)"
        c = bd.cursor()
        c.execute(query, (usuario_id, descricao, data, False, False, False))
        bd.commit()
        c.close()

    @staticmethod
    def atualizar_tarefa(bd: sqlite3.Connection, tarefa_id: int, descricao: str, data: date, concluida: bool, em_andamento: bool, atrasada: bool) -> None:
        """
        Atualiza uma tarefa que já existe na tabela 'tarefas'.
        """
        query = "UPDATE tarefas SET descricao = ?, data = ?, concluida = ?, em_andamento = ?, atrasada = ? WHERE id = ?"
        c = bd.cursor()
        c.execute(query, (descricao, data, concluida, em_andamento, atrasada, tarefa_id))
        bd.commit()
        c.close()

    @staticmethod
    def remover_tarefa(bd: sqlite3.Connection, tarefa_id: int) -> None:
        """
        Apaga do banco de dados a tarefa com o ID fornecido.
        """
        query = "DELETE FROM tarefas WHERE id = ?"
        c = bd.cursor()
        c.execute(query, (tarefa_id,))
        bd.commit()
        c.close()

    @staticmethod
    def inserir_usuario(bd: sqlite3.Connection, usuario: str, senha: str) -> None:
        """
        Insere na tabela 'usuarios' o usuário e a senha passados como argumento para a função.
        """
        query = "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)"
        c = bd.cursor()
        c.execute(query, (usuario, senha))
        bd.commit()
        c.close()

    @staticmethod
    def verificar_usuario(bd: sqlite3.Connection, usuario: str) -> tuple | None:
        """
        Verifica se o usuário já existe no Banco de Dados no momento de fazer um novo registro.
        """
        query = "SELECT * FROM usuarios WHERE usuario = ?"
        c = bd.cursor()
        c.execute(query, (usuario,))
        usuario_encontrado = c.fetchone()
        c.close()
        return usuario_encontrado is not None

    @staticmethod
    def verificar_credenciais(bd: sqlite3.Connection, usuario: str, senha: str) -> tuple:
        """
        Verifica se as credenciais inseridas correspondem às cadastradas no banco de dados.
        """
        query = "SELECT * FROM usuarios WHERE usuario = ? AND senha = ?"
        c = bd.cursor()
        c.execute(query, (usuario, senha))
        usuario_encontrado = c.fetchone()
        c.close()
        return usuario_encontrado

    @staticmethod
    def trocar_senha(bd: sqlite3.Connection, usuario_id: int, nova_senha: str) -> None:
        """
        Modifica o valor de senha do usuário com o ID especificado.
        """
        query = "UPDATE usuarios SET senha = ? WHERE id = ?"
        c = bd.cursor()
        c.execute(query, (nova_senha, usuario_id))
        bd.commit()
        c.close()

    @staticmethod
    def apagar_conta(bd: sqlite3.Connection, usuario_id: int) -> None:
        """
        Apaga o usuário e as tarefas do usuário com o ID especificado.
        """
        query = "DELETE FROM usuarios WHERE id = ?"
        c = bd.cursor()
        c.execute(query, (usuario_id,))
        bd.commit()
        c.close()

        query = "DELETE FROM tarefas WHERE usuario_id = ?"
        c = bd.cursor()
        c.execute(query, (usuario_id,))
        bd.commit()
        c.close()
