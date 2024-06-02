from flet import *
import flet as ft
from styles import _dark, _light, toggle_style_sheet, add_style_sheet, item_style_sheet
from tarefa import Tarefa
from login import Login
from banco_de_dados import BancoDeDados

class Principal(ft.SafeArea):
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.title: ft.Text = ft.Text("SUAS TAREFAS", size=20, weight="w800")
        self.toggle: ft.IconButton = ft.IconButton(**toggle_style_sheet, on_click=lambda e: self.switch(e))

        self.item: ft.TextField = ft.TextField(**item_style_sheet)
        self.add: ft.IconButton = ft.IconButton(**add_style_sheet, on_click=self.add_board)

        self.bd, self.cursor = BancoDeDados.conectarAoBanco()
        self.usuario_logado = None

        self.area_tarefas: ft.DragTarget = ft.DragTarget(
            content=ft.Column(spacing=18, height=680, scroll="Auto", controls=[ft.Container()]),
            group="tarefa"
        )
        self.counter: ft.Text = ft.Text("0 itens", italic=True)
        self.area_concluida: ft.DragTarget = ft.DragTarget(
            content=ft.Column(spacing=18, height=680, scroll="Auto", controls=[ft.Container()]),
            group="tarefa"
        )

    def tela_tarefa(self):
        self.main: ft.Container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        alignment="start",
                        controls=[
                            self.title, 
                            ft.Container(
                                expand=True
                            ),
                            self.add, 
                            self.toggle
                        ],
                    ),
                    ft.Divider(height=20),
                    ft.ResponsiveRow(
                        alignment="spaceBetween",
                        columns=100,
                        controls=[
                            ft.Column(
                                col={
                                    "xs": 51
                                },
                                controls=[
                                    ft.Container(
                                        content=ft.Column(
                                            scroll=ft.ScrollMode.AUTO,
                                            controls=[
                                                ft.Row(
                                                    alignment="spaceBetween",
                                                    col=2,
                                                    controls=[
                                                        ft.Text('Lista de Tarefas'),
                                                        self.counter
                                                    ]
                                                ),
                                                self.area_tarefas
                                            ],
                                        ),
                                        bgcolor=ft.colors.with_opacity(0.5,"grey50"),
                                        border_radius=5,
                                        border=ft.border.all(1,"grey50"),
                                        padding=10,
                                    )
                                ],
                            ),
                            ft.Column(
                                col={
                                    "xs": 49
                                },
                                controls=[
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Row(
                                                    controls=[
                                                        ft.Text("Tarefas Concluídas"),
                                                        ft.Container(
                                                            expand=True
                                                        )
                                                    ]
                                                ),
                                                self.area_concluida
                                            ],
                                        ),
                                        bgcolor=ft.colors.with_opacity(0.5,"grey50"),
                                        border_radius=5,
                                        border=ft.border.all(1,"grey50"),
                                        padding=10,
                                    )
                                ],
                            ),
                        ],
                        height=500
                    )
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
            padding=ft.padding.all(20),
        )

        self.page.theme = ft.Theme(
                appbar_theme=ft.AppBarTheme(
                    bgcolor=ft.colors.YELLOW,
                    color=ft.colors.BLACK87,
                )
            )

        return self.main

    def item_size(self) -> None:
        if len(self.area_tarefas.content.controls[:]) == 2:
            self.counter.value = f"{len(self.area_tarefas.content.controls[:]) - 1} item"
        else:
            self.counter.value = f"{len(self.area_tarefas.content.controls[:]) - 1} itens"

        self.counter.update()

    def add_item(self, dialog_text: str) -> None:
        if dialog_text != "":
            if self.page.theme_mode == ft.ThemeMode.DARK:
                self.area_tarefas.content.controls.append(Tarefa(self, dialog_text, "dark", self.usuario_logado))
            else:
                self.area_tarefas.content.controls.append(Tarefa(self, dialog_text, "light", self.usuario_logado))

            self.area_tarefas.update()
            self.item_size()

        else:
            pass

    def switch(self, e) -> None:
        if self.page.theme_mode == ft.ThemeMode.DARK:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.toggle.icon = ft.icons.DARK_MODE_ROUNDED
            self.toggle.icon_color = ft.colors.BLACK87
            self.add.icon_color = ft.colors.BLACK87
            self.item.border_color = _light

            self.page.theme=ft.Theme(
                appbar_theme=ft.AppBarTheme(
                    color=ft.colors.BLACK87,
                    bgcolor=ft.colors.YELLOW
                ),
                dialog_theme=ft.DialogTheme(
                    content_text_style=ft.TextStyle(color=ft.colors.WHITE)
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

            for item in self.area_tarefas.content.controls[:]:
                item.border = ft.border.all(1, _light)

        else:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.toggle.icon = ft.icons.LIGHT_MODE_ROUNDED
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

            for item in self.area_tarefas.content.controls[:]:
                item.border = ft.border.all(1, _dark)

        self.page.update()

    def add_board(self, e) -> None:
        def close_dlg(e):
            self.add_item(dialog_text.value)
            dialog.open = False
            self.page.update()

        def cancel_dlg(e):
            dialog.open = False
            self.page.update()

        def textfield_change(e):
            if dialog_text.value == "":
                create_button.disabled = True
            else:
                create_button.disabled = False
            self.page.update()

        dialog_text = TextField(
            label="Nome da nova tarefa",
            border_color=ft.colors.BLACK87 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
            label_style=ft.TextStyle(
                color=ft.colors.BLACK54 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
                weight=ft.FontWeight.BOLD,
                font_family='Arial Rounded MT Bold',
                size=14
            ),
            cursor_height=15,
            cursor_width=1,
            cursor_color=ft.colors.BLACK87 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
            color=ft.colors.BLACK87 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
            border_width=2,
            on_submit=close_dlg,
            on_change=textfield_change
        )
        create_button = ft.ElevatedButton(
            text="Criar",
            style=ft.ButtonStyle(
                color={
                    ft.MaterialState.DEFAULT: ft.colors.BLACK87,
                    ft.MaterialState.HOVERED: ft.colors.WHITE
                },
                bgcolor={
                    ft.MaterialState.DEFAULT: ft.colors.WHITE,
                    ft.MaterialState.HOVERED: ft.colors.BLACK87,
                    ft.MaterialState.DISABLED: ft.colors.GREY
                },
                shape=ft.RoundedRectangleBorder(radius=5)
            ),
            on_click=close_dlg,
            disabled=True
        )
        dialog = AlertDialog(
            title=ft.Text("Criar nova tarefa"),
            bgcolor= ft.colors.with_opacity(0.6,ft.colors.GREY_100),
            content=ft.Column(
                controls=[
                    dialog_text,
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Cancelar",
                                style=ft.ButtonStyle(
                                    color={
                                        ft.MaterialState.DEFAULT: ft.colors.WHITE,
                                        ft.MaterialState.HOVERED: ft.colors.BLACK87
                                    },
                                    bgcolor={
                                        ft.MaterialState.DEFAULT: ft.colors.BLACK87,
                                        ft.MaterialState.HOVERED: ft.colors.WHITE
                                    },
                                    shape=ft.RoundedRectangleBorder(radius=5)
                                ),
                                on_click=cancel_dlg,
                            ),
                            create_button,
                        ],
                        alignment="spaceBetween",
                    ),
                ],
                tight=True,
            )
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        dialog_text.focus()

    def open_edit_dialog(self, tarefa: Tarefa) -> None:
        def close_dlg(e):
            tarefa.update_text(dialog_text.value)
            dialog.open = False
            self.page.update()
            self.area_tarefas.content.update()

        def cancel_dlg(e):
            dialog.open = False
            self.page.update()

        def textfield_change(e):
            if dialog_text.value == "":
                update_button.disabled = True
            else:
                update_button.disabled = False
            self.page.update()

        dialog_text = TextField(
            label="Editar nome da tarefa",
            value=tarefa.description,
            border_color=ft.colors.BLACK87 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
            label_style=ft.TextStyle(
                color=ft.colors.BLACK54 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
                weight=ft.FontWeight.BOLD,
                font_family='Arial Rounded MT Bold',
                size=14
            ),
            cursor_height=15,
            cursor_width=1,
            cursor_color=ft.colors.BLACK87 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
            color=ft.colors.BLACK87 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
            border_width=2,
            on_submit=close_dlg,
            on_change=textfield_change
        )

        update_button = ft.ElevatedButton(
            text="Atualizar",
            style=ft.ButtonStyle(
                color={ft.MaterialState.DEFAULT: ft.colors.BLACK87, ft.MaterialState.HOVERED: ft.colors.WHITE},
                bgcolor={ft.MaterialState.DEFAULT: ft.colors.WHITE, ft.MaterialState.HOVERED: ft.colors.BLACK87,
                        ft.MaterialState.DISABLED: ft.colors.GREY},
                shape=ft.RoundedRectangleBorder(radius=5)
            ),
            on_click=close_dlg,
            disabled=True
        )

        dialog = AlertDialog(
            title=ft.Text("Editar tarefa"),
            bgcolor=ft.colors.with_opacity(0.7, ft.colors.GREY_100),
            content=ft.Column(
                controls=[
                    dialog_text,
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Cancelar",
                                style=ft.ButtonStyle(
                                    color={ft.MaterialState.DEFAULT: ft.colors.WHITE, ft.MaterialState.HOVERED: ft.colors.BLACK87},
                                    bgcolor={ft.MaterialState.DEFAULT: ft.colors.BLACK87, ft.MaterialState.HOVERED: ft.colors.WHITE},
                                    shape=ft.RoundedRectangleBorder(radius=5)
                                ),
                                on_click=cancel_dlg,
                            ),
                            update_button,
                        ],
                        alignment="spaceBetween",
                    ),
                ],
                tight=True,
            )
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        dialog_text.focus()
