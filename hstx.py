import os
import flet as ft
from flet_webview_all import FletWebviewAll
from theme import BG

def hstx_view(page, navigate):
    html_path = os.path.join("assets", "html", "graph.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        html_content = "<h1 style='color:white; padding:20px;'>找不到 HTML 文件，请检查路径</h1>"

    return ft.View(
        route="/hstx", padding=0,
        controls=[
            ft.AppBar(
                title=ft.Text("函数图像绘制", color="white", weight=ft.FontWeight.BOLD),
                bgcolor=BG,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: navigate("/"))
            ),
            FletWebviewAll(html=html_content, expand=True)
        ],
        bgcolor=BG,
    )