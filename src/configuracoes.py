import flet as ft
from typing import Type
from principal import Principal
from banco_de_dados import BancoDeDados
from styles import button_style, button_style_reverse, _light, _dark

"""
------------------------------------------------ Classe Configuracoes ------------------------------------------------
Entradas: Page e Principal
Saídas: -
Descrição: Exibe um pop-up na tela do usuário que permite alterar a senha de login ou deletar a conta logada.
----------------------------------------------------------------------------------------------------------------------
"""
class Configuracoes:
    def __init__(self, page: ft.Page, principal: Type[Principal]) -> None:
        self.page = page
        self.principal = principal
        
        self.__bd = self.principal.bd                               #Obtém a conexão com o banco de dados inicializado na classe Principal
        self.__usuario_id = None

        #Atributos Flet
        self.seta_voltar = ft.IconButton(
            icon = ft.icons.ARROW_BACK,
            icon_color = "grey700",
            on_click = lambda _: self.abrir_configuracoes()
        )

        self.fechar = ft.IconButton(
            icon = ft.icons.CLOSE,
            icon_color = "grey700",
            on_click = lambda _: self.fechar_dialog()
        )

    @property
    def usuario_id(self) -> int:
        return self.__usuario_id                                           #Obtem o ID do usuário
    
    @usuario_id.setter
    def usuario_id(self, usuario_id: int) -> None:
        self.__usuario_id = usuario_id                                     #Atualiza o ID do usuário.

    def trocar_senha(self, nova_senha: str) -> None:
        BancoDeDados.trocar_senha(self.__bd, self.__usuario_id, nova_senha) #Altera a senha do usuário no Banco de Dados.
        self.fechar_dialog()
        self.page.go("/login")

    def apagar_conta(self) -> None:
        BancoDeDados.apagar_conta(self.__bd, self.__usuario_id)             #Apaga a conta do usuário no Banco de Dados.
        self.fechar_dialog()
        self.page.go("/login")
    
    def fechar_dialog(self) -> None:
        self.dialog.open = False                                          #Fecha o diálogo de configuração.
        self.page.update()

    def voltar(self) -> None:
        self.abrir_configuracoes()                                        #Volta para o menu de configurações.
    
    """
    ----------------------------------------------------------------------------------------------------------------------
                                                  Método abrir_configuracoes
    Entradas: -
    Saídas: -
    Descrição: Exibe um pop-up na tela do usuário com 2 botões. Cria a interface do Menu Configurações.
    ----------------------------------------------------------------------------------------------------------------------
    """
    def abrir_configuracoes(self) -> None:

        self.abrir_trocar_senha = ft.ElevatedButton(
            text = "Alterar Senha",
            on_click = lambda _: self.tela_trocar_senha(),
            width = 400,
            style = button_style_reverse if self.page.theme_mode == ft.ThemeMode.LIGHT else button_style,
        )

        self.abrir_apagar_conta = ft.ElevatedButton(
            text = "Apagar Conta",
            on_click = lambda _: self.tela_apagar_conta(),
            width = 400,
            style = button_style_reverse if self.page.theme_mode == ft.ThemeMode.LIGHT else button_style
        )

        self.dialog = ft.AlertDialog(
            modal = True,
            title = ft.Row(
                controls=[
                    ft.Text(
                        value = "Configurações",
                        size = 20,
                        weight = "w800"
                    ),
                    self.fechar
                ],
                alignment = "spaceBetween"
            ),
            content = ft.Container(
                content =ft.Column(
                    controls = [
                        self.abrir_trocar_senha,
                        self.abrir_apagar_conta
                    ],
                    alignment = "center",
                ),
                width=300,
                height=200,
                padding=20,
            ),
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    """
    ----------------------------------------------------------------------------------------------------------------------
                                                  Método tela_trocar_senha
    Entradas: -
    Saídas: -
    Descrição: Exibe um pop-up na tela do usuário com 1 campo de texto e 1 botão. Define a tela 'Alterar Senha
    ----------------------------------------------------------------------------------------------------------------------
    """
    def tela_trocar_senha(self) -> None: 
        nova_senha_field = ft.TextField(
            label = "Nova Senha",
            password = True,
            can_reveal_password = True,
            border = _light if self.page.theme_mode == ft.ThemeMode.LIGHT else _dark,
            label_style = ft.TextStyle(
                color = "black87" if self.page.theme_mode == ft.ThemeMode.LIGHT else "white",
                weight = "bold",
                font_family = "Arial Rounded MT Bold",
                size = 14
            ),
            cursor_height = 15,
            cursor_width = 1,
            cursor_color = "black87" if self.page.theme_mode == ft.ThemeMode.LIGHT else "white",
            color = "black87" if self.page.theme_mode == ft.ThemeMode.LIGHT else "black54",
            border_width = 2
        )

        trocar_senha_button = ft.ElevatedButton(
            text = "Salvar Alterações",
            on_click = lambda _: self.trocar_senha(nova_senha_field.value),
            style = button_style_reverse if self.page.theme_mode == ft.ThemeMode.LIGHT else button_style,
        )
        
        self.dialog.title.controls = [
            self.seta_voltar,
            ft.Text(
                value = "Alterar Senha",
                size = 20,
                weight = "w800"
            ),
            self.fechar
        ]

        self.dialog.content.content.controls = [
            nova_senha_field,
            trocar_senha_button
        ]
        self.page.update()

    """
    ----------------------------------------------------------------------------------------------------------------------
                                                  Método tela_apagar_conta
    Entradas: -
    Saídas: -
    Descrição: Exibe um pop-up na tela do usuário com 1 texto e 1 botão. Define a tela 'Apagar Conta'.
    ----------------------------------------------------------------------------------------------------------------------
    """
    def tela_apagar_conta(self) -> None:
        apagar_conta_button = ft.ElevatedButton(
            text = "Apagar Conta",
            on_click = lambda _: self.apagar_conta(),
            style = ft.ButtonStyle(
                bgcolor = "red",
                color = "white",
                shape = ft.RoundedRectangleBorder(radius=5)
            )
        )
        
        self.dialog.title.controls = [
            self.seta_voltar,
            ft.Text(
                value = "Apagar Conta",
                size = 20,
                weight = "w800"
            ),
            self.fechar
        ]

        self.dialog.content.content.controls = [
            ft.Text(
                value = "Tem certeza que deseja apagar sua conta?",
                color = "black87" if self.page.theme_mode == ft.ThemeMode.LIGHT else "white"
            ),
            apagar_conta_button
        ]
        
        self.page.update()