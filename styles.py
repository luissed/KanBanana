from flet import *
import flet as ft

_dark: str = ft.colors.with_opacity(1, "black")
_light: str = ft.colors.with_opacity(1, "black")

alerta: dict = {
    'login': ft.Container(
        content=(
            ft.Text(
                value='Usuário ou senha incorretos',
                color=ft.colors.RED
            )
        )
    ),
    'registro': ft.Container(
        content=(
            ft.Text(
                value='Usuário já existe',
                color=ft.colors.RED
            )
        )
    ),
    'preenchimento': ft.Container(
        content=(
            ft.Text(
                value='Por favor, preencha todos os campos',
                color=ft.colors.RED
            )
        )
    )
}

toggle_style_sheet: dict = {
    "icon": ft.icons.DARK_MODE_ROUNDED,
    "icon_size": 18,
    "icon_color": ft.colors.BLACK87
}
add_style_sheet: dict = {
    "icon": ft.icons.ADD_ROUNDED,
    "icon_size": 18,
    "icon_color": ft.colors.BLACK87
}
item_style_sheet: dict = {
    "height": 50,
    "expand": True,
    "border_color": _light,
    "cursor_height": 24,
    "hint_text": "Adicione sua tarefa aqui",
    "content_padding": 15
}
tarefa_style_sheet: dict = {
    "height": 50,
    "border_radius": 4
}

button_style: ft.ButtonStyle = ft.ButtonStyle(
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
)
