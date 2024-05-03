import flet as ft

class Registrar():
    def __init__(self, page: ft.Page):
        self.page = page
    
    def verificaUsuario(self, usuario):
        self.usuario = usuario
        usuarioExiste = False
        with open('arquivo.txt', 'r') as arquivo:
            for linha in arquivo:
                usuarioSalvo, _ = linha.strip().split(', ')
                if usuarioSalvo == self.usuario:
                    usuarioExiste = True
                    break
        return(usuarioExiste)
    
    def registrar(self, registro):
        usuario = registro.content.controls[0].content.controls[2].content.value
        senha = registro.content.controls[0].content.controls[3].content.value
        registro.content.controls[0].content.controls[2].content.value = f''
        registro.content.controls[0].content.controls[3].content.value = f''
        alerta = ft.Container(
            content=(
                ft.Text(
                    value='Usuário já existe',
                    color=ft.colors.RED
                )
            )
        )
        usuarioExiste = self.verificaUsuario(usuario)
        if usuarioExiste:
            if len(registro.content.controls[0].content.controls) < 7:
                registro.content.controls[0].content.controls.append(alerta)
            self.page.update()
        else:
            with open ('arquivo.txt','r+') as arquivo:
                arquivo.write(f'{usuario}, {senha}\n')
            self.page.go('/')
    
    def tela_registro(self):
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
                                                    text_style=ft.TextStyle(font_family='Annai MN'),
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
                                                    text_style=ft.TextStyle(font_family='Annai MN'),
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
                                                    on_click=lambda _:self.page.go('/login')
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
        return(registro)