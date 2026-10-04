import flet as ft
from theme import BG, PRIMARY, TEXT, MUTED

def make_card(title, route, desc, navigate):
    return ft.Container(
        content=ft.Column(
            [ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color="white"),
             ft.Text(desc, size=12, color="white70")],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=PRIMARY, padding=15,
        border_radius=12, width=260, on_click=lambda _: navigate(route),
        ink=True, margin=ft.Margin(bottom=15, left=0, right=0, top=0),
        shadow=ft.BoxShadow(blur_radius=10, color="#d0d8e8"),
    )

def home_view(page, navigate):
    return ft.View(route="/", controls=[
        ft.Column([
            ft.Text("杯子计算器", size=32, weight=ft.FontWeight.BOLD, color=TEXT),
            ft.Text("选择一个功能", size=14, color=MUTED),
            ft.Divider(height=40, color="transparent"),
            make_card("解一元二次方程", "/solver", "求解 ax² + bx + c = 0", navigate),
            make_card("BMI 计算", "/bmi", "偏瘦，正常，超重，肥胖", navigate),
            make_card("计算器", "/calc", "滚木", navigate),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    ], bgcolor=BG)