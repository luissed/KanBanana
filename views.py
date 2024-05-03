import flet as ft
from login import Login
from registro import Registrar
from principal import Principal

def views_handler(page: ft.Page):
    pri = Principal(page)
    log = Login(page)
    reg = Registrar(page)
    return {
        '/':ft.View(
            route='/',
            controls=[
                pri.tela()
            ],
            padding=0
        ),
        '/login':ft.View(
            route='/login',
            controls=[
                log.tela_login()
            ],
            padding=0
        ),
        '/registro':ft.View(
            route='/registro',
            controls=[
                reg.tela_registro()
            ],
            padding=0
        )
    }