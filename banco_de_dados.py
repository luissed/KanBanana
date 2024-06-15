import sqlite3

class BancoDeDados():
    @staticmethod
    def _conectar_ao_banco():
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
                    concluida BOOLEAN NOT NULL DEFAULT 0,
                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
                )
            ''')
            return bd, c
        except Exception as e:
            print(e)

    @staticmethod
    def obter_tarefas(bd, usuario_id):
        query = "SELECT id, descricao, concluida FROM tarefas WHERE usuario_id = ?"
        c = bd.cursor()
        c.execute(query, (usuario_id,))
        tarefas = c.fetchall()
        c.close()  
        return tarefas

    @staticmethod
    def adicionar_tarefa(bd, usuario_id, descricao):
        query = "INSERT INTO tarefas (usuario_id, descricao, concluida) VALUES (?, ?, ?)"
        c = bd.cursor()
        c.execute(query, (usuario_id, descricao, False))
        bd.commit()
        c.close()  

    @staticmethod
    def atualizar_tarefa(bd, tarefa_id, descricao, concluida):
        query = "UPDATE tarefas SET descricao = ?, concluida = ? WHERE id = ?"
        c = bd.cursor()
        c.execute(query, (descricao, concluida, tarefa_id))
        bd.commit()
        c.close() 

    @staticmethod
    def remover_tarefa(bd, tarefa_id):
        query = "DELETE FROM tarefas WHERE id = ?"
        c = bd.cursor()
        c.execute(query, (tarefa_id,))
        bd.commit()
        c.close()  

    @staticmethod
    def inserir_usuario(bd, usuario, senha):
        query = "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)"
        c = bd.cursor()
        c.execute(query, (usuario, senha))
        bd.commit()
        c.close()  

    @staticmethod
    def verificar_usuario(bd, usuario):
        query = "SELECT * FROM usuarios WHERE usuario = ?"
        c = bd.cursor()
        c.execute(query, (usuario,))
        usuario_encontrado = c.fetchone()
        c.close() 
        return usuario_encontrado is not None

    @staticmethod
    def verificar_credenciais(bd, usuario, senha):
        query = "SELECT id FROM usuarios WHERE usuario = ? AND senha = ?"
        c = bd.cursor()
        c.execute(query, (usuario, senha))
        usuario_encontrado = c.fetchone()
        c.close()  
        return usuario_encontrado

    @staticmethod
    def trocar_senha(bd, usuario_id, nova_senha):
        try:
            query = "UPDATE usuarios SET senha = ? WHERE id = ?"
            c = bd.cursor()
            c.execute(query, (nova_senha, usuario_id))
            bd.commit()
            c.close()
            print(f"Senha do usuário {usuario_id} alterada com sucesso.")
        except Exception as e:
            print(f"Erro ao alterar a senha: {e}")

    @staticmethod
    def apagar_conta(bd, usuario_id):
        try:
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
        except Exception as e:
            print(f"Erro ao apagar a conta: {e}")

