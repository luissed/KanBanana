import flet as ft

class Principal():
    def __init__(self, page: ft.Page):
        self.page = page

    def tela(self):
        appBarItens=[
            ft.PopupMenuItem(text='Deslogar'),
            ft.PopupMenuItem(text='Configurações')
        ]

        appBar = ft.AppBar(
            leading=ft.Icon(
                ft.icons.APPS,
            ),
            leading_width=50,
            bgcolor="0xff1f005c",
            color=ft.colors.WHITE,
            surface_tint_color=ft.colors.BLACK,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            title=ft.Text(
                value='KanBanana',
                font_family='Annai MN',
                size=15,
                text_align='start'
            ),
            actions=[
                ft.Container(
                    content=(
                        ft.PopupMenuButton(
                            items=appBarItens,
                            icon=ft.icons.PERSON
                        )
                    ),
                    margin=ft.margin.only(left=50,right=10)
                )
            ]
        )
        self.page.appbar = appBar
        tela_main = ft.Container(
            content=(
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.FilledButton(
                                    text='Voltar',
                                    on_click=lambda _: self.page.go('/login')
                                )
                            ],
                            expand=True
                        )
                    ],
                )
            ),
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    "0xff1f005c",
                    "0xff5b0060",
                    "0xff870160",
                    "0xffac255e",
                ],
                tile_mode=ft.GradientTileMode.MIRROR
            )
        )
        return(tela_main)