import flet as ft
from flet_webview_all import FletWebviewAll
from theme import BG

def web_view(page, navigate):
    return ft.View(
        route="/webview",
        padding=0,
        controls=[
            ft.AppBar(
                title=ft.Text("十中校园服务", color="white", weight=ft.FontWeight.BOLD),
                bgcolor=BG,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: navigate("/")),
            ),
            FletWebviewAll(
                url="https://st.xssz.net.cn/visitorp/mobile/menuPage/mainHome",
                expand=True,
            )
        ],
        bgcolor=BG,
    )