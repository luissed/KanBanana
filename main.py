import flet as ft
from login import *

def main(page: ft.Page):
    page.title = 'KanBanana'
    page.theme_mode = 'light'
    page.padding=0
    app = Login(page)

ft.app(target = main, assets_dir = 'assets')