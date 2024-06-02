from flet import *
import flet as ft
from styles import _dark, _light, tarefa_style_sheet
from banco_de_dados import BancoDeDados

class Tarefa(ft.Draggable):
    def __init__(self, tela_tarefa: object, description: str, theme: str, usuario: str, tarefa_id: int = None) -> None:
        if theme == "dark":
            tarefa_style_sheet["border"] = ft.border.all(1, _dark)
        else:
            tarefa_style_sheet["border"] = ft.border.all(1, _light)
        
        super().__init__(group="tarefa")
        self.tela_tarefa: object = tela_tarefa
        self.description = description
        self.usuario = usuario
        self.tarefa_id = tarefa_id

        if self.tarefa_id is None:
            self.tarefa_id = self.criar_tarefa(description)

        self.tick = ft.Checkbox(on_change=lambda e: self.strike(e))
        self.text: ft.Text = ft.Text(spans=[ft.TextSpan(text=self.description)], size=14)
        self.delete: ft.IconButton = ft.IconButton(
            icon=ft.icons.DELETE_ROUNDED,
            icon_color="red700",
            on_click=lambda e: self.delete_text(e),
        )
        self.edit: ft.IconButton = ft.IconButton(
            icon=ft.icons.EDIT_ROUNDED,
            icon_color="blue700",
            on_click=lambda e: self.edit_text(e),
        )

        self.content: ft.Container = ft.Container(
            content=(
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Row(
                            controls=[
                                self.tick,
                                self.text
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.edit,
                                self.delete,
                            ]
                        )
                    ],
                )
            ),
            **tarefa_style_sheet,
            expand=True
        )

        self.content_feedback: ft.Container = ft.Container(
            content=(
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Row(
                            controls=[
                                self.tick,
                                self.text
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.edit,
                                self.delete,
                            ]
                        )
                    ],
                )
            ),
            **tarefa_style_sheet,
            bgcolor=ft.colors.with_opacity(0.5,"white")
        )
        self.on_drag_complete = self.drag_complete

    def criar_tarefa(self, descricao: str) -> int:
        BancoDeDados.adicionarTarefa(self.tela_tarefa.bd, self.usuario, descricao)
        query = "SELECT last_insert_rowid()"
        c = self.tela_tarefa.bd.cursor()
        c.execute(query)
        tarefa_id = c.fetchone()[0]
        return tarefa_id

    def strike(self, e) -> None:
        concluida = e.control.value
        if concluida:
            self.text.spans[0].style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH, decoration_thickness=2
            )
            self.tela_tarefa.area_tarefas.content.controls.remove(self)
            self.tela_tarefa.area_concluida.content.controls.append(self)
        else:
            self.text.spans[0].style = ft.TextStyle()
            self.tela_tarefa.area_concluida.content.controls.remove(self)
            self.tela_tarefa.area_tarefas.content.controls.append(self)

        BancoDeDados.atualizarTarefa(self.tela_tarefa.bd, self.tarefa_id, self.description, concluida)
        self.tela_tarefa.area_tarefas.update()
        self.tela_tarefa.area_concluida.update()
        self.tela_tarefa.item_size()
        self.text.update()

    def delete_text(self, e) -> None:
        BancoDeDados.removerTarefa(self.tela_tarefa.bd, self.tarefa_id)
        if self in self.tela_tarefa.area_tarefas.content.controls:
            self.tela_tarefa.area_tarefas.content.controls.remove(self)
            self.tela_tarefa.area_tarefas.update()
        else:
            self.tela_tarefa.area_concluida.content.controls.remove(self)
            self.tela_tarefa.area_concluida.update()
        self.tela_tarefa.item_size()

    def edit_text(self, e) -> None:
        self.tela_tarefa.open_edit_dialog(self)

    def update_text(self, new_description: str) -> None:
        self.description = new_description
        self.text.spans[0].text = new_description
        BancoDeDados.atualizarTarefa(self.tela_tarefa.bd, self.tarefa_id, self.description, self.tick.value)
        self.text.update()

    def drag_complete(self, e):
        concluida = e.control.content.content.controls[0].controls[0].value
        if concluida == False:
            self.text.spans[0].style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH, decoration_thickness=2
            )
            e.control.content.content.controls[0].controls[0].value = True
            self.tela_tarefa.area_tarefas.content.controls.remove(self)
            self.tela_tarefa.area_concluida.content.controls.append(self)
            BancoDeDados.atualizarTarefa(self.tela_tarefa.bd, self.tarefa_id, self.description, concluida)
            self.tela_tarefa.area_tarefas.update()
            self.tela_tarefa.area_concluida.update()
            self.tela_tarefa.item_size()
        else:
            self.text.spans[0].style = ft.TextStyle()
            e.control.content.content.controls[0].controls[0].value = False
            self.tela_tarefa.area_concluida.content.controls.remove(self)
            self.tela_tarefa.area_tarefas.content.controls.append(self)
            self.tela_tarefa.area_concluida.update()
            self.tela_tarefa.area_tarefas.update()
            self.tela_tarefa.item_size()

        self.text.update()
