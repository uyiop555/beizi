import flet as ft
from theme import BG, CARD, PRIMARY, TEXT, MUTED

def make_grid_card(title, desc, route, navigate, is_web=False):
    title_row = ft.Row(
        [
            ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=TEXT),
            ft.Container(
                content=ft.Text("(网页)", size=10, color=PRIMARY),
                bgcolor="#332200",
                padding=ft.Padding(left=4, right=4, top=1, bottom=1),
                border_radius=4,
            ) if is_web else ft.Container()
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    return ft.Container(
        content=ft.Column([
            title_row,
            ft.Text(desc, size=12, color=MUTED),
        ]),
        bgcolor=CARD,
        border_radius=10,
        padding=15,
        height=100,
        on_click=lambda _: navigate(route),
        expand=1,
        ink=True,
    )


def home_view(page, navigate):
    tools_data = [
        {"title": "解方程", "desc": "解ax²+bx+c=0", "route": "/solver", "is_web": False},
        {"title": "BMI 计算", "desc": "偏瘦，正常，超重，肥胖", "route": "/bmi", "is_web": False},
        {"title": "计算器", "desc": "滚木", "route": "/calc", "is_web": False},
        {"title": "萧山十中校园服务网页", "desc": "傻福十中", "route": "/webview", "is_web": True},
    ]

    search_field = ft.TextField(
        hint_text="搜索",
        hint_style=ft.TextStyle(color=MUTED),
        text_style=ft.TextStyle(color=TEXT),
        prefix_icon=ft.Icons.SEARCH,
        bgcolor=CARD,
        border_color="transparent",
        border_radius=30,
        cursor_color=PRIMARY,
    )

    title_container = ft.Container(
        content=ft.Text("乐迪计算器", size=32, weight=ft.FontWeight.BOLD, color=TEXT),
        padding=ft.Padding(left=20, right=20, top=60, bottom=0),
        alignment=ft.Alignment.CENTER,
    )

    creations_card = ft.Container(
        content=ft.Row([
            ft.Text("神的其他作品", size=16, weight=ft.FontWeight.BOLD, color="white"),
        ], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=PRIMARY,
        padding=10,
        border_radius=12,
        margin=ft.Margin(left=10, right=10, bottom=15, top=0),
        on_click=lambda _: navigate("/creations"),
        ink=True,
    )

    section_title = ft.Container(
        content=ft.Text("本地", size=14, weight=ft.FontWeight.BOLD, color=MUTED),
        padding=ft.Padding(left=20, right=20, bottom=10, top=0),
    )

    grid_column = ft.Column(spacing=15)

    def update_grid(search_query):
        grid_column.controls.clear()
        query = search_query.lower()

        filtered = [
            t for t in tools_data
            if query in t["title"].lower() or query in t["desc"].lower()
        ]

        if not filtered:
            grid_column.controls.append(
                ft.Text("滚木。。。", color=MUTED, size=14, text_align=ft.TextAlign.CENTER)
            )
        else:
            for i in range(0, len(filtered), 2):
                chunk = filtered[i:i + 2]
                row_controls = []
                for item in chunk:
                    row_controls.append(make_grid_card(
                        item["title"],
                        item["desc"],
                        item["route"],
                        navigate,
                        item.get("is_web", False)
                    ))
                if len(row_controls) == 1:
                    row_controls.append(ft.Container(expand=1))
                grid_column.controls.append(ft.Row(row_controls, spacing=15))

    search_field.on_change = lambda e: (update_grid(e.control.value), page.update())
    update_grid("")

    return ft.View(
        route="/",
        padding=0,
        controls=[
            ft.Column([
                title_container,
                ft.Container(
                    content=search_field,
                    padding=ft.Padding(left=10, right=10, top=20, bottom=10),
                ),
                creations_card,
                section_title,
                ft.Container(
                    content=grid_column,
                    padding=ft.Padding(left=10, right=10, bottom=20),
                )
            ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
        ],
        bgcolor=BG,
    )