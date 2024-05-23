import flet as ft
from typing import Type
from login import Login
from registro import Registrar
from principal import Principal

def criar_appbar(login: Type[Login], page: ft.Page) -> ft.AppBar:
    appBarItens = [
        ft.PopupMenuItem(
            text='Deslogar',
            on_click=lambda _: page.go('/login'),
        ),
        ft.PopupMenuItem(text='Configurações')
    ]

    return ft.AppBar(
        leading=ft.Image(src='/images/banana.webp'),
        leading_width=30,
        title=ft.Text(
            value='KanBanana',
            font_family='Annai MN',
            size=15,
            text_align='start'
        ),
        actions=[
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            value=login.get_usuario()
                        ),
                    ),
                    ft.Container(
                        content=ft.PopupMenuButton(
                            items=appBarItens,
                            icon=ft.icons.PERSON,
                            menu_position=ft.PopupMenuPosition.UNDER
                        ),
                        margin=ft.margin.only(left=10, right=10)
                    )
                ],
                spacing=0
            )
        ]
    )

def views_handler(page: ft.Page, login: Type[Login], registro: Type[Registrar], principal: Type[Principal]) -> ft.View:
    return {
        '/': ft.View(
            route='/',
            controls=[principal.tela_tarefa()],
            padding=0,
            appbar=criar_appbar(login, page)
        ),
        '/login': ft.View(
            route='/login',
            controls=[login.tela_login()],
            padding=0
        ),
        '/registro': ft.View(
            route='/registro',
            controls=[registro.tela_registro()],
            padding=0
        )
    }
