import flet as ft

class Login():
    def __init__(self, page: ft.Page):
        self.page = page

    def verificaUsuario(self, usuario, senha):
        self.usuario = usuario
        self.senha = senha
        usuarioExiste = False
        senhaExiste = False
        with open('arquivo.txt', 'r') as arquivo:
            for linha in arquivo:
                usuarioSalvo, senhaSalva = linha.strip().split(', ')
                if usuarioSalvo == self.usuario:
                    usuarioExiste = True
                    if senhaSalva == self.senha:
                        senhaExiste = True
                    break
        return(usuarioExiste, senhaExiste)

    def entrar(self,login):
        usuario = login.content.controls[0].content.controls[2].content.value
        senha = login.content.controls[0].content.controls[3].content.value
        login.content.controls[0].content.controls[2].content.value = f''
        login.content.controls[0].content.controls[3].content.value = f''
        usuarioExiste, senhaExiste = self.verificaUsuario(usuario, senha)
        alerta = ft.Container(
            content=(
                ft.Text(
                    value='Usuário e senha incorreta',
                    color=ft.colors.RED
                )
            )
        )
        alerta_preenchimento = ft.Container(
            content=(
                ft.Text(
                    value='Por favor, preencha todos os campos',
                    color=ft.colors.RED
                )
            )
        )
        if len(usuario.strip()) == 0 or len(senha.strip()) == 0:
            if len(login.content.controls[0].content.controls) < 7:
                login.content.controls[0].content.controls.append(alerta_preenchimento)
        else:
            if usuarioExiste and senhaExiste:
                self.page.go('/')
            else:
                if len(login.content.controls[0].content.controls) < 7:
                    login.content.controls[0].content.controls.append(alerta)
        self.page.update()
    
    def tela_login(self):
        login = ft.Container(
            content=(
                ft.Row(
                    controls=[
                        ft.Container(
                            content=(
                                ft.Column(
                                    controls=[
                                        ft.Image(
                                            src='/images/banana.webp',
                                            height=45
                                        ),
                                        ft.Container(
                                            content=(
                                                ft.Text('KanBanana',
                                                        color=ft.colors.BLACK87,
                                                        size=23,
                                                        weight=ft.FontWeight.BOLD,
                                                        font_family='Annai MN'
                                                    )
                                            ),
                                        ),
                                        ft.Container(
                                            content=(
                                                ft.TextField(
                                                    height=45,
                                                    width=200,
                                                    label='Usuário',
                                                    border_color=ft.colors.BLACK87,
                                                    autofocus=True,
                                                    label_style=ft.TextStyle(
                                                        color=ft.colors.BLACK54,
                                                        weight=ft.FontWeight.BOLD, 
                                                        font_family='Annai MN',
                                                        size=14
                                                    ),
                                                    text_style=ft.TextStyle(font_family='Annai MN'),
                                                    cursor_height=15,
                                                    cursor_width=1,
                                                    cursor_color=ft.colors.BLACK87,
                                                    color=ft.colors.BLACK87,
                                                    border_width=2,
                                                    prefix_icon=ft.icons.PERSON,
                                                )
                                            )
                                        ),
                                        ft.Container(
                                            content=(
                                                ft.TextField(
                                                    height=45,
                                                    width=200,
                                                    label='Senha',
                                                    border_color=ft.colors.BLACK87,
                                                    label_style=ft.TextStyle(
                                                        color=ft.colors.BLACK54,
                                                        weight=ft.FontWeight.BOLD,
                                                        font_family='Annai MN',
                                                        size=14
                                                    ),
                                                    cursor_height=15,
                                                    cursor_width=1,
                                                    cursor_color=ft.colors.BLACK87,
                                                    color=ft.colors.BLACK87,
                                                    password=True,
                                                    border_width=2,
                                                    prefix_icon=ft.icons.LOCK,
                                                )
                                            )
                                        ),
                                        ft.FilledButton(
                                            text='Login',
                                            style=ft.ButtonStyle(
                                                color={
                                                    ft.MaterialState.DEFAULT: ft.colors.BLACK87,
                                                    ft.MaterialState.HOVERED: ft.colors.WHITE
                                                },
                                                bgcolor={
                                                    ft.MaterialState.DEFAULT: ft.colors.WHITE,
                                                    ft.MaterialState.HOVERED: ft.colors.BLACK87
                                                },
                                                shape=ft.RoundedRectangleBorder(radius=10)
                                            ),
                                            icon=ft.icons.LOGIN,
                                            width=200,
                                            on_click=lambda _: self.entrar(login)
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.Text(
                                                    value='Não tem uma conta?',
                                                    style=ft.TextStyle(
                                                        color=ft.colors.BLACK87
                                                    ),
                                                    size=14
                                                ),
                                                ft.TextButton(
                                                    text='Registre-se',
                                                    style=ft.ButtonStyle(
                                                        color={
                                                            ft.MaterialState.DEFAULT: ft.colors.BLACK54,
                                                            ft.MaterialState.HOVERED: ft.colors.WHITE
                                                        },
                                                        bgcolor={
                                                            ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
                                                            ft.MaterialState.HOVERED: ft.colors.BLACK87
                                                        }
                                                    ),
                                                    on_click=lambda _: self.page.go('/registro')
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=True
                                )
                            ),
                            border=ft.border.all(1,ft.colors.GREY_50),
                            alignment= ft.alignment.center,
                            height=500,
                            width=300,
                            border_radius=20,
                            bgcolor=ft.colors.with_opacity(600000,ft.colors.GREY_100),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                )
            ),
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    ft.colors.YELLOW,ft.colors.YELLOW_200
                ]
            )
        )
        return(login)