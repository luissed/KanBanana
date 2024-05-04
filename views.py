import flet as ft
from typing import Type
from login import Login
from registro import Registrar
from principal import Principal

def views_handler(page: ft.Page, login: Type[Login], registro: Type[Registrar], principal: Type[Principal]):
    return {
        '/':ft.View(
            route='/',
            controls=[
                principal.tela()
            ],
            padding=0
        ),
        '/login':ft.View(
            route='/login',
            controls=[
                login.tela_login()
            ],
            padding=0
        ),
        '/registro':ft.View(
            route='/registro',
            controls=[
                registro.tela_registro()
            ],
            padding=0
        )
    }