import flet as ft
from views import views_handler
from login import Login
from registro import Registrar
from principal import Principal
from configuracoes import Configuracoes

def main(page: ft.Page):
    """
    Define as configurações básicas do aplicativo, incluindo:
    - Nome do aplicativo;
    - Tema;
    - Tamanho mínimo e máximo da janela;
    - Diretório dos assets;
    - Comandos básicos para execução do framework Flet.
    Além disso, cria um objeto para cada configuração de tela.
    """
    page.title = 'KanBanana'
    page.theme_mode = 'light'
    page.window_min_height = 600
    page.window_min_width = 400
    page.fonts = {
        "Chalkboard": "/fonts/Chalkboard.ttc"
    }

    principal = Principal(page)
    login = Login(page)
    registro = Registrar(page)
    configuracoes = Configuracoes(page, principal)

    """
    --------------------------------------------------------------------------------------------------------------------
                                            Método criar_appbar
    Entradas: route (obrigatório no Flet)
    Saídas: -
    Descrição: Recebe os objetos de cada tela e do pop-up de configuração. A partir da rota selecionada pelo comando page.go,
               acessa o dicionário e exibe a tela correspondente no aplicativo.
    --------------------------------------------------------------------------------------------------------------------
    """
    def route_change(route) -> None:
        page.views.clear()
        page.views.append(
            views_handler(page, login, registro, principal, configuracoes)[page.route]
        )
        page.update()

    page.on_route_change = route_change
    page.go("/login")

ft.app(target=main, assets_dir="assets")
