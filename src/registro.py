import flet as ft
from styles import alerta, button_style_login, bg_gradient
from banco_de_dados import BancoDeDados  

"""
--------------------------------------------------- Classe Registrar ---------------------------------------------------
Entradas: Page
Saídas: -
Descrição: Configura a tela do aplicativo para o registro, incluindo:
           - Dois campos de texto para usuário e senha.
           - Dois botões: um para registrar-se e outro para voltar à tela de login.
           - Logo e nome do aplicativo.
           Além disso, nesta classe é feita a verificação se o usuário já existe, evitando duplicação.
--------------------------------------------------------------------------------------------------------------------
"""
class Registrar():
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.__usuario = ""
        self.__senha = ""
        self.__bd, self.__c = BancoDeDados._conectar_ao_banco() 

    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método verifica_usuario
    Entradas: -
    Saídas: Booleano (True se o usuário existe, None caso contrário)
    Descrição: Verifica as credenciais do usuário e retorna o ID do usuário se encontrado.
    --------------------------------------------------------------------------------------------------------------------
    """
    def verifica_usuario(self) -> bool:
        return BancoDeDados.verificar_usuario(self.__bd, self.__usuario)
    
    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método registrar
    Entradas: registro
    Saídas: -
    Descrição: Recebe os valores inseridos nos campos de texto e os envia para o método verifica_usuario.
               Com base nisso, realiza o registro ou exibe um alerta na tela.
    --------------------------------------------------------------------------------------------------------------------
    """
    def registrar(self, registro: ft.Container) -> None:
        self.__usuario = registro.content.controls[0].content.controls[2].content.value
        self.__senha = registro.content.controls[0].content.controls[3].content.value
        registro.content.controls[0].content.controls[2].content.value = f""
        registro.content.controls[0].content.controls[3].content.value = f""
        
        if len(self.__usuario.strip()) == 0 or len(self.__senha.strip()) == 0:
            if len(registro.content.controls[0].content.controls) < 7:
                registro.content.controls[0].content.controls.append(alerta["preenchimento"])
            elif len(registro.content.controls[0].content.controls) == 7:
                registro.content.controls[0].content.controls.pop()
                registro.content.controls[0].content.controls.append(alerta["preenchimento"])
            self.page.update()
        else:
            usuarioExiste = self.verifica_usuario()
            if usuarioExiste:
                if len(registro.content.controls[0].content.controls) < 7:
                    registro.content.controls[0].content.controls.append(alerta["registro"])
                elif len(registro.content.controls[0].content.controls) == 7:
                    registro.content.controls[0].content.controls.pop()
                    registro.content.controls[0].content.controls.append(alerta["registro"])
                self.page.update()
            else:
                BancoDeDados.inserir_usuario(self.__bd, self.__usuario, self.__senha)
                self.page.go('/login')
    
    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método tela_registro
    Entradas: -
    Saídas: registro (Retorna as configurações da interface para serem exibidas na tela.)
    Descrição: Configura a tela do aplicativo para exibir a interface de registro. Esta tela inclui:
                - Dois campos de texto para inserir usuário e senha.
                - Logo e nome do aplicativo.
                - Botões de login e registrar-se.
    --------------------------------------------------------------------------------------------------------------------
    """
    def tela_registro(self) -> ft.Container:
        self.page.theme_mode = ft.ThemeMode.LIGHT
        registro = ft.Container(
            content = (
                ft.Row(
                    controls = [
                        ft.Container(
                            content = (
                                ft.Column(
                                    controls = [
                                        ft.Image(
                                            src = f"/images/banana.webp",
                                            height = 45
                                        ),
                                        ft.Container(
                                            content = (
                                                ft.Text(
                                                    value = "Registre-se",
                                                    color = "black87",
                                                    size = 23,
                                                    weight = "bold",
                                                    font_family = "Chalkboard"
                                                )
                                            ),
                                        ),
                                        ft.Container(
                                            content = (
                                                ft.TextField(
                                                    height = 45,
                                                    width = 200,
                                                    label = "Nome do Usuário",
                                                    border_color = "black87",
                                                    autofocus = True,
                                                    label_style = ft.TextStyle(
                                                        color = "black54",
                                                        weight = "bold",
                                                        font_family = "Arial Rounded MT Bold",
                                                        size = 14
                                                    ),
                                                    text_style = ft.TextStyle(font_family = "Arial"),
                                                    cursor_height = 15,
                                                    cursor_width = 1,
                                                    cursor_color = "black87",
                                                    color = "black87",
                                                    border_width = 2,
                                                    prefix_icon = ft.icons.PERSON
                                                )
                                            )
                                        ),
                                        ft.Container(
                                            content = (
                                                ft.TextField(
                                                    height = 45,
                                                    width = 200,
                                                    label = "Senha",
                                                    border_color = "black87",
                                                    label_style = ft.TextStyle(
                                                        color = "black54",
                                                        weight = "bold",
                                                        font_family = "Arial Rounded MT Bold",
                                                        size = 14
                                                    ),
                                                    text_style = ft.TextStyle(font_family = "Arial"),
                                                    cursor_height = 15,
                                                    cursor_width = 1,
                                                    cursor_color = "black87",
                                                    color = "black87",
                                                    password = True,
                                                    can_reveal_password = True,
                                                    border_width = 2,
                                                    prefix_icon = ft.icons.LOCK
                                                )
                                            )
                                        ),
                                        ft.Container(
                                            content = (
                                                ft.FilledButton(
                                                    text = "Registre-se",
                                                    style = button_style_login,
                                                    width = 200,
                                                    on_click = lambda _:self.registrar(registro)
                                                )
                                            )
                                        ),
                                        ft.Container(
                                            content = (
                                                ft.FilledButton(
                                                    text = "Fazer Login",
                                                    style = button_style_login,
                                                    width = 200,
                                                    on_click = lambda _:self.page.go("/login")
                                                )
                                            )
                                        )
                                    ],
                                    alignment = "center",
                                    horizontal_alignment = "center",
                                    expand = True
                                )
                            ),
                            border = ft.border.all(1, "grey50"),
                            alignment = ft.alignment.center,
                            height = 500,
                            width = 300,
                            border_radius = 20,
                            bgcolor = ft.colors.with_opacity(600000, "grey100"),
                        )
                    ],
                    alignment = "center",
                    vertical_alignment = "center",
                    expand = True
                )
            ),
            gradient = bg_gradient,
            expand = True
        )
        return(registro)