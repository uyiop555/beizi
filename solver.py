import math
import flet as ft
from theme import BG, PRIMARY, TEXT, MUTED, ERROR, OK, fmt

def solver_view(page, navigate):
    a_in = ft.TextField(label="a", width=90, text_align=ft.TextAlign.CENTER)
    b_in = ft.TextField(label="b", width=90, text_align=ft.TextAlign.CENTER)
    c_in = ft.TextField(label="c", width=90, text_align=ft.TextAlign.CENTER)
    result = ft.Text("结果将显示在这里", size=16, weight=ft.FontWeight.BOLD, color=MUTED, text_align=ft.TextAlign.CENTER)

    def solve(e):
        try:
            a = float(a_in.value or 0); b = float(b_in.value or 0); c = float(c_in.value or 0)
        except ValueError:
            result.value = "请输入有效数字"; result.color = ERROR; page.update(); return

        if abs(a) < 1e-12:
            if abs(b) < 1e-12: result.value = "不是二次方程（a = 0）"
            else: result.value = f"一次方程\nx = {fmt(-c / b)}"
            result.color = ERROR
        else:
            delta = b ** 2 - 4 * a * c
            if delta < 0: result.value = f"没有实数根\nΔ = {fmt(delta)} < 0"; result.color = ERROR
            elif abs(delta) < 1e-12: result.value = f"两个相等的实数根\nx₁ = x₂ = {fmt(-b / (2 * a))}"; result.color = OK
            else:
                x1 = (-b + math.sqrt(delta)) / (2 * a); x2 = (-b - math.sqrt(delta)) / (2 * a)
                result.value = f"两个实数根\nx₁ = {fmt(x1)}\nx₂ = {fmt(x2)}\nΔ = {fmt(delta)}"; result.color = OK
        page.update()

    return ft.View(route="/solver", padding=20, controls=[
        ft.AppBar(title=ft.Text("解一元二次方程"), bgcolor=PRIMARY, color="white",
                  leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: navigate("/"))),
        ft.Column([
            ft.Text("ax² + bx + c = 0", size=16, color=TEXT),
            ft.Divider(height=20, color="transparent"),
            ft.Row([a_in, b_in, c_in], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ft.Divider(height=20, color="transparent"),
            ft.Button("计算", on_click=solve, bgcolor=PRIMARY, color="white", width=200),
            ft.Divider(height=30, color="transparent"), result,
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True,)
    ], bgcolor=BG)