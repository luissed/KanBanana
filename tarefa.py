from flet import *
import flet as ft
from styles import _dark, _light, tarefa_style_sheet

class Tarefa(ft.Container):
    def __init__(self, tela_tarefa: object, description: str, theme: str) -> None:
        
        if theme == "dark":
            tarefa_style_sheet["border"] = ft.border.all(1, _dark)
        else:
            tarefa_style_sheet["border"] = ft.border.all(1, _light)
        
        super().__init__(**tarefa_style_sheet)
        self.tela_tarefa: object = tela_tarefa
        self.description = description

        self.tick = ft.Checkbox(on_change=lambda e: self.strike(e))
        self.text: ft.Text = ft.Text(spans=[ft.TextSpan(text=self.description)], size=14)
        self.delete: ft.IconButton = ft.IconButton(
            icon=ft.icons.DELETE_ROUNDED,
            icon_color="red700",
            on_click=lambda e: self.delete_text(e),
        )

        self.content: ft.Row = ft.Row(
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

    def strike(self, e) -> None:
        if e.control.value == True:
            self.text.spans[0].style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH, decoration_thickness=2
            )
        else:
            self.text.spans[0].style = ft.TextStyle()

        self.text.update()

    def delete_text(self, e) -> None:
        self.tela_tarefa.area_tarefas.controls.remove(self)
        self.tela_tarefa.area_tarefas.update()
        self.tela_tarefa.item_size()