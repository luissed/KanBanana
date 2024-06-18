import flet as ft
from typing import Type
from login import Login
from registro import Registrar
from principal import Principal
from configuracoes import Configuracoes

"""
--------------------------------------------------------------------------------------------------------------------
                                            Método criar_appbar
Entradas: login, page, configuracoes.
Saídas: ft.AppBar
Descrição: Recebe as configuraçoes da pagina de login (login), da pagina atual (page) e do pop-up de configurações.
           Retorna uma barra de menu contendo:
           - Logo do aplicativo
           - Nome do aplicativo
           - Nome do usuário
           - Botões para deslogar e acessar configurações
--------------------------------------------------------------------------------------------------------------------
"""
def criar_appbar(login: Type[Login], page: ft.Page, configuracoes: Type[Configuracoes]) -> ft.AppBar:
    appBarItens = [
        ft.PopupMenuItem(
            text = 'Deslogar',
            on_click  =lambda _: page.go("/login"),
        ),
        ft.PopupMenuItem(
            text = "Configurações",
            on_click = lambda _: configuracoes.abrir_configuracoes()
        )
    ]

    return ft.AppBar(
        leading = ft.Image(src = "/images/banana.webp"),
        leading_width = 30,
        title = ft.Text(
            value = "KanBanana",
            font_family = "Chalkboard",
            size = 15,
            text_align = "start"
        ),
        actions = [
            ft.Row(
                controls = [
                    ft.Container(
                        content = ft.Text(
                            value = login.usuario
                        ),
                    ),
                    ft.Container(
                        content = ft.PopupMenuButton(
                            items = appBarItens,
                            icon = ft.icons.PERSON,
                            menu_position = ft.PopupMenuPosition.UNDER
                        ),
                        margin = ft.margin.only(left = 10, right = 10)
                    )
                ],
                spacing = 0
            )
        ]
    )

"""
--------------------------------------------------------------------------------------------------------------------
                                            Método views_handler
Entradas: page, login, registro, principal, configuracoes
Saídas: ft.View
Descrição: Recebe a página atual, as configurações das telas de login, registro, principal, e o pop-up de configurações.
           Retorna o conteúdo que deve ser exibido na tela do aplicativo dependendo da rota, utilizando um dicionário.
--------------------------------------------------------------------------------------------------------------------
"""
def views_handler(page: ft.Page, login: Type[Login], registro: Type[Registrar], principal: Type[Principal], configuracoes: Type[Configuracoes]) -> ft.View:
    return {
        "/": ft.View(
            route = "/",
            controls = [principal.tela_tarefa()],
            padding = 0,
            appbar = criar_appbar(login, page, configuracoes)
        ),
        "/login": ft.View(
            route = "/login",
            controls = [login.tela_login(principal, configuracoes)],
            padding = 0
        ),
        "/registro": ft.View(
            route = "/registro",
            controls = [registro.tela_registro()],
            padding = 0
        )
    }
