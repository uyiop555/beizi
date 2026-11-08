import re
import flet as ft
from ai_math import ask_math_ai
from theme import BG, CARD, PRIMARY, TEXT, MUTED, ERROR


def format_latex(text: str) -> str:
    text = text.replace(r"\[", "$$")
    text = text.replace(r"\]", "$$")
    text = text.replace(r"\(", "$")
    text = text.replace(r"\)", "$")

    def replace_text_cmd(match):
        return r"\mathrm{" + match.group(1) + "}"

    text = re.sub(r"\\text\{([^}]+)\}", replace_text_cmd, text)
    return text


def ai_math_view(page, navigate):
    chat_list = ft.ListView(expand=True, spacing=10, padding=10, auto_scroll=True)
    question_input = ft.TextField(
        hint_text="输入...",
        expand=True,
        multiline=True,
        min_lines=1,
        max_lines=4,
        bgcolor=CARD,
        border=ft.OutlineInputBorder(
            border_radius=15,
            side=ft.BorderSide(0, "transparent")
        ),
        cursor_color=PRIMARY,
    )
    send_button = ft.IconButton(ft.Icons.SEND, icon_color=PRIMARY)

    def add_message(text, is_user=False):
        clean_text = format_latex(text)
        chat_list.controls.append(
            ft.Container(
                content=ft.Markdown(
                    value=clean_text,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    latex_scale_factor=1.0,
                ),
                bgcolor=PRIMARY if is_user else CARD,
                padding=ft.Padding(10, 10, 10, 10),
                border_radius=12,
                alignment=ft.Alignment.CENTER_RIGHT if is_user else ft.Alignment.CENTER_LEFT,
                margin=ft.Margin(left=50 if is_user else 0, right=0 if is_user else 50),
            )
        )
        page.update()

    async def send_question(e):
        question = question_input.value.strip()
        if not question:
            return

        add_message(question, is_user=True)
        question_input.value = ""
        page.update()

        ai_message_container = ft.Container(
            content=ft.Markdown(value="思考中..."),
            bgcolor=CARD,
            padding=10,
            border_radius=12,
            alignment=ft.Alignment.CENTER_LEFT,
            margin=ft.Margin(left=0, right=50),
        )
        chat_list.controls.append(ai_message_container)
        page.update()

        full_response = ""

        async for chunk in ask_math_ai(question):
            full_response += chunk
            clean_text = format_latex(full_response)
            ai_message_container.content.value = clean_text
            page.update()

    send_button.on_click = send_question

    return ft.View(
        route="/ai_math",
        padding=0,
        controls=[
            ft.AppBar(
                title=ft.Text("AI", color="white", weight=ft.FontWeight.BOLD),
                bgcolor=BG,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: navigate("/")),
            ),
            ft.Container(
                content=ft.Column([
                    chat_list,
                    ft.Row([question_input, send_button], spacing=10),
                ], expand=True),
                padding=15,
                expand=True,
            )
        ],
        bgcolor=BG,
    )