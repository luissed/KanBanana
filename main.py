import flet as ft
from views import views_handler
from login import Login
from registro import Registrar
from principal import Principal

def main(page: ft.Page):
    page.title = 'KanBanana'
    page.theme_mode = 'light'
    page.window_min_height = 600
    page.window_min_width = 400
    
    def route_change(route):
        page.views.clear()
        page.views.append(
            views_handler(page, Login(page), Registrar(page), Principal(page))[page.route]
        )
        page.update()
    
    page.on_route_change = route_change
    page.go('/login')

ft.app(target=main, assets_dir='assets')