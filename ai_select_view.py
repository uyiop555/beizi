import flet as ft
from theme import BG, CARD, PRIMARY, TEXT, MUTED

def ai_select_view(page, navigate):
    models = [
        {"name": "DeepSeek-V4.1-Flash", "id": "deepseek-flash", "desc": "直接可用"},
        {"name": "Gemini-4-Hydrogen", "id": "gemini-4-hydrogen", "desc": "开VPN"},
    ]

    def select_model(model_id):
        page.current_model = model_id
        navigate("/ai_math")

    cards = []
    for m in models:
        card = ft.Container(
            content=ft.Column([
                ft.Text(m["name"], size=16, weight=ft.FontWeight.BOLD, color=TEXT),
                ft.Text(m["desc"], size=12, color=MUTED),
            ]),
            bgcolor=CARD,
            padding=20,
            border_radius=12,
            on_click=lambda e, m_id=m["id"]: select_model(m_id),
            ink=True,
            width=320,
        )
        cards.append(card)

    return ft.View(
        route="/ai_select",
        padding=0,
        controls=[
            ft.AppBar(
                title=ft.Text("选择模型", color="white", weight=ft.FontWeight.BOLD),
                bgcolor=BG,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: navigate("/")),
            ),
            ft.Container(
                content=ft.Column(cards, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, expand=True),
                expand=True,
            )
        ],
        bgcolor=BG,
    )