import flet as ft
from typing import Type
from styles import alerta, button_style_login, button_style_registrar, bg_gradient
from banco_de_dados import BancoDeDados
from principal import Principal
from configuracoes import Configuracoes

"""
--------------------------------------------------- Classe Login ---------------------------------------------------
Entradas: Page
Saídas: -
Descrição: Configura a tela do aplicativo para o login, com os seguintes elementos:
            - Dois campos de texto para usuário e senha, respectivamente.
            - Dois botões: um para login e outro para registrar-se.
            - Logo e nome do aplicativo.
          Além disso, nesta classe é feita a verificação do usuário e senha para o login.
--------------------------------------------------------------------------------------------------------------------
"""
class Login():
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self._usuario = ""
        self._senha = ""
        self._bd, self._c = BancoDeDados._conectar_ao_banco()

    @property
    def usuario(self) -> str:
        return self._usuario

    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método verifica_usuario
    Entradas: -
    Saídas: Booleano (True se o usuário existe, None caso contrário)
    Descrição: Verifica as credenciais do usuário e retorna o ID do usuário se encontrado.
    --------------------------------------------------------------------------------------------------------------------
    """
    def verifica_usuario(self) -> bool:
        usuario_encontrado = BancoDeDados.verificar_credenciais(self._bd, self._usuario, self._senha)
        if usuario_encontrado:
            return usuario_encontrado[0]
        else:
            return None

    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método entrar
    Entradas: login, principal, configuracoes
    Saídas: -
    Descrição: Recebe os valores inseridos nos campos de texto e os envia para o método verifica_usuario.
               Com base nisso, realiza o login ou exibe um alerta na tela, utilizando as variáveis login, principal e 
               configuracoes para configurar o comportamento da interface.
    --------------------------------------------------------------------------------------------------------------------
    """
    def entrar(self, login: ft.Container, principal: Type[Principal], configuracoes: Type[Configuracoes]) -> None:
        self._usuario = login.content.controls[0].content.controls[2].content.value
        self._senha = login.content.controls[0].content.controls[3].content.value
        login.content.controls[0].content.controls[2].content.value = f''
        login.content.controls[0].content.controls[3].content.value = f''

        if len(self._usuario.strip()) == 0 or len(self._senha.strip()) == 0:
            if len(login.content.controls[0].content.controls) < 7:
                login.content.controls[0].content.controls.append(alerta['preenchimento'])
            elif len(login.content.controls[0].content.controls) == 7:
                login.content.controls[0].content.controls.pop()
                login.content.controls[0].content.controls.append(alerta['preenchimento'])
        else:
            usuario_id = self.verifica_usuario()
            if usuario_id:
                principal.usuario_logado = usuario_id 
                configuracoes.usuario_id = usuario_id 
                self.page.go("/")
                principal.carregar_tarefas() 
            else:
                if len(login.content.controls[0].content.controls) < 7:
                    login.content.controls[0].content.controls.append(alerta['login'])
                elif len(login.content.controls[0].content.controls) == 7:
                    login.content.controls[0].content.controls.pop()
                    login.content.controls[0].content.controls.append(alerta['login'])
        self.page.update()

    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método tela_login
    Entradas: principal, configuracoes
    Saídas: login (Retorna as configurações da interface para serem exibidas na tela.)
    Descrição: Configura a tela do aplicativo para exibir a interface de login. Esta tela inclui:
                - Dois campos de texto para inserir usuário e senha.
                - Logo e nome do aplicativo.
                - Botões de login e registrar-se.
               Utiliza as variáveis login, principal e configuracoes para definir a aparência e funcionalidade da tela.
    --------------------------------------------------------------------------------------------------------------------
    """
    def tela_login(self, principal: Type[Principal], configuracoes: Type[Configuracoes]) -> ft.Container:
        self.page.theme_mode = ft.ThemeMode.LIGHT
        login = ft.Container(
            content = (
                ft.Row(
                    controls = [
                        ft.Container(
                            content = (
                                ft.Column(
                                    controls = [
                                        ft.Image(
                                            src = "/images/banana.webp",
                                            height = 45
                                        ),
                                        ft.Container(
                                            content = (
                                                ft.Text(
                                                    value = "KanBanana",
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
                                                    label = "Usuário",
                                                    border_color = "black87",
                                                    autofocus = True,
                                                    label_style=ft.TextStyle(
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
                                                    prefix_icon = ft.icons.PERSON,
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
                                                    prefix_icon = ft.icons.LOCK,
                                                    on_submit = lambda _: self.entrar(login, principal, configuracoes)
                                                )
                                            )
                                        ),
                                        ft.FilledButton(
                                            text = "Login",
                                            style = button_style_login,
                                            icon = ft.icons.LOGIN,
                                            width = 200,
                                            on_click = lambda _: self.entrar(login, principal, configuracoes)
                                        ),
                                        ft.Row(
                                            controls = [
                                                ft.Text(
                                                    value = "Não tem uma conta?",
                                                    style = ft.TextStyle(
                                                        color = "black87"
                                                    ),
                                                    size = 14
                                                ),
                                                ft.TextButton(
                                                    text = "Registre-se",
                                                    style = button_style_registrar,
                                                    on_click = lambda _: self.page.go("/registro")
                                                )
                                            ],
                                            alignment = "center",
                                        )
                                    ],
                                    alignment = "center",
                                    horizontal_alignment = "center",
                                    expand = True
                                )
                            ),
                            border = ft.border.all(1,"grey50"),
                            alignment = ft.alignment.center,
                            height = 500,
                            width = 300,
                            border_radius = 20,
                            bgcolor = ft.colors.with_opacity(600000,"grey100"),
                        )
                    ],
                    alignment = "center",
                    vertical_alignment = "center",
                    expand = True
                )
            ),
            expand = True,
            gradient = bg_gradient
        )

        return(login)