import flet as ft
from views import views_handler
from login import Login
from registro import Registrar
from principal import Principal
from configuracoes import Configuracoes

def main(page: ft.Page):
    page.title = 'KanBanana'
    page.theme_mode = 'light'
    page.window_min_height = 600
    page.window_min_width = 400

    principal = Principal(page)
    login = Login(page)
    registro = Registrar(page)
    configuracoes = Configuracoes(page, principal)

    def route_change(route) -> None:
        page.views.clear()
        page.views.append(
            views_handler(page, login, registro, principal, configuracoes)[page.route]
        )
        page.update()

    page.on_route_change = route_change
    page.go('/login')

ft.app(target=main, assets_dir='assets')
