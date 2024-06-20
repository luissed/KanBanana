import sqlite3
from datetime import date

class BancoDeDados:
    """
    --------------------------------------------------- Classe Banco de Dados ---------------------------------------------------
    Entradas: -
    Saídas: -
    Descrição: Classe para gerenciar o banco de dados SQLite, incluindo a criação de tabelas e operações CRUD (CREATE, UPDATE e DELETE).
    -----------------------------------------------------------------------------------------------------------------------------
    """

    @staticmethod
    def _conectar_ao_banco() -> tuple:
        """
        ----------------------------------------------------------------------------------------------------------------------
                                                  Método _conectar_ao_banco
        Entradas: -
        Saídas: Tuple (sqlite3.Connection, sqlite3.Cursor)
        Descrição: Conecta ao Banco de Dados SQLite e cria as tabelas 'usuarios' e 'tarefas'.
        -------------------------------------------------------------------------------------------------------------------
        """
        try:    
            bd = sqlite3.connect('kanbanana.db', check_same_thread=False)
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
        ----------------------------------------------------------------------------------------------------------------------
                                                  Método obter_tarefas
        Entradas: Banco de Dados (sqlite3.Connection), usuario_id (int)
        Saídas: Lista de tarefas (list)
        Descrição: Obtém todas as tarefas do usuário especificado e retorna os detalhes das tarefas.
        -------------------------------------------------------------------------------------------------------------------
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
        ----------------------------------------------------------------------------------------------------------------------
                                                  Método adicionar_tarefa
        Entradas: Banco de Dados (sqlite3.Connection), usuario_id (int), descricao (str), data (date)
        Saídas: -
        Descrição: Adiciona uma nova tarefa na tabela de tarefas.
        -------------------------------------------------------------------------------------------------------------------
        """
        query = "INSERT INTO tarefas (usuario_id, descricao, data, concluida, em_andamento, atrasada) VALUES (?, ?, ?, ?, ?, ?)"
        c = bd.cursor()
        c.execute(query, (usuario_id, descricao, data, False, False, False))
        bd.commit()
        c.close()

    @staticmethod
    def atualizar_tarefa(bd: sqlite3.Connection, tarefa_id: int, descricao: str, data: date, concluida: bool, em_andamento: bool, atrasada: bool) -> None:
        """
        ----------------------------------------------------------------------------------------------------------------------
                                                  Método atualizar_tarefa
        Entradas: Banco de Dados (sqlite3.Connection), tarefa_id (int), descricao (str), data (date), concluida (bool), em_andamento (bool), atrasada (bool)
        Saídas: -
        Descrição: Atualiza uma tarefa que já existe na tabela 'tarefas'.
        -------------------------------------------------------------------------------------------------------------------
        """
        query = "UPDATE tarefas SET descricao = ?, data = ?, concluida = ?, em_andamento = ?, atrasada = ? WHERE id = ?"
        c = bd.cursor()
        c.execute(query, (descricao, data, concluida, em_andamento, atrasada, tarefa_id))
        bd.commit()
        c.close()

    @staticmethod
    def remover_tarefa(bd: sqlite3.Connection, tarefa_id: int) -> None:
        """
        ----------------------------------------------------------------------------------------------------------------------
                                                  Método remover_tarefa
        Entradas: Banco de Dados (sqlite3.Connection), tarefa_id (int)
        Saídas: -
        Descrição: Apaga do banco de dados a tarefa com o ID fornecido.
        -------------------------------------------------------------------------------------------------------------------
        """
        query = "DELETE FROM tarefas WHERE id = ?"
        c = bd.cursor()
        c.execute(query, (tarefa_id,))
        bd.commit()
        c.close()

    @staticmethod
    def inserir_usuario(bd: sqlite3.Connection, usuario: str, senha: str) -> None:
        """
        ----------------------------------------------------------------------------------------------------------------------
                                                  Método inserir_usuario
        Entradas: Banco de Dados (sqlite3.Connection), usuario (str), senha (str)
        Saídas: -
        Descrição: Insere na tabela 'usuarios' o usuário e a senha passados como argumento para a função.
        -------------------------------------------------------------------------------------------------------------------
        """
        query = "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)"
        c = bd.cursor()
        c.execute(query, (usuario, senha))
        bd.commit()
        c.close()

    @staticmethod
    def verificar_usuario(bd: sqlite3.Connection, usuario: str) -> tuple :
        """
        ----------------------------------------------------------------------------------------------------------------------
                                                  Método verificar_usuario
        Entradas: Banco de Dados (sqlite3.Connection), usuario (str)
        Saídas: Informações do usuário (tuple)
        Descrição: Verifica se o usuário já existe no Banco de Dados no momento de fazer um novo registro.
        -------------------------------------------------------------------------------------------------------------------
        """
        query = "SELECT * FROM usuarios WHERE usuario = ?"
        c = bd.cursor()
        c.execute(query, (usuario,))
        usuario_encontrado = c.fetchone()
        c.close()
        return usuario_encontrado 
    
    @staticmethod
    def verificar_credenciais(bd: sqlite3.Connection, usuario: str, senha: str) -> tuple :
        """
        ----------------------------------------------------------------------------------------------------------------------
                                                  Método verificar_credenciais
        Entradas: Banco de Dados (sqlite3.Connection), usuario (str), senha (str)
        Saídas: Tuple (tupla) 
        Descrição: Verifica se as credenciais inseridas correspondem às cadastradas no banco de dados.
        -------------------------------------------------------------------------------------------------------------------
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
        ----------------------------------------------------------------------------------------------------------------------
                                                  Método trocar_senha
        Entradas: Banco de Dados (sqlite3.Connection), usuario_id (int), nova_senha (str)
        Saídas: -
        Descrição: Modifica o valor de senha do usuário com o ID especificado.
        -------------------------------------------------------------------------------------------------------------------
        """
        query = "UPDATE usuarios SET senha = ? WHERE id = ?"
        c = bd.cursor()
        c.execute(query, (nova_senha, usuario_id))
        bd.commit()
        c.close()

    @staticmethod
    def apagar_conta(bd: sqlite3.Connection, usuario_id: int) -> None:
        """
        ----------------------------------------------------------------------------------------------------------------------
                                                  Método apagar_conta
        Entradas: Banco de Dados (sqlite3.Connection), usuario_id (int)
        Saídas: -
        Descrição: Apaga o usuário e as tarefas do usuário com o ID especificado.
        -------------------------------------------------------------------------------------------------------------------
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
