from flet import *
import flet as ft
from styles import _dark, _light, tarefa_style_sheet
from banco_de_dados import BancoDeDados
from datetime import date
import locale

#Define o padrão Brasileiro para hora.
try:
    locale.setlocale(locale.LC_TIME, "pt_BR.utf8")
except locale.Error:
    # Tente outra configuração se "pt_BR.utf8" não estiver disponível
    locale.setlocale(locale.LC_TIME, "pt_BR")

"""
-------------------------------------------------- Classe Tarefa --------------------------------------------------
Entradas: tela_tarefa, descricao, theme, usuario_id, data, tarefa_id
Saídas: -
Descrição: Recebe como parâmetros o objeto da classe Principal, a descrição da tarefa, o tema da página no momento,
           o ID do usuário, a data da tarefa e o ID da tarefa. Com esses atributos, a classe cria uma tarefa com a
           descrição, data e tema recebidos, e define a que usuário essa tarefa pertence juntamente com o ID da tarefa.
--------------------------------------------------------------------------------------------------------------------
"""
class Tarefa(ft.Container):
    def __init__(self, tela_tarefa: object, descricao: str, theme: str, usuario_id:int, data: date, tarefa_id: int = None) -> None:
        
        if theme == "dark":
            tarefa_style_sheet["border"] = ft.border.all(1, _dark)
        else:
            tarefa_style_sheet["border"] = ft.border.all(1, _light)
        
        super().__init__(**tarefa_style_sheet)
        self.tela_tarefa = tela_tarefa
        self.descricao = descricao
        self.usuario_id = usuario_id
        self.tarefa_id = tarefa_id
        self.data = data

        #Atributos Flet
        self.tick = ft.Checkbox(on_change = lambda e: self.strike(e))
        self.text = ft.Text(
            spans=[ft.TextSpan(text = self.descricao)],
            size=14,
            expand=True,
        )

        self.previous = ft.IconButton(
            icon = ft.icons.NAVIGATE_BEFORE_ROUNDED,
            icon_color = "black" if theme == "light" else "white",
            on_click = lambda e: self.previous_step(e),
        )

        self.next = ft.IconButton(
            icon = ft.icons.NAVIGATE_NEXT_ROUNDED,
            icon_color = "black" if theme == "light" else "white",
            on_click = lambda e: self.next_step(e),
        )

        self.delete = ft.IconButton(
            icon = ft.icons.DELETE_ROUNDED,
            icon_color = "red700",
            on_click = lambda e: self.delete_text(e),
        )

        self.data_text = ft.Text(
            spans = [ft.TextSpan(text = self.data.strftime("%a, %d de %b"))],
            size = 14,
            expand = True,
            text_align = ft.TextAlign.CENTER
        )

        self.content = ft.Column(
                controls = [
                    ft.Row(
                        alignment = "start",
                        controls = [
                            self.tick,
                            self.text,
                            self.previous,
                            self.next,
                            self.delete,
                        ],
                    ),
                    ft.Row(
                        controls = [
                            ft.Icon(
                                name = ft.icons.CALENDAR_MONTH_OUTLINED,
                                size = 16,
                                color = "black" if theme == "light" else "white"
                            ),
                            ft.Text("Concluir "),
                            ft.Container(
                                content = self.data_text,
                                padding = ft.Padding(
                                    left = -2,
                                    top = 0,
                                    right = 0,
                                    bottom = 0
                                )
                            ),
                        ],
                    ),
                ],
            )
    
    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método next_step
    Entradas: e (não utilizado, mas obrigatório no Flet)
    Saídas: -
    Descrição: Avança a tarefa entre os campos "A fazer", "Em andamento" e "Tarefas Concluídas".
    --------------------------------------------------------------------------------------------------------------------
    """
    def next_step(self, e) -> None:
        if self in self.tela_tarefa.area_tarefas.controls:
            self.tela_tarefa.area_tarefas.controls.remove(self)
            self.tela_tarefa.area_tarefas.update()
            self.tela_tarefa.area_andamento.controls.append(self)
            self.tela_tarefa.area_andamento.update()
            self.tela_tarefa.item_size()
            BancoDeDados.atualizar_tarefa(self.tela_tarefa.bd, self.tarefa_id, self.descricao, self.data, False, True, False)

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
            BancoDeDados.atualizar_tarefa(self.tela_tarefa.bd, self.tarefa_id, self.descricao, self.data, True, False, False)

    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método previous_step
    Entradas: e (não utilizado, mas obrigatório no Flet)
    Saídas: -
    Descrição: Recua a tarefa entre os campos "A fazer", "Em andamento" e "Tarefas Concluídas".
    --------------------------------------------------------------------------------------------------------------------
    """
    def previous_step(self, e) -> None:
        if self in self.tela_tarefa.area_andamento.controls:
            self.tela_tarefa.area_andamento.controls.remove(self)
            self.tela_tarefa.area_andamento.update()
            self.tela_tarefa.area_tarefas.controls.append(self)
            self.tela_tarefa.area_tarefas.update()
            self.tela_tarefa.item_size()
            BancoDeDados.atualizar_tarefa(self.tela_tarefa.bd, self.tarefa_id, self.descricao, self.data, False, False, False)
        
        elif self in self.tela_tarefa.area_concluida.controls:
            self.tick.value = False
            self.text.spans[0].style = ft.TextStyle()
            if self.data < date.today():
                self.tela_tarefa.area_concluida.controls.remove(self)
                self.tela_tarefa.area_atrasada.controls.append(self)
                self.tela_tarefa.area_concluida.update()
                self.tela_tarefa.area_atrasada.update()
                self.tela_tarefa.item_size()
                BancoDeDados.atualizar_tarefa(self.tela_tarefa.bd, self.tarefa_id, self.descricao, self.data, False, False, True)
            else:
                self.tela_tarefa.area_concluida.controls.remove(self)
                self.tela_tarefa.area_andamento.controls.append(self)
                self.tela_tarefa.area_concluida.update()
                self.tela_tarefa.area_andamento.update()
                self.tela_tarefa.item_size()
                BancoDeDados.atualizar_tarefa(self.tela_tarefa.bd, self.tarefa_id, self.descricao, self.data, False, True, False)
    
    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método strike
    Entradas: e (evento)
    Saídas: -
    Descrição: Recebe como parâmetro 'e', que contém informações sobre o evento. Se a caixa de seleção estiver marcada,
            o método avança a tarefa para o campo "Tarefas Concluídas" e risca a descrição da tarefa. Se a tarefa for atrasada,
            a cor da data não é alterada para sinalizar que a tarefa foi concluída com atraso.
    --------------------------------------------------------------------------------------------------------------------
    """
    def strike(self, e) -> None:
        concluida = e.control.value
        if concluida == True:
            if self in self.tela_tarefa.area_andamento.controls:
                self.text.spans[0].style = ft.TextStyle(
                    decoration = ft.TextDecoration.LINE_THROUGH,
                    decoration_thickness = 2
                )
                self.tela_tarefa.area_andamento.controls.remove(self)
                self.tela_tarefa.area_concluida.controls.append(self)
                self.tela_tarefa.area_andamento.update()
                self.tela_tarefa.area_concluida.update()
                self.tela_tarefa.item_size()
                BancoDeDados.atualizar_tarefa(self.tela_tarefa.bd, self.tarefa_id, self.descricao, self.data, True, False, False)
            elif self in self.tela_tarefa.area_tarefas.controls:
                self.text.spans[0].style = ft.TextStyle(
                    decoration = ft.TextDecoration.LINE_THROUGH,
                    decoration_thickness = 2
                )
                self.tela_tarefa.area_tarefas.controls.remove(self)
                self.tela_tarefa.area_concluida.controls.append(self)
                self.tela_tarefa.area_tarefas.update()
                self.tela_tarefa.area_concluida.update()
                self.tela_tarefa.item_size()
                BancoDeDados.atualizar_tarefa(self.tela_tarefa.bd, self.tarefa_id, self.descricao, self.data, True, False, False)
            elif self in self.tela_tarefa.area_atrasada.controls:
                self.text.spans[0].style = ft.TextStyle(
                    decoration = ft.TextDecoration.LINE_THROUGH,
                    decoration_thickness = 2
                )
                self.tela_tarefa.area_atrasada.controls.remove(self)
                self.tela_tarefa.area_concluida.controls.append(self)
                self.tela_tarefa.area_atrasada.update()
                self.tela_tarefa.area_concluida.update()
                self.tela_tarefa.item_size()
                BancoDeDados.atualizar_tarefa(self.tela_tarefa.bd, self.tarefa_id, self.descricao, self.data, True, False, False)
        else:
            self.text.spans[0].style = ft.TextStyle()
            self.tela_tarefa.area_concluida.controls.remove(self)
            if self.data < date.today():
                self.tela_tarefa.area_atrasada.controls.append(self)
                self.tela_tarefa.area_concluida.update()
                self.tela_tarefa.area_atrasada.update()
                self.tela_tarefa.item_size()
                BancoDeDados.atualizar_tarefa(self.tela_tarefa.bd, self.tarefa_id, self.descricao, self.data, False, False, True)
            else:
                self.tela_tarefa.area_tarefas.controls.append(self)
                self.tela_tarefa.area_concluida.update()
                self.tela_tarefa.area_tarefas.update()
                self.tela_tarefa.item_size()
                BancoDeDados.atualizar_tarefa(self.tela_tarefa.bd, self.tarefa_id, self.descricao, self.data, False, False, False)
        self.text.update()

    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método delete_text
    Entradas: e (não utilizado, mas obrigatório no Flet)
    Saídas: -
    Descrição: Identifica em qual campo a tarefa está e a remove, além de removê-la também do banco de dados.
    --------------------------------------------------------------------------------------------------------------------
    """
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
        elif self in self.tela_tarefa.area_atrasada.controls:
            self.tela_tarefa.area_atrasada.controls.remove(self)
            self.tela_tarefa.area_atrasada.update()
            self.tela_tarefa.item_size()
        else:
            self.tela_tarefa.area_concluida.controls.remove(self)
            self.tela_tarefa.area_concluida.update()
        