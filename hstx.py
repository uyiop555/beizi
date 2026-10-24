import math
import flet as ft
import flet.canvas as cv
from theme import BG, CARD, PRIMARY, TEXT, MUTED, ERROR

def hstx_view(page, navigate):
    input_field = ft.TextField(
        multiline=True,
        min_lines=3,
        max_lines=5,
        value="",
        hint_text="单个函数直接输入（省略f(x)）\n分段函数格式：“范围:函数”",
        hint_style=ft.TextStyle(color=MUTED),
        text_style=ft.TextStyle(color=TEXT, font_family="Consolas"),
        bgcolor=CARD,
        border=ft.OutlineInputBorder(
            border_radius=10,
            side=ft.BorderSide(0, "transparent"),
        ),
        cursor_color=PRIMARY,
    )

    status_text = ft.Text("", color=PRIMARY, size=12, visible=False)

    canvas = cv.Canvas(width=350, height=350)
    canvas_container = ft.Container(
        content=canvas,
        bgcolor=CARD,
        border_radius=10,
        padding=10,
        alignment=ft.Alignment.CENTER,
    )

    def draw_graph(e):
        status_text.visible = False
        canvas.shapes.clear()
        page.update()

        code = input_field.value.strip()
        if not code:
            status_text.value = "请输入函数"
            status_text.color = ERROR
            status_text.visible = True
            page.update()
            return

        lines = code.split("\n")
        segments = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if ":" in line:
                cond_str, expr_str = line.split(":", 1)
                expr_str = expr_str.replace("^", "**")
                segments.append((cond_str.strip(), expr_str.strip()))
            else:
                segments.append(("True", line.replace("^", "**")))

        w, h = 350, 350
        x_min, x_max = -10.0, 10.0
        y_min, y_max = -10.0, 10.0

        def to_px_x(x):
            return (x - x_min) / (x_max - x_min) * w

        def to_px_y(y):
            return h - (y - y_min) / (y_max - y_min) * h

        grid_color = "#333333"
        axis_color = "#888888"

        for i in range(int(x_min), int(x_max) + 1):
            if i != 0:
                px = to_px_x(i)
                canvas.shapes.append(cv.Line(px, 0, px, h, paint=ft.Paint(color=grid_color, stroke_width=1)))

        for i in range(int(y_min), int(y_max) + 1):
            if i != 0:
                py = to_px_y(i)
                canvas.shapes.append(cv.Line(0, py, w, py, paint=ft.Paint(color=grid_color, stroke_width=1)))

        canvas.shapes.append(cv.Line(0, to_px_y(0), w, to_px_y(0), paint=ft.Paint(color=axis_color, stroke_width=2)))
        canvas.shapes.append(cv.Line(to_px_x(0), 0, to_px_x(0), h, paint=ft.Paint(color=axis_color, stroke_width=2)))

        safe_dict = {
            "math": math, "abs": abs, "sin": math.sin, "cos": math.cos,
            "tan": math.tan, "log": math.log, "sqrt": math.sqrt,
            "pi": math.pi, "e": math.e
        }

        try:
            elements = []
            is_drawing = False
            step = (x_max - x_min) / 400

            x = x_min
            while x <= x_max:
                y = None
                for cond_str, expr_str in segments:
                    if eval(cond_str, {"__builtins__": {}}, {**safe_dict, "x": x}):
                        y = eval(expr_str, {"__builtins__": {}}, {**safe_dict, "x": x})
                        break

                if y is not None and isinstance(y, (int, float)) and not math.isnan(y) and not math.isinf(y) and y_min <= y <= y_max:
                    px = to_px_x(x)
                    py = to_px_y(y)
                    if not is_drawing:
                        elements.append(cv.Path.MoveTo(px, py))
                        is_drawing = True
                    else:
                        elements.append(cv.Path.LineTo(px, py))
                else:
                    is_drawing = False

                x += step

            if elements:
                canvas.shapes.append(
                    cv.Path(
                        elements=elements,
                        paint=ft.Paint(color=PRIMARY, stroke_width=3, style=ft.PaintingStyle.STROKE)
                    )
                )
                status_text.value = "绘制成功"
                status_text.color = PRIMARY
                status_text.visible = True
            else:
                status_text.value = "滚木"
                status_text.color = ERROR
                status_text.visible = True

            page.update()

        except Exception as ex:
            status_text.value = f"格式滚木: {str(ex)}"
            status_text.color = ERROR
            status_text.visible = True
            page.update()

    return ft.View(
        route="/hstx",
        padding=0,
        controls=[
            ft.AppBar(
                title=ft.Text("函数图像绘制", color="white", weight=ft.FontWeight.BOLD),
                bgcolor=BG,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: navigate("/")),
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("^代表乘方，/表示除，*表示乘(不可省略) \n不等号分别为<   <=   >   >=\n\"sqrt(数字)\" 表示平方，\"abs(数字)\" 表示绝对值\n所有括号,冒号用英文", size=12, color=MUTED),
                    ft.Divider(height=5, color="transparent"),
                    input_field,
                    status_text,
                    ft.Button("绘制", on_click=draw_graph, bgcolor=PRIMARY, color="white", height=40),
                    ft.Divider(height=10, color="transparent"),
                    canvas_container,
                ], expand=True),
                padding=20,
                expand=True,
            )
        ],
        bgcolor=BG,
    )