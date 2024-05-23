from flet import *
import flet as ft
from styles import _dark, _light, toggle_style_sheet, add_style_sheet, item_style_sheet
from tarefa import Tarefa

class Principal(ft.SafeArea):
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.title: ft.Text = ft.Text("LISTA DE TAREFAS", size=20, weight="w800")
        self.toggle: ft.IconButton = ft.IconButton(**toggle_style_sheet, on_click=lambda e: self.switch(e))

        self.item: ft.TextField = ft.TextField(**item_style_sheet)
        self.add: ft.IconButton = ft.IconButton(**add_style_sheet, on_click=lambda e: self.add_item(e))

        self.area_tarefas: ft.Column = ft.Column(expand=True, spacing=18)
        self.counter: ft.Text = ft.Text("0 itens", italic=True)

    def tela_tarefa(self):
        self.main: ft.Container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        alignment="spaceBetween",
                        controls=[self.title, self.toggle],
                    ),
                    ft.Divider(height=20), 
                    ft.Divider(height=10, color="transparent"),
                    ft.Text("1. Adicione sua tarefa abaixo"),
                    ft.Row(controls=[self.item, self.add], alignment="spaceBetween"),
                    ft.Divider(height=10, color="transparent"),
                    ft.Row(
                        alignment="spaceBetween",
                        controls=[
                            ft.Text("2. Lista de tarefas"),
                            self.counter, 
                        ]
                    ),
                    self.area_tarefas,
                ],
            ),
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    ft.colors.YELLOW,
                    ft.colors.YELLOW_200
                ]
            ),
            padding=ft.padding.all(20)
        )

        self.page.theme = ft.Theme(
                appbar_theme=ft.AppBarTheme(
                    bgcolor=ft.colors.YELLOW,
                    color=ft.colors.BLACK87,
                )
            )

        self.content = self.main
        return self.content

    def item_size(self) -> None:
        if len(self.area_tarefas.controls[:]) == 1:
            self.counter.value = f"{len(self.area_tarefas.controls[:])} item"
        else:
            self.counter.value = f"{len(self.area_tarefas.controls[:])} itens"

        self.counter.update()

    def add_item(self, e) -> None:
        if self.item.value != "":
            if self.page.theme_mode == ft.ThemeMode.DARK:
                self.area_tarefas.controls.append(Tarefa(self, self.item.value, "dark"))
            else:
                self.area_tarefas.controls.append(Tarefa(self, self.item.value, "light"))

            self.area_tarefas.update()
            self.item_size()
            self.item.value = ""
            self.item.update()

        else:
            pass

    def switch(self, e) -> None:
        if self.page.theme_mode == ft.ThemeMode.DARK:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.toggle.icon_color = ft.colors.BLACK87
            self.add.icon_color = ft.colors.BLACK87
            self.item.border_color = _light

            self.page.theme = ft.Theme(
                appbar_theme=ft.AppBarTheme(
                    color=ft.colors.BLACK87,
                    bgcolor=ft.colors.YELLOW
                )
            )

            self.main.gradient = ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    ft.colors.YELLOW,
                    ft.colors.YELLOW_200
                ]
            )

            for item in self.area_tarefas.controls[:]:
                item.border = ft.border.all(1, _light)

        else:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.toggle.icon_color = ft.colors.WHITE
            self.add.icon_color = ft.colors.WHITE
            self.item.border_color = _dark

            self.page.theme = ft.Theme(
                appbar_theme=ft.AppBarTheme(
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.BLACK87
                )
            )

            self.main.gradient = ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    ft.colors.BLACK,
                    ft.colors.GREY_900
                ]
            )

            for item in self.area_tarefas.controls[:]:
                item.border = ft.border.all(1, _dark)

        self.page.update()