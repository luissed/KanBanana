import sqlite3

class BancoDeDados:
    @staticmethod
    def conectarAoBanco():
        try:
            bd = sqlite3.connect('kanbanana.db', check_same_thread=False)
            c = bd.cursor()

            c.execute('''
                CREATE TABLE IF NOT EXISTS tarefas (
                    id INTEGER PRIMARY KEY,
                    Tarefa VARCHAR(255) NOT NULL,
                    Data VARCHAR(255) NOT NULL
                )
            ''')

            c.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY,
                    usuario VARCHAR(255) NOT NULL UNIQUE,
                    senha VARCHAR(255) NOT NULL
                )
            ''')
            return bd, c  
        except Exception as e:
            print(e)
    
    @staticmethod
    def lerTarefa(bd):
        c = bd.cursor()
        c.execute('SELECT Tarefa, Data FROM tarefas')
        registros = c.fetchall()
        return registros
    
    @staticmethod
    def inserirTarefa(bd, valores):
        c = bd.cursor()
        c.execute('INSERT INTO tarefas (Tarefa, Data) VALUES (?, ?)', valores)
        bd.commit()
    
    @staticmethod
    def excluirTarefa(bd, valor):
        c = bd.cursor()
        c.execute('DELETE FROM tarefas WHERE Tarefa = ?', (valor,))
        bd.commit()
    
    @staticmethod
    def atualizarTarefa(bd, valores):
        c = bd.cursor()
        c.execute('UPDATE tarefas SET Tarefa = ? WHERE Tarefa = ?', valores)
        bd.commit()

    @staticmethod
    def inserirUsuario(bd, usuario, senha):
        c = bd.cursor()
        c.execute('INSERT INTO usuarios (usuario, senha) VALUES (?, ?)', (usuario, senha))
        bd.commit()
    
    @staticmethod
    def verificarUsuario(bd, usuario):
        c = bd.cursor()
        c.execute('SELECT * FROM usuarios WHERE usuario = ?', (usuario,))
        usuario_encontrado = c.fetchone()
        return usuario_encontrado is not None

    @staticmethod
    def verificarCredenciais(bd, usuario, senha):
        c = bd.cursor()
        c.execute('SELECT * FROM usuarios WHERE usuario = ? AND senha = ?', (usuario, senha))
        usuario_encontrado = c.fetchone()
        return usuario_encontrado is not None
