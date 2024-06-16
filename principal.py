from flet import *
import flet as ft
from styles import _dark, _light, toggle_style_sheet, add_style_sheet, item_style_sheet
from tarefa import Tarefa
from banco_de_dados import BancoDeDados

class Principal(ft.SafeArea):
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.title = ft.Text("MINHAS TAREFAS", size=20, weight="w800")
        self.toggle = ft.IconButton(**toggle_style_sheet, on_click=lambda e: self.switch(e))

        self.item = ft.TextField(**item_style_sheet)
        self.add = ft.IconButton(**add_style_sheet, on_click=self.add_board)

        self.bd, self.cursor = BancoDeDados._conectar_ao_banco()
        self.usuario_logado = None

        self.area_tarefas = ft.Column(spacing=18, expand=True, scroll="Auto")
        self.counter = ft.Text("0 itens", italic=True)

        self.area_atrasada = ft.Column(spacing=18, expand=True, scroll="Auto")
        self.counter_atrasada = ft.Text("0 itens", italic=True)

        self.area_andamento = ft.Column(spacing=18, expand=True, scroll="Auto")
        self.counter_andamento = ft.Text("0 itens", italic=True)

        self.area_concluida = ft.Column(spacing=18, expand=True, scroll="Auto")

    def tela_tarefa(self):
        self.main = ft.Container(
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
                        columns=80,
                        controls=[
                            ft.Container(
                                col={"xs": 20},
                                content=ft.Column(
                                    controls=[
                                        ft.Row(
                                            alignment="spaceBetween",
                                            col=2,
                                            controls=[
                                                ft.Text('A fazer'),
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
                            ),
                            ft.Container(
                                col={"xs": 20},
                                content=ft.Column(
                                    controls=[
                                        ft.Row(
                                            alignment="spaceBetween",
                                            col=2,
                                            controls=[
                                                ft.Text('Atrasada'),
                                                self.counter_atrasada
                                            ]
                                        ),
                                        self.area_atrasada
                                    ],
                                ),
                                bgcolor=ft.colors.with_opacity(0.5,"grey50"),
                                border_radius=5,
                                border=ft.border.all(1,"grey50"),
                                padding=10,
                            ),
                            ft.Container(
                                col={"xs": 20},
                                content=ft.Column(
                                    controls=[
                                        ft.Row(
                                            alignment="spaceBetween",
                                            col=2,
                                            controls=[
                                                ft.Text('Em andamento'),
                                                self.counter_andamento
                                            ]
                                        ),
                                        self.area_andamento
                                    ],
                                ),
                                bgcolor=ft.colors.with_opacity(0.5,"grey50"),
                                border_radius=5,
                                border=ft.border.all(1,"grey50"),
                                padding=10,
                            ),
                            ft.Container(
                                col={"xs": 20},
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Tarefas Concluídas"),
                                        self.area_concluida
                                    ],
                                ),
                                bgcolor=ft.colors.with_opacity(0.5,"grey50"),
                                border_radius=5,
                                border=ft.border.all(1,"grey50"),
                                padding=10,
                            ),
                        ],
                        expand=True
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
    
    def carregar_tarefas(self) -> None:
        """
        Se o usuário estiver logado, esta função obtém todas as tarefas daquele usuário no banco
        de dados, limpa as áreas de tarefas na interface e adiciona as tarefas nas áreas 
        correspondentes (concluída, em andamento, atrasada, e pendente).

        """
        if self.usuario_logado is not None:
            print(f"ID do usuario logado: {self.usuario_logado}")
            # Obtem do banco de dados todas as tarefas do usuário logado
            tarefas = BancoDeDados.obter_tarefas(self.bd, self.usuario_logado)

            # Limpa todas as áreas da tela principal
            self.area_tarefas.controls.clear()
            self.area_concluida.controls.clear()
            self.area_andamento.controls.clear()
            self.area_atrasada.controls.clear()

            # Adiciona as tarefas recuperadas do banco de dados nas áreas correspondentes
            for tarefa in tarefas:
                tarefa_id, descricao, concluida, em_andamento, atrasada = tarefa
                theme = "dark" if self.page.theme_mode == ft.ThemeMode.DARK else "light"
                obj_tarefa = Tarefa(self, descricao, theme, self.usuario_logado, tarefa_id)

                if concluida:
                    obj_tarefa.tick.value = True
                    obj_tarefa.text.spans[0].style = ft.TextStyle(
                        decoration=ft.TextDecoration.LINE_THROUGH,
                        decoration_thickness=2
                    )
                    self.area_concluida.controls.append(obj_tarefa)
                elif em_andamento:
                    self.area_andamento.controls.append(obj_tarefa)
                elif atrasada:
                    self.area_atrasada.controls.append(obj_tarefa)
                else:
                    self.area_tarefas.controls.append(obj_tarefa)

            # Atualiza todas as áreas de tarefas
            self.area_tarefas.update()
            self.area_atrasada.update()
            self.area_andamento.update()
            self.area_concluida.update()
            self.item_size()


    def item_size(self) -> None:
        if len(self.area_tarefas.controls[:]) == 1:
            self.counter.value = f"{len(self.area_tarefas.controls[:])} item"
        else:
            self.counter.value = f"{len(self.area_tarefas.controls[:])} itens"

        self.counter.update()

        if len(self.area_atrasada.controls[:]) == 1:
            self.counter_atrasada.value = f"{len(self.area_atrasada.controls[:])} item"
        else:
            self.counter_atrasada.value = f"{len(self.area_atrasada.controls[:])} itens"

        self.counter_atrasada.update()

        if len(self.area_andamento.controls[:]) == 1:
            self.counter_andamento.value = f"{len(self.area_andamento.controls[:])} item"
        else:
            self.counter_andamento.value = f"{len(self.area_andamento.controls[:])} itens"

        self.counter_andamento.update()

    def add_item(self, dialog_text: str) -> None:
        if dialog_text != "":
            BancoDeDados.adicionar_tarefa(self.bd,self.usuario_logado, dialog_text)
            tarefas = BancoDeDados.obter_tarefas(self.bd, self.usuario_logado)
            if tarefas:
                tarefa_id = tarefas[-1][0] 
            else: None

            if self.page.theme_mode == ft.ThemeMode.DARK:
                self.area_tarefas.controls.append(Tarefa(self, dialog_text, "dark", self.usuario_logado, tarefa_id))
            else:
                self.area_tarefas.controls.append(Tarefa(self, dialog_text, "light", self.usuario_logado, tarefa_id))

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

            for item in self.area_tarefas.controls[:]:
                item.border = ft.border.all(1, _light)
                item.content.controls[2].icon_color = "black"
                item.content.controls[3].icon_color = "black"
            
            for item in self.area_atrasada.controls[:]:
                item.border = ft.border.all(1, _light)
                item.content.controls[2].icon_color = "black"
                item.content.controls[3].icon_color = "black"
            
            for item in self.area_andamento.controls[:]:
                item.border = ft.border.all(1, _light)
                item.content.controls[2].icon_color = "black"
                item.content.controls[3].icon_color = "black"
            
            for item in self.area_concluida.controls[:]:
                item.border = ft.border.all(1, _light)
                item.content.controls[2].icon_color = "black"
                item.content.controls[3].icon_color = "black"

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

            for item in self.area_tarefas.controls[:]:
                item.border = ft.border.all(1, _dark)
                item.content.controls[2].icon_color = "white"
                item.content.controls[3].icon_color = "white"
            
            for item in self.area_atrasada.controls[:]:
                item.border = ft.border.all(1, _dark)
                item.content.controls[2].icon_color = "white"
                item.content.controls[3].icon_color = "white"
            
            for item in self.area_andamento.controls[:]:
                item.border = ft.border.all(1, _dark)
                item.content.controls[2].icon_color = "white"
                item.content.controls[3].icon_color = "white"
            
            for item in self.area_concluida.controls[:]:
                item.border = ft.border.all(1, _dark)
                item.content.controls[2].icon_color = "white"
                item.content.controls[3].icon_color = "white"

        self.page.update()

    def add_board(self, e) -> None:
        def close_dlg(e):
            self.add_item(dialog_text.value)
            dialog.open = False
            self.page.update()
        
        def cancel_task(e):
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
                color=ft.colors.BLACK87 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLACK54,
                weight=ft.FontWeight.BOLD,
                font_family='Arial Rounded MT Bold',
                size=14
            ),
            cursor_height=15,
            cursor_width=1,
            cursor_color=ft.colors.BLACK87 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
            color=ft.colors.BLACK87 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLACK54,
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
            title_text_style=ft.TextStyle(
                color=ft.colors.BLACK87 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLACK54,
                weight=ft.FontWeight.BOLD,
                font_family='Arial Rounded MT ',
                size=18,
            ),

            bgcolor= ft.colors.with_opacity(0.8,ft.colors.GREY_100),
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
                                on_click=cancel_task,
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
    
    # Retorna o banco de dados 
    def get_bd(self):
        return self.bd
