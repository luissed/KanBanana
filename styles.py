from flet import *
import flet as ft

_dark: str = ft.colors.with_opacity(0.5, "white")
_light: str = ft.colors.with_opacity(1, "black")

toggle_style_sheet: dict = {
    "icon": ft.icons.DARK_MODE_ROUNDED,
    "icon_size": 18
}
add_style_sheet: dict = {
    "icon": ft.icons.ADD_ROUNDED,
    "icon_size": 18
}
item_style_sheet: dict = {
    "height": 50,
    "expand": True,
    "border_color": _dark,
    "cursor_height": 24,
    "hint_text": "Adicione sua tarefa aqui",
    "content_padding": 15
}
tarefa_style_sheet: dict = {
    "height": 50,
    "border_radius": 4
}