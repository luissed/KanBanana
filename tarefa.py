from flet import *
import flet as ft
from styles import _dark, _light, tarefa_style_sheet
from banco_de_dados import BancoDeDados

class Tarefa(ft.Container):
    def __init__(self, tela_tarefa: object, descricao: str, theme: str, usuario_id:int, tarefa_id:int = None) -> None:
        
        if theme == "dark":
            tarefa_style_sheet["border"] = ft.border.all(1, _dark)
        else:
            tarefa_style_sheet["border"] = ft.border.all(1, _light)
        
        super().__init__(**tarefa_style_sheet)
        self.tela_tarefa: object = tela_tarefa
        self.descricao = descricao
        self.usuario_id = usuario_id
        self.tarefa_id = tarefa_id

        self.tick = ft.Checkbox(on_change=lambda e: self.strike(e))
        self.text = ft.Text(
            spans=[ft.TextSpan(text=self.descricao)],
            size=14,
            expand=True,
        )
        self.delete = ft.IconButton(
            icon = ft.icons.DELETE_ROUNDED,
            icon_color = "red700",
            on_click = lambda e: self.delete_text(e),
        )
        self.previous = ft.IconButton(
            icon = ft.icons.NAVIGATE_BEFORE_ROUNDED,
            icon_color = "black",
            on_click = lambda e: self.previous_step(e),
        )
        self.next = ft.IconButton(
            icon = ft.icons.NAVIGATE_NEXT_ROUNDED,
            icon_color = "black",
            on_click = lambda e: self.next_step(e),
        )

        self.content = ft.Row(
            alignment="start",
            controls=[
                self.tick,
                self.text,
                self.previous,
                self.next,
                self.delete,
            ],
        )
        
    def next_step(self, e) -> None:
        if self in self.tela_tarefa.area_tarefas.controls:
            self.tela_tarefa.area_tarefas.controls.remove(self)
            self.tela_tarefa.area_tarefas.update()
            self.tela_tarefa.area_andamento.controls.append(self)
            self.tela_tarefa.area_andamento.update()
            self.tela_tarefa.item_size()

        elif self in self.tela_tarefa.area_andamento.controls:
            self.tick.value = True
            self.text.spans[0].style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH, decoration_thickness=2
            )
            self.tela_tarefa.area_andamento.controls.remove(self)
            self.tela_tarefa.area_concluida.controls.append(self)
            self.tela_tarefa.area_andamento.update()
            self.tela_tarefa.area_concluida.update()
            self.tela_tarefa.item_size()

    def previous_step(self, e) -> None:
        if self in self.tela_tarefa.area_andamento.controls:
            self.tela_tarefa.area_andamento.controls.remove(self)
            self.tela_tarefa.area_andamento.update()
            self.tela_tarefa.area_tarefas.controls.append(self)
            self.tela_tarefa.area_tarefas.update()
            self.tela_tarefa.item_size()
        
        elif self in self.tela_tarefa.area_concluida.controls:
            self.tick.value = False
            self.text.spans[0].style = ft.TextStyle()
            self.tela_tarefa.area_concluida.controls.remove(self)
            self.tela_tarefa.area_andamento.controls.append(self)
            self.tela_tarefa.area_concluida.update()
            self.tela_tarefa.area_andamento.update()
            self.tela_tarefa.item_size()

    def strike(self, e) -> None:
        concluida = e.control.value
        if concluida == True:
            if self in self.tela_tarefa.area_andamento.controls:
                self.text.spans[0].style = ft.TextStyle(
                    decoration=ft.TextDecoration.LINE_THROUGH, decoration_thickness=2
                )
                self.tela_tarefa.area_andamento.controls.remove(self)
                self.tela_tarefa.area_concluida.controls.append(self)
                self.tela_tarefa.area_andamento.update()
                self.tela_tarefa.area_concluida.update()
                self.tela_tarefa.item_size()
            elif self in self.tela_tarefa.area_tarefas.controls:
                self.text.spans[0].style = ft.TextStyle(
                    decoration=ft.TextDecoration.LINE_THROUGH, decoration_thickness=2
                )
                self.tela_tarefa.area_tarefas.controls.remove(self)
                self.tela_tarefa.area_concluida.controls.append(self)
                self.tela_tarefa.area_tarefas.update()
                self.tela_tarefa.area_concluida.update()
                self.tela_tarefa.item_size()
        else:
            self.text.spans[0].style = ft.TextStyle()
            self.tela_tarefa.area_concluida.controls.remove(self)
            self.tela_tarefa.area_tarefas.controls.append(self)
            self.tela_tarefa.area_concluida.update()
            self.tela_tarefa.area_tarefas.update()
            self.tela_tarefa.item_size()
        BancoDeDados.atualizar_tarefa(self.tela_tarefa.bd,self.tarefa_id,self.descricao, concluida)
        self.text.update()

    def delete_text(self, e) -> None:
        BancoDeDados.remover_tarefa(self.tela_tarefa.bd, self.tarefa_id)
        if self in self.tela_tarefa.area_tarefas.controls:
            self.tela_tarefa.area_tarefas.controls.remove(self)
            self.tela_tarefa.area_tarefas.update()
            self.tela_tarefa.item_size()
        elif self in self.tela_tarefa.area_andamento.controls:
            self.tela_tarefa.area_andamento.controls.remove(self)
            self.tela_tarefa.area_andamento.update()
            self.tela_tarefa.item_size()
        else:
            self.tela_tarefa.area_concluida.controls.remove(self)
            self.tela_tarefa.area_concluida.update()
        