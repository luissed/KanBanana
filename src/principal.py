from flet import *
import flet as ft
from styles import _dark, _light, toggle_style_sheet, add_style_sheet, bg_gradient, bg_gradient_dark, button_style, button_style_reverse
from tarefa import Tarefa
from banco_de_dados import BancoDeDados
from datetime import date, datetime

"""
-------------------------------------------------- Classe Principal --------------------------------------------------
Entradas: Page
Saídas: -
Descrição: Configura a tela principal do aplicativo, com os seguintes elementos:
           - Barra de menu com a logo, nome do aplicativo, nome do usuário, e botões para deslogar e acessar as
           configurações.
           - Linha contendo "Minhas Tarefas", botão para adicionar tarefas, e botão para alternar entre modo diurno e 
           noturno.
           - Quatro campos para organizar as tarefas:
             - "A fazer";
             - "Atrasadas";
             - "Em andamento";
             - "Tarefas Concluídas".
           Cada campo contém suas respectivas tarefas. A classe também carrega as tarefas dos usuários salvas em um
           banco de dados.
----------------------------------------------------------------------------------------------------------------------
"""
class Principal(ft.SafeArea):
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.__bd, self.__cursor = BancoDeDados._conectar_ao_banco()
        self.__usuario_logado = None

        #Atributos Flet
        self.title = ft.Text(
            value = "MINHAS TAREFAS",
            size = 20,
            weight = "w800"
        )

        self.toggle = ft.IconButton(
            **toggle_style_sheet, 
            on_click = lambda e: self.switch(e)
        )

        self.add = ft.IconButton(
            **add_style_sheet,
            on_click = self.add_board
        )

        self.area_tarefas = ft.Column(
            spacing = 18,
            expand=True,
            scroll="Auto"
        )

        self.counter = ft.Text(
            value = "0 itens",
            italic = True
        )

        self.area_atrasada = ft.Column(
            spacing = 18,
            expand = True,
            scroll = "Auto"
        )

        self.counter_atrasada = ft.Text(
            value = "0 itens",
            italic = True
        )

        self.area_andamento = ft.Column(
            spacing = 18,
            expand = True,
            scroll = "Auto"
        )

        self.counter_andamento = ft.Text(
            value = "0 itens",
            italic = True
        )

        self.area_concluida = ft.Column(
            spacing = 18,
            expand = True,
            scroll = "Auto"
        )

    @property
    def bd(self):
        return self.__bd
    
    @property
    def usuario_logado(self) -> int:
        return self.__usuario_logado
    
    @usuario_logado.setter
    def usuario_logado(self, usuario_logado: int) -> None:
        self.__usuario_logado = usuario_logado
        
    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método item_size
    Entradas: -
    Saídas: -
    Descrição: Conta o número de tarefas em cada campo e atualiza seus respectivos contadores.
    --------------------------------------------------------------------------------------------------------------------
    """
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
    
    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método carregar_tarefas
    Entradas: -
    Saídas: -
    Descrição: Se o usuário estiver logado, este método obtém todas as tarefas daquele usuário no banco de dados, limpa 
    os campos de tarefas na interface e adiciona as tarefas nos campos correspondentes (concluída, em andamento, atrasada 
    e pendente).
    --------------------------------------------------------------------------------------------------------------------
    """
    def carregar_tarefas(self) -> None:
        if self.__usuario_logado is not None:
            # Obtem do banco de dados todas as tarefas do usuário logado
            tarefas = BancoDeDados.obter_tarefas(self.__bd, self.__usuario_logado)

            self.area_tarefas.controls.clear()
            self.area_concluida.controls.clear()
            self.area_andamento.controls.clear()
            self.area_atrasada.controls.clear()

            for tarefa in tarefas:
                tarefa_id, descricao, data_str, concluida, em_andamento, atrasada = tarefa
                data = datetime.strptime(data_str, '%Y-%m-%d').date()
                theme = "dark" if self.page.theme_mode == ft.ThemeMode.DARK else "light"
                obj_tarefa = Tarefa(self, descricao, theme, self.__usuario_logado, data, tarefa_id)

                if data == date.today():
                    obj_tarefa.data_text.spans[0].style = ft.TextStyle(color = "amber")
                elif data < date.today():
                    obj_tarefa.data_text.spans[0].style = ft.TextStyle(color = "red")

                if concluida:
                    obj_tarefa.tick.value = True
                    obj_tarefa.text.spans[0].style = ft.TextStyle(
                        decoration = ft.TextDecoration.LINE_THROUGH,
                        decoration_thickness = 2
                    )
                    self.area_concluida.controls.append(obj_tarefa)
                elif data < date.today():
                    self.area_atrasada.controls.append(obj_tarefa)
                    if not atrasada:
                        BancoDeDados.atualizar_tarefa(self.__bd, tarefa_id, descricao, data, False, False, True)
                elif em_andamento:
                    self.area_andamento.controls.append(obj_tarefa)
                else:
                    self.area_tarefas.controls.append(obj_tarefa)
                    
            self.area_tarefas.update()
            self.area_atrasada.update()
            self.area_andamento.update()
            self.area_concluida.update()
            self.item_size()
    
    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método verifica_atrasada
    Entradas: -
    Saídas: -
    Descrição: Reorganiza os campos de tarefas para identificar as tarefas atrasadas e colocá-las em seu respectivo campo.
    --------------------------------------------------------------------------------------------------------------------
    """
    def verifica_atrasada(self) -> None:
        for tarefa in self.area_tarefas.controls[:]:
            if tarefa.data == date.today():
                tarefa.data_text.spans[0].style = ft.TextStyle(color = "amber")
            elif tarefa.data < date.today():
                tarefa.data_text.spans[0].style = ft.TextStyle(color = "red")
                self.area_tarefas.controls.remove(tarefa)
                self.area_atrasada.controls.append(tarefa)
                BancoDeDados.atualizar_tarefa(self.__bd, tarefa.tarefa_id, tarefa.descricao, tarefa.data, False, False, True)
       
        for tarefa in self.area_andamento.controls[:]:
            if tarefa.data == date.today():
                tarefa.data_text.spans[0].style = ft.TextStyle(color = "amber")
            elif tarefa.data < date.today():
                tarefa.data_text.spans[0].style = ft.TextStyle(color = "red")
                self.area_andamento.controls.remove(tarefa)
                self.area_atrasada.controls.append(tarefa)
                BancoDeDados.atualizar_tarefa(self.__bd, tarefa.tarefa_id, tarefa.descricao, tarefa.data, False, False, True)
        
        self.area_tarefas.update()
        self.area_andamento.update()
        self.area_atrasada.update()
        self.item_size()

    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método add_item
    Entradas: dialog_text, data_picker
    Saídas: -
    Descrição: Adiciona uma nova tarefa no campo "A fazer". Se a tarefa criada já estiver atrasada, ela é adicionada no 
    campo "Atrasadas" em vez de "A fazer".
    --------------------------------------------------------------------------------------------------------------------
    """
    def add_item(self, dialog_text: str, date_picker: date) -> None:
        if dialog_text != "":
            BancoDeDados.adicionar_tarefa(self.__bd, self.__usuario_logado, dialog_text, date_picker)
            tarefas = BancoDeDados.obter_tarefas(self.__bd, self.__usuario_logado)
            if tarefas:
                tarefa_id = tarefas[-1][0] 
            else: None

            if self.page.theme_mode == ft.ThemeMode.DARK:
                self.area_tarefas.controls.append(Tarefa(self, dialog_text, "dark", self.__usuario_logado, date_picker, tarefa_id))
            else:
                self.area_tarefas.controls.append(Tarefa(self, dialog_text, "light", self.__usuario_logado, date_picker, tarefa_id))
            self.verifica_atrasada()

        else:
            pass

    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método add_board
    Entradas: -
    Saídas: -
    Descrição: Exibe um pop-up na tela do usuário contendo:
            - Um campo de texto para a descrição da tarefa.
            - Um botão para escolher a data da tarefa.
            - Um botão para criar a tarefa, habilitado somente se o usuário digitar algo no campo de texto.
            Também configura o calendário para selecionar a data.
    --------------------------------------------------------------------------------------------------------------------
    """
    def add_board(self, e) -> None:
        def close_dlg(e):
            self.add_item(dialog_text.value, date_picker.value.date())
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

        dialog_text = ft.TextField(
            label = "Nome da nova tarefa",
            border_color = "black87" if self.page.theme_mode == ft.ThemeMode.LIGHT else "white",
            label_style = ft.TextStyle(
                color = "black87" if self.page.theme_mode == ft.ThemeMode.LIGHT else "black54",
                weight = "bold",
                font_family = "Arial Rounded MT Bold",
                size = 14
            ),
            cursor_height = 15,
            cursor_width = 1,
            cursor_color = "black87" if self.page.theme_mode == ft.ThemeMode.LIGHT else "white",
            color = "black87" if self.page.theme_mode == ft.ThemeMode.LIGHT else "black54",
            border_width = 2,
            on_submit = close_dlg,
            on_change = textfield_change
        )

        create_button = ft.ElevatedButton(
            text = "Criar",
            style = button_style_reverse if self.page.theme_mode == ft.ThemeMode.LIGHT else button_style,
            on_click = close_dlg,
            disabled=True
        )

        date_picker = ft.DatePicker(
            value=date.today(),
        )

        self.page.overlay.append(date_picker)

        date_button = ft.ElevatedButton(
            text = "Escolha uma data",
            icon = ft.icons.CALENDAR_MONTH,
            style = button_style_reverse if self.page.theme_mode == ft.ThemeMode.LIGHT else button_style,
            on_click = lambda _: date_picker.pick_date(),
        )

        dialog_content = ft.Container(
            content = ft.Column(
                controls = [
                    dialog_text,
                    ft.Row(
                        controls = [
                            date_button,
                            create_button,
                        ],
                        alignment = "spaceBetween",
                    ),
                ],
                tight = True,
            ),
            width = 500,  
            height = 140  
        )

        dialog = ft.AlertDialog(
            title = ft.Row(
                controls = [
                    ft.Text("Criar nova tarefa"),
                    ft.IconButton(
                        icon = ft.icons.CLOSE,
                        on_click = cancel_task,
                        icon_color = "grey700"
                    )
                ],
                alignment = "spaceBetween"

            ),
            title_text_style = ft.TextStyle(
                color = "black87" if self.page.theme_mode == ft.ThemeMode.LIGHT else "black54",
                weight = "bold",
                font_family = "Arial Rounded MT",
                size = 18,
            ),
            bgcolor = ft.colors.with_opacity(0.8, "grey100"),
            content = dialog_content
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        dialog_text.focus()
    
    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método switch
    Entradas: -
    Saídas: -
    Descrição: Alterna as cores dos itens da tela entre os temas diurno e noturno. Se o tema atual for diurno, a troca 
    muda para o tema noturno e vice-versa.
    --------------------------------------------------------------------------------------------------------------------
    """
    def switch(self, e) -> None:
        if self.page.theme_mode == ft.ThemeMode.DARK:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.toggle.icon = ft.icons.DARK_MODE_ROUNDED
            self.toggle.icon_color = "black87"
            self.add.icon_color = "black87"

            self.page.theme = ft.Theme(
                appbar_theme = ft.AppBarTheme(
                    color = "black87",
                    bgcolor = "yellow"
                ),
                dialog_theme = ft.DialogTheme(
                    content_text_style = ft.TextStyle(color = "white")
                )
            )

            self.main.gradient = bg_gradient

            for item in self.area_tarefas.controls[:]:
                item.border = ft.border.all(1, _light)
                item.content.controls[0].controls[2].icon_color = "black"
                item.content.controls[0].controls[3].icon_color = "black"
                item.content.controls[1].controls[0].color = "black"
            
            for item in self.area_atrasada.controls[:]:
                item.border = ft.border.all(1, _light)
                item.content.controls[0].controls[2].icon_color = "black"
                item.content.controls[0].controls[3].icon_color = "black"
                item.content.controls[1].controls[0].color = "black"
            
            for item in self.area_andamento.controls[:]:
                item.border = ft.border.all(1, _light)
                item.content.controls[0].controls[2].icon_color = "black"
                item.content.controls[0].controls[3].icon_color = "black"
                item.content.controls[1].controls[0].color = "black"
            
            for item in self.area_concluida.controls[:]:
                item.border = ft.border.all(1, _light)
                item.content.controls[0].controls[2].icon_color = "black"
                item.content.controls[0].controls[3].icon_color = "black"
                item.content.controls[1].controls[0].color = "black"

        else:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.toggle.icon = ft.icons.LIGHT_MODE_ROUNDED
            self.toggle.icon_color = "white"
            self.add.icon_color = "white"

            self.page.theme = ft.Theme(
                appbar_theme = ft.AppBarTheme(
                    color = "white",
                    bgcolor = "black87"
                )
            )

            self.main.gradient = bg_gradient_dark

            for item in self.area_tarefas.controls[:]:
                item.border = ft.border.all(1, _dark)
                item.content.controls[0].controls[2].icon_color = "white"
                item.content.controls[0].controls[3].icon_color = "white"
                item.content.controls[1].controls[0].color = "white"
            
            for item in self.area_atrasada.controls[:]:
                item.border = ft.border.all(1, _dark)
                item.content.controls[0].controls[2].icon_color = "white"
                item.content.controls[0].controls[3].icon_color = "white"
                item.content.controls[1].controls[0].color = "white"
            
            for item in self.area_andamento.controls[:]:
                item.border = ft.border.all(1, _dark)
                item.content.controls[0].controls[2].icon_color = "white"
                item.content.controls[0].controls[3].icon_color = "white"
                item.content.controls[1].controls[0].color = "white"
            
            for item in self.area_concluida.controls[:]:
                item.border = ft.border.all(1, _dark)
                item.content.controls[0].controls[2].icon_color = "white"
                item.content.controls[0].controls[3].icon_color = "white"
                item.content.controls[1].controls[0].color = "white"

        self.page.update()

    """
    --------------------------------------------------------------------------------------------------------------------
                                                Método tela_tarefa
    Entradas: -
    Saídas: main (Retorna as configurações da interface para serem exibidas na tela).
    Descrição: Retorna a configuração da tela principal do aplicativo. Esta tela inclui:
                - Barra de menu com a logo, nome do aplicativo, nome do usuário, e botões para deslogar e acessar as
                configurações.
                - Linha contendo "Minhas Tarefas", botão para adicionar tarefas, e botão para alternar entre modo diurno e 
                noturno.
                - Quatro campos para organizar as tarefas:
                - "A fazer";
                - "Atrasadas";
                - "Em andamento";
                - "Tarefas Concluídas".
    --------------------------------------------------------------------------------------------------------------------
    """
    def tela_tarefa(self):
        self.main = ft.Container(
            content = ft.Column(
                controls = [
                    ft.Row(
                        alignment = "start",
                        controls = [
                            self.title, 
                            ft.Container(
                                expand = True
                            ),
                            self.add, 
                            self.toggle
                        ],
                    ),
                    ft.Divider(height=20),
                    ft.ResponsiveRow(
                        alignment = "spaceBetween",
                        columns = 80,
                        controls = [
                            ft.Container(
                                col = {"xs": 20},
                                content = ft.Column(
                                    controls = [
                                        ft.Row(
                                            alignment = "spaceBetween",
                                            col = 2,
                                            controls = [
                                                ft.Text("A fazer"),
                                                self.counter
                                            ]
                                        ),
                                        self.area_tarefas
                                    ],
                                ),
                                bgcolor = ft.colors.with_opacity(0.5, "grey50"),
                                border_radius = 5,
                                border = ft.border.all(1, "grey50"),
                                padding = 10,
                            ),
                            ft.Container(
                                col = {"xs": 20},
                                content = ft.Column(
                                    controls = [
                                        ft.Row(
                                            alignment = "spaceBetween",
                                            col = 2,
                                            controls = [
                                                ft.Text("Atrasadas"),
                                                self.counter_atrasada
                                            ]
                                        ),
                                        self.area_atrasada
                                    ],
                                ),
                                bgcolor = ft.colors.with_opacity(0.5, "grey50"),
                                border_radius = 5,
                                border = ft.border.all(1, "grey50"),
                                padding = 10,
                            ),
                            ft.Container(
                                col = {"xs": 20},
                                content = ft.Column(
                                    controls = [
                                        ft.Row(
                                            alignment = "spaceBetween",
                                            col = 2,
                                            controls = [
                                                ft.Text("Em andamento"),
                                                self.counter_andamento
                                            ]
                                        ),
                                        self.area_andamento
                                    ],
                                ),
                                bgcolor = ft.colors.with_opacity(0.5, "grey50"),
                                border_radius = 5,
                                border = ft.border.all(1, "grey50"),
                                padding = 10,
                            ),
                            ft.Container(
                                col = {"xs": 20},
                                content = ft.Column(
                                    controls = [
                                        ft.Text("Tarefas Concluídas"),
                                        self.area_concluida
                                    ],
                                ),
                                bgcolor = ft.colors.with_opacity(0.5,"grey50"),
                                border_radius = 5,
                                border = ft.border.all(1, "grey50"),
                                padding = 10,
                            ),
                        ],
                        expand = True
                    )
                ],
            ),
            expand = True,
            gradient = bg_gradient,
            padding = ft.padding.all(20),
        )

        #Configura o tema da barra de menu
        self.page.theme = ft.Theme(
            appbar_theme = ft.AppBarTheme(
                bgcolor = "yellow",
                color = "black87",
            )
        )

        return self.main