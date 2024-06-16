import flet as ft
from typing import Type
from principal import Principal
from banco_de_dados import BancoDeDados
from styles import button_style

class Configuracoes:
    """
    Classe que gerencia as configurações do usuário, como trocar senha e apagar conta.

    """
    def __init__(self, page: ft.Page, principal: Type[Principal]) -> None:
        """
        Inicializa a classe Configuracoes.

        """
        self.page = page
        self.principal = principal
        self.bd = self.principal.get_bd()  # Obtém a conexão com o banco de dados inicializado na classe Principal
        self.usuario_id = None
        self.dialog = None

        self.seta_voltar = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            on_click=lambda _: self.abrir_configuracoes(),
            icon_color=ft.colors.GREY_700
        )
        self.fechar = ft.IconButton(
            icon=ft.icons.CLOSE,
            on_click=lambda _: self.fechar_dialog(),
            icon_color=ft.colors.GREY_700
        )

    def atualizar_usuario_id(self, usuario_id: int) -> None:
        """
        Atualiza o ID do usuário.

        """
        self.usuario_id = usuario_id

    def trocar_senha(self, nova_senha: str) -> None:
        """
        Altera a senha do usuário no Banco de Dados.

        """
        BancoDeDados.trocar_senha(self.bd, self.usuario_id, nova_senha)
        self.fechar_dialog()
        self.page.go('/login')

    def apagar_conta(self) -> None:
        """
        Apaga a conta do usuário no Banco de Dados.
        """
        BancoDeDados.apagar_conta(self.bd, self.usuario_id)
        self.fechar_dialog()
        self.page.go('/login')

    def abrir_configuracoes(self) -> None:
        """
        Cria a interface do Menu Configurações.
        """
        abrir_trocar_senha = ft.ElevatedButton(
            text="Alterar Senha",
            on_click=lambda _: self.tela_trocar_senha(),
            width=400,
            style=button_style,
        )

        abrir_apagar_conta = ft.ElevatedButton(
            text="Apagar Conta",
            on_click=lambda _: self.tela_apagar_conta(),
            width=400,
            style=button_style,
        )

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Text("Configurações", size=20, weight="w800"),
                    self.fechar,
                ],
                alignment="spaceBetween"
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        abrir_trocar_senha,
                        abrir_apagar_conta
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=300,
                height=200,
                padding=20,
            ),
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def tela_trocar_senha(self) -> None:
        """
        Define a tela 'Alterar Senha'.
        """
        self.dialog.title.controls = [
            self.seta_voltar,
            ft.Text("Alterar Senha", size=20, weight="w800"),
            self.fechar,
        ]

        nova_senha_field = ft.TextField(
            label="Nova Senha",
            password=True,
            can_reveal_password=True,
            border_color=ft.colors.BLACK87 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
            label_style=ft.TextStyle(
                color=ft.colors.BLACK87 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
                weight=ft.FontWeight.BOLD,
                font_family='Arial Rounded MT Bold',
                size=14
            ),
            cursor_height=15,
            cursor_width=1,
            cursor_color=ft.colors.BLACK87 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
            color=ft.colors.BLACK87 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLACK54,
            border_width=2,
        )

        trocar_senha_button = ft.ElevatedButton(
            text="Salvar Alterações",
            on_click=lambda _: self.trocar_senha(nova_senha_field.value),
            style=button_style,
        )

        self.dialog.content.content.controls = [
            nova_senha_field,
            trocar_senha_button
        ]
        self.page.update()

    def tela_apagar_conta(self) -> None:
        """
        Define a tela 'Apagar Conta'.
        """
        self.dialog.title.controls = [
            self.seta_voltar,
            ft.Text("Apagar Conta", size=20, weight="w800"),
            self.fechar,
        ]

        apagar_conta_button = ft.ElevatedButton(
            text="Apagar Conta",
            on_click=lambda _: self.apagar_conta(),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.RED,
                color=ft.colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=5),
            ),
        )
        self.dialog.content.content.controls = [
            ft.Text("Tem certeza que deseja apagar sua conta?"),
            apagar_conta_button
        ]
        self.page.update()

    def fechar_dialog(self) -> None:
        """
        Fecha o diálogo de configuração.
        """
        self.dialog.open = False
        self.page.update()

    def voltar(self) -> None:
        """
        Volta para o menu de configurações.
        """
        self.abrir_configuracoes()
