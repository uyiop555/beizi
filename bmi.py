import flet as ft
from theme import BG, PRIMARY, MUTED, ERROR, OK

def bmi_view(page, navigate):
    h_in = ft.TextField(label="身高 (cm)", width=130, text_align=ft.TextAlign.CENTER)
    w_in = ft.TextField(label="体重 (kg)", width=130, text_align=ft.TextAlign.CENTER)
    result = ft.Text("结果将显示在这里", size=16, weight=ft.FontWeight.BOLD, color=MUTED, text_align=ft.TextAlign.CENTER)

    def calc(e):
        try:
            h_cm = float(h_in.value); w = float(w_in.value)
        except ValueError:
            result.value = "请输入有效数字"; result.color = ERROR; page.update(); return
        if h_cm <= 0 or w <= 0:
            result.value = "身高和体重必须大于 0"; result.color = ERROR; page.update(); return

        h = h_cm / 100; bmi = w / (h * h)
        if bmi < 18.5: level = "偏瘦"; result.color = "#e8a33d"
        elif bmi < 24: level = "正常"; result.color = OK
        elif bmi < 28: level = "超重"; result.color = "#e8a33d"
        else: level = "肥胖"; result.color = ERROR

        result.value = f"BMI = {bmi:.1f}\n你的范围：{level}\n\n参考：\n偏瘦 < 18.5\n正常 18.5 ~ 24\n超重 24 ~ 28\n肥胖 ≥ 28"
        page.update()

    return ft.View(
        route="/bmi",
        padding=0,
        controls=[
            ft.AppBar(
                title=ft.Text("BMI 计算", color="white", weight=ft.FontWeight.BOLD),
                bgcolor=PRIMARY,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: navigate("/")),
            ),
            # 下方内容加自己的边距
            ft.Container(
                content=ft.Column([
                    ft.Text("BMI = 体重(kg) ÷ 身高(m)²", size=14, color=MUTED),
                    ft.Divider(height=20, color="transparent"),
                    ft.Row([h_in, w_in], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                    ft.Divider(height=20, color="transparent"),
                    ft.Button("计算", on_click=calc, bgcolor=PRIMARY, color="white", width=200),
                    ft.Divider(height=30, color="transparent"),
                    result,
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
                padding=20,
                expand=True,
            )
        ],
        bgcolor=BG,
    )