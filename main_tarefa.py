from flet import *
import flet as ft
from tela_tarefa import TelaTarefa

def main(page: ft.Page) -> None:
    page.theme_mode = ft.ThemeMode.DARK
    theme = ft.Theme()
    page.theme = theme

    tela_tarefa: object = TelaTarefa(page)
    page.add(tela_tarefa)
    page.update()

if __name__ == "__main__":
    app(target=main)