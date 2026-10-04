import flet as ft
from theme import BG, PRIMARY, TEXT, ERROR, OK

def calc_view(page, navigate):
    display = ft.TextField(value="", text_align=ft.TextAlign.RIGHT, read_only=True, text_size=24, width=320)

    def press(ch):
        if ch == "C": display.value = ""
        elif ch == "←": display.value = display.value[:-1]
        elif ch == "=":
            try:
                expr = display.value.replace("×", "*").replace("÷", "/")
                if not set(expr).issubset(set("0123456789.+-*/() ")): display.value = "错误"
                else:
                    res = eval(expr, {"__builtins__": {}}, {})
                    if isinstance(res, float) and res.is_integer(): res = int(res)
                    display.value = str(res)
            except Exception: display.value = "错误"
        else: display.value += ch
        page.update()

    def make_btn(text, color=TEXT, bgcolor="#e8edf7"):
        return ft.Container(
            content=ft.Text(text, size=22, weight=ft.FontWeight.BOLD, color=color),
            alignment=ft.Alignment.CENTER,
            bgcolor=bgcolor, border_radius=8,
            on_click=lambda e, t=text: press(t), ink=True, expand=1, height=65, margin=2
        )

    layout = [["C", "←", "÷", "×"], ["7", "8", "9", "-"], ["4", "5", "6", "+"], ["1", "2", "3", "="], [".", "0", "", ""]]
    rows = []
    for row in layout:
        row_controls = []
        for ch in row:
            if ch == "": row_controls.append(ft.Container(expand=1, height=65, margin=2))
            elif ch in ["÷", "×", "-", "+"]: row_controls.append(make_btn(ch, color="white", bgcolor=PRIMARY))
            elif ch == "=": row_controls.append(make_btn(ch, color="white", bgcolor=OK))
            elif ch in ["C", "←"]: row_controls.append(make_btn(ch, color="white", bgcolor=ERROR))
            else: row_controls.append(make_btn(ch))
        rows.append(ft.Row(row_controls, spacing=0, alignment=ft.MainAxisAlignment.CENTER))

    return ft.View(route="/calc", padding=20, controls=[
        ft.AppBar(title=ft.Text("计算器"), bgcolor=PRIMARY, color="white",
                  leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: navigate("/"))),
        ft.Column([display, ft.Divider(height=10, color="transparent"), *rows],
                  alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True,)
    ], bgcolor=BG)