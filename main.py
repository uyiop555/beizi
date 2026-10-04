import flet as ft
from theme import BG
from home import home_view
from solver import solver_view
from bmi import bmi_view
from calculator import calc_view
from creations import creations_view  # 导入作品页

def main(page: ft.Page):
    page.title = "乐迪计算器"
    page.bgcolor = BG
    page.window_width = 400
    page.window_height = 700
    page.theme = ft.Theme(font_family="Microsoft YaHei")

    def navigate(route: str):
        page.views.clear()
        if route == "/solver":
            page.views.append(solver_view(page, navigate))
        elif route == "/bmi":
            page.views.append(bmi_view(page, navigate))
        elif route == "/calc":
            page.views.append(calc_view(page, navigate))
        elif route == "/creations":
            page.views.append(creations_view(page, navigate))
        else:
            page.views.append(home_view(page, navigate))
        page.update()

    navigate("/")

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")