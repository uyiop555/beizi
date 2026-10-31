import os
import flet as ft
from flet_webview_all import FletWebviewAll
from theme import BG


def hstx_view(page, navigate):
    html_content = "<h1 style='color:white; padding:20px;'>读取 HTML 文件失败</h1>"

    paths_to_try = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "html", "graph.html"),
        os.path.join("assets", "html", "graph.html"),
        "assets/html/graph.html"
    ]

    for path in paths_to_try:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                break
            except Exception:
                pass

    return ft.View(
        route="/hstx",
        padding=0,
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