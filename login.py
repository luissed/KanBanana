import flet as ft

class Login():
    def __init__(self, page: ft.Page):
        self.page = page   
        self.page.window_min_height = 600
        self.page.window_min_width = 400
        self.tela_login()

    def verificaLogin(self, usuario, senha):
        self.usuario = usuario
        self.senha = senha
        usuarioVerifica = f'{self.usuario}, {self.senha}\n'
        usuarioExiste = False
        with open('arquivo.txt', 'r') as arquivo:
            for linha in arquivo:
                if linha.strip() == usuarioVerifica.strip():
                    usuarioExiste = True
                break
        return(usuarioExiste)
    
    def verificaUsuario(self, usuario):
        self.usuario = usuario
        usuarioExiste = False
        with open('arquivo.txt', 'r') as arquivo:
            for linha in arquivo:
                usuarioVerifica = linha.strip().split(',')
                if linha.strip() == usuarioVerifica.strip():
                    usuarioExiste = True
                break
        return(usuarioExiste)

    def registrar(self, registro):
        usuario = registro.content.controls[0].content.controls[2].content.value
        senha = registro.content.controls[0].content.controls[3].content.value
        registro.content.controls[0].content.controls[2].content.value = f''
        registro.content.controls[0].content.controls[3].content.value = f''
        usuarioExiste = False
        alerta = ft.Container(
            content=(
                ft.Text(
                    value='Usuário já existe',
                    color=ft.colors.RED
                )
            )
        )
        with open('arquivo.txt', 'r+') as arquivo:
            for linha in arquivo:
                usuarioVerifica, senhaVerifica = linha.strip().split(',')
                if usuarioVerifica == usuario:
                    usuarioExiste = True
                    break
            if usuarioExiste:
                if len(registro.content.controls[0].content.controls) < 7:
                    registro.content.controls[0].content.controls.append(alerta)
            else:
                arquivo.write(f'{usuario}, {senha}\n')
                self.tela_certa(usuario)
        self.page.update()

    def entrar(self,login):
        usuario = login.content.controls[0].content.controls[2].content.value
        senha = login.content.controls[0].content.controls[3].content.value
        usuarioExiste = self.verificaLogin(usuario, senha)
        login.content.controls[0].content.controls[2].content.value = f''
        login.content.controls[0].content.controls[3].content.value = f''
        if usuarioExiste:
            self.tela_certa(usuario)
        else:
            alerta = ft.Container(
                content=(
                    ft.Text(
                        value='Usuário e senha incorreta',
                        color=ft.colors.RED
                    )
                )
            )
            if len(login.content.controls[0].content.controls) < 7:
                login.content.controls[0].content.controls.append(alerta)
        self.page.update()
    
    def tela_login(self):
        self.page.clean()
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
                                                        color=ft.colors.BLACK87,
                                                        weight=ft.FontWeight.BOLD, 
                                                        font_family='Annai MN'
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
                                                        color=ft.colors.BLACK87,
                                                        weight=ft.FontWeight.BOLD,
                                                        font_family='Annai MN'),
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
                                                overlay_color=ft.colors.BLACK87,
                                                bgcolor=ft.colors.WHITE,
                                                shape=ft.RoundedRectangleBorder(radius=10)
                                            ),
                                            icon=ft.icons.LOGIN,
                                            width=200,
                                            on_click=lambda _: self.entrar(login)
                                        ),
                                        ft.FilledButton(
                                            text='Registre-se',
                                            style=ft.ButtonStyle(
                                                color={
                                                    ft.MaterialState.DEFAULT: ft.colors.BLACK87,
                                                    ft.MaterialState.HOVERED: ft.colors.WHITE
                                                },
                                                overlay_color=ft.colors.BLACK87,
                                                bgcolor=ft.colors.WHITE,
                                                shape=ft.RoundedRectangleBorder(radius=10)
                                            ),
                                            width=200,
                                            on_click=lambda _: self.tela_registro()
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
        self.page.add(login)

    def tela_registro(self):
        self.page.clean()
        registro = ft.Container(
            content=(
                ft.Row(
                    controls=[
                        ft.Container(
                            content=(
                                ft.Column(
                                    controls=[
                                        ft.Image(
                                            src=f'/images/banana.webp',
                                            height=45
                                        ),
                                        ft.Container(
                                            content=(
                                                ft.Text('Registre-se',
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
                                                    label='Nome do Usuário',
                                                    border_color=ft.colors.BLACK87,
                                                    autofocus=True,
                                                    label_style=ft.TextStyle(
                                                        color=ft.colors.BLACK87,
                                                        weight=ft.FontWeight.BOLD,
                                                        font_family='Annai MN'
                                                    ),
                                                    cursor_height=15,
                                                    cursor_width=1,
                                                    cursor_color=ft.colors.BLACK87,
                                                    border_width=2,
                                                    prefix_icon=ft.icons.PERSON
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
                                                        color=ft.colors.BLACK87,
                                                        weight=ft.FontWeight.BOLD,
                                                        font_family='Annai MN'
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
                                        ft.Container(
                                            content=(
                                                ft.FilledButton(
                                                    text='Registre-se',
                                                    style=ft.ButtonStyle(
                                                        color={
                                                            ft.MaterialState.DEFAULT: ft.colors.BLACK87,
                                                            ft.MaterialState.HOVERED: ft.colors.WHITE
                                                        },
                                                        overlay_color=ft.colors.BLACK87,
                                                        bgcolor=ft.colors.WHITE,
                                                        shape=ft.RoundedRectangleBorder(radius=10)
                                                    ),
                                                    width=200,
                                                    on_click=lambda _:self.registrar(registro)
                                                )
                                            )
                                        ),
                                        ft.Container(
                                            content=(
                                                ft.FilledButton(
                                                    text='Fazer Login',
                                                    style=ft.ButtonStyle(
                                                        color={
                                                            ft.MaterialState.DEFAULT: ft.colors.BLACK87,
                                                            ft.MaterialState.HOVERED: ft.colors.WHITE
                                                        },
                                                        overlay_color=ft.colors.BLACK87,
                                                        bgcolor=ft.colors.WHITE,
                                                        shape=ft.RoundedRectangleBorder(radius=10)
                                                    ),
                                                    width=200,
                                                    on_click=lambda _:self.tela_login()
                                                )
                                            )
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
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    ft.colors.YELLOW,
                    ft.colors.YELLOW_200
                ]
            ),
            expand=True
        )
        self.page.add(registro)

    def tela_certa(self, usuario):
        self.page.clean()
        prx = ft.Container(
            content=(
                ft.Row(
                    controls=[
                        ft.Text(
                            value=f'Usuário {usuario} logado com sucesso!',
                            font_family='Annai MN',
                            weight=ft.FontWeight.BOLD,
                            size=15
                        )
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            ),
            gradient=ft.LinearGradient(begin=ft.alignment.top_left,end=ft.alignment.bottom_right,colors=[ft.colors.YELLOW,ft.colors.YELLOW_200]),
            expand=True,
        )
        self.page.add(prx)
