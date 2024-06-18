from flet import *
import flet as ft

"""
------------------------------------------------------ Styles ------------------------------------------------------
Descrição: Uma biblioteca contendo todos os styles para a interface gráfica do Flet.
--------------------------------------------------------------------------------------------------------------------
"""
_dark = ft.colors.with_opacity(1, "white")
_light = ft.colors.with_opacity(1, "black")

alerta: dict = {
    'login': ft.Container(
        content=(
            ft.Text(
                value = "Usuário ou senha incorretos",
                color = "red"
            )
        )
    ),
    'registro': ft.Container(
        content=(
            ft.Text(
                value = "Usuário já existe",
                color = "red"
            )
        )
    ),
    'preenchimento': ft.Container(
        content=(
            ft.Text(
                value = "Por favor, preencha todos os campos",
                color = "red"
            )
        )
    )
}

toggle_style_sheet: dict = {
    "icon": ft.icons.DARK_MODE_ROUNDED,
    "icon_size": 18,
    "icon_color": "black87"
}
add_style_sheet: dict = {
    "icon": ft.icons.ADD_ROUNDED,
    "icon_size": 18,
    "icon_color": "black87"
}
tarefa_style_sheet: dict = {
    "border_radius": 4
}

button_style_login = ft.ButtonStyle(
    color = {
        ft.MaterialState.DEFAULT: "black87",
        ft.MaterialState.HOVERED: "white"
    },
    bgcolor = {
        ft.MaterialState.DEFAULT: "white",
        ft.MaterialState.HOVERED: "black87"
    },
    shape = ft.RoundedRectangleBorder(radius=10)
)

button_style_registrar = ft.ButtonStyle(
    color = {
        ft.MaterialState.DEFAULT: "black54",
        ft.MaterialState.HOVERED: "white"
    },
    bgcolor = {
        ft.MaterialState.DEFAULT: "transparent",
        ft.MaterialState.HOVERED: "black87"
    },
    shape = ft.RoundedRectangleBorder(radius=10)
)

button_style = ft.ButtonStyle(
    color = {
        ft.MaterialState.DEFAULT: "black87",
        ft.MaterialState.HOVERED: "white"
    },
    bgcolor = {
        ft.MaterialState.DEFAULT: "white",
        ft.MaterialState.HOVERED: "black87",
        ft.MaterialState.DISABLED: "grey"
    },
    shape = ft.RoundedRectangleBorder(radius=5)
)

button_style_reverse = ft.ButtonStyle(
    color = {
        ft.MaterialState.DEFAULT: "white",
        ft.MaterialState.HOVERED: "black87"
    },
    bgcolor = {
        ft.MaterialState.DEFAULT: "black87",
        ft.MaterialState.HOVERED: "white",
        ft.MaterialState.DISABLED: "grey"
    },
    shape = ft.RoundedRectangleBorder(radius=5)
)

bg_gradient = ft.LinearGradient(
    begin = ft.alignment.top_center,
    end = ft.alignment.bottom_center,
    colors = [
        "yellow",
        "yellow200"
    ]
)

bg_gradient_dark = ft.LinearGradient(
    begin = ft.alignment.top_center,
    end = ft.alignment.bottom_center,
    colors = [
        "black",
        "grey900"
    ]
)