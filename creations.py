import flet as ft
from theme import BG, CARD, PRIMARY, TEXT, MUTED


def make_work_card(title, desc, image_names):
    col_controls: list[ft.Control] = [
        ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=TEXT),
        ft.Text(desc, size=12, color=MUTED),
        ft.Divider(height=10, color="transparent")
    ]

    for img_name in image_names:
        col_controls.append(
            ft.Image(
                src=img_name,
                height=150,
                border_radius=8,
                fit=ft.BoxFit.COVER,
                margin=ft.Margin(bottom=10, top=0, left=0, right=0)
            )
        )

    return ft.Container(
        content=ft.Column(col_controls, horizontal_alignment=ft.CrossAxisAlignment.START),
        bgcolor=CARD,
        padding=15,
        border_radius=12,
        expand=1
    )


# 把 page 改成 _page，消除未使用的警告
def creations_view(_page, navigate):
    return ft.View(
        route="/creations",
        padding=0,
        controls=[
            ft.AppBar(
                title=ft.Text("神的其他作品", color="white", weight=ft.FontWeight.BOLD),
                bgcolor=PRIMARY,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: navigate("/")),
            ),
            ft.Container(
                content=ft.Row(
                    [
                        make_work_card(
                            "我的世界JAVA版模组",
                            "目前适配forge1.20.1\n正在做neoforge1.21.1",
                            ["mc_mod.jpg"]
                        ),
                        make_work_card(
                            "TACZ枪包",
                            "目前做了8个家具",
                            ["tacz_1.jpg", "tacz_3.jpg", "tacz_2.jpg"]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=10
                ),
                padding=20,
                expand=True
            )
        ],
        bgcolor=BG,
    )