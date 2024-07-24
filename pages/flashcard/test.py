import flet as ft
import random

def main(page: ft.Page):
    page.title = "Perfect Flashcard App"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.bgcolor = "#1A1A2E"  # Deep blue background

    current_card = 0
    cards = [
        {"question": "1 + 1 = ?", "answer": "2", "icon": ft.icons.ADD},
        {"question": "2 * 3 = ?", "answer": "6", "icon": ft.icons.CLOSE},
        {"question": "9 - 5 = ?", "answer": "4", "icon": ft.icons.REMOVE},
    ]

    def change_card(forward: bool):
        nonlocal current_card
        if forward and current_card < len(cards) - 1:
            current_card += 1
        elif not forward and current_card > 0:
            current_card -= 1
        update_card()

    def flip_card(e):
        is_question = card_text.value == cards[current_card]["question"]
        card_text.value = cards[current_card]["answer"] if is_question else cards[current_card]["question"]
        card_icon.visible = not is_question
        card_content.bgcolor = "#0F3460" if is_question else "#16213E"
        card_content.update()

    def update_card():
        card_icon.name = cards[current_card]["icon"]
        card_text.value = cards[current_card]["question"]
        card_icon.visible = True
        card_content.bgcolor = "#16213E"
        progress_bar.value = (current_card + 1) / len(cards)
        page.update()

    card_icon = ft.Icon(name=cards[0]["icon"], size=50, color="#E94560")
    card_text = ft.Text(
        value=cards[0]["question"],
        size=30,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        color="#FFFFFF",
    )

    card_content = ft.Container(
        content=ft.Column([card_icon, card_text], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        width=300,
        height=200,
        border_radius=20,
        bgcolor="#16213E",
        alignment=ft.alignment.center,
        on_click=flip_card,
        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
    )

    progress_bar = ft.ProgressBar(width=300, color="#E94560", bgcolor="#0F3460", value=1/len(cards))

    flashcard = ft.Container(
        content=ft.Column([card_content, progress_bar], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        width=320,
        height=280,
        border_radius=25,
        bgcolor="#0F3460",
        border=ft.border.all(2, "#E94560"),
        padding=10,
        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
    )

    page.add(
        ft.AppBar(
            leading=ft.Icon(ft.icons.AUTO_STORIES, color="#E94560"),
            title=ft.Text("Perfect Math Cards", color="#FFFFFF", size=24, weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor="#16213E",
        ),
        ft.Column(
            [
                flashcard,
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK_IOS,
                            icon_color="#E94560",
                            on_click=lambda _: change_card(False),
                            icon_size=30,
                        ),
                        ft.IconButton(
                            icon=ft.icons.ARROW_FORWARD_IOS,
                            icon_color="#E94560",
                            on_click=lambda _: change_card(True),
                            icon_size=30,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=40,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=40,
        ),
    )

ft.app(target=main)