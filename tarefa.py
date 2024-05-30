from flet import *
import flet as ft
from styles import _dark, _light, tarefa_style_sheet

class Tarefa(ft.Draggable):
    def __init__(self, tela_tarefa: object, description: str, theme: str) -> None:
        
        if theme == "dark":
            tarefa_style_sheet["border"] = ft.border.all(1, _dark)
        else:
            tarefa_style_sheet["border"] = ft.border.all(1, _light)
        
        super().__init__(group="tarefa")
        self.tela_tarefa: object = tela_tarefa
        self.description = description

        self.tick = ft.Checkbox(on_change=lambda e: self.strike(e))
        self.text: ft.Text = ft.Text(spans=[ft.TextSpan(text=self.description)], size=14)
        self.delete: ft.IconButton = ft.IconButton(
            icon=ft.icons.DELETE_ROUNDED,
            icon_color="red700",
            on_click=lambda e: self.delete_text(e),
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
                        self.delete,
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
                        self.delete,
                    ],
                )
            ),
            **tarefa_style_sheet,
            bgcolor=ft.colors.with_opacity(0.5,"white")
        )
        self.on_drag_complete = self.drag_complete
        

    def strike(self, e) -> None:
        if e.control.value == True:
            self.text.spans[0].style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH, decoration_thickness=2
            )
            self.tela_tarefa.area_tarefas.content.controls.remove(self)
            self.tela_tarefa.area_concluida.content.controls.append(self)
            self.tela_tarefa.area_tarefas.update()
            self.tela_tarefa.area_concluida.update()
            self.tela_tarefa.item_size()
        else:
            self.text.spans[0].style = ft.TextStyle()
            self.tela_tarefa.area_concluida.content.controls.remove(self)
            self.tela_tarefa.area_tarefas.content.controls.append(self)
            self.tela_tarefa.area_concluida.update()
            self.tela_tarefa.area_tarefas.update()
            self.tela_tarefa.item_size()

        self.text.update()

    def delete_text(self, e) -> None:
        if self in self.tela_tarefa.area_tarefas.content.controls:
            self.tela_tarefa.area_tarefas.content.controls.remove(self)
            self.tela_tarefa.area_tarefas.update()
            self.tela_tarefa.item_size()
        else:
            self.tela_tarefa.area_concluida.content.controls.remove(self)
            self.tela_tarefa.area_concluida.update()
        
    def drag_complete(self, e):
        if e.control.content.content.controls[0].controls[0].value == False:
            self.text.spans[0].style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH, decoration_thickness=2
            )
            e.control.content.content.controls[0].controls[0].value = True
            self.tela_tarefa.area_tarefas.content.controls.remove(self)
            self.tela_tarefa.area_concluida.content.controls.append(self)
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