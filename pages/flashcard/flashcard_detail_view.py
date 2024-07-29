import flet as ft
import json
import os

def load_flashcards():
    json_path = r'E:\web\flet-app\pages\flashcard\flashcards.json'
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {json_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file at {json_path}")
        return {}

def get_flashcard_detail_view(page: ft.Page, category: str):
    flashcards = load_flashcards()
    flashcard_list = flashcards.get(category, [])
    current_card_index = 0

    def flip_card(_):
        if flashcard.data == "question":
            flashcard.content = answer_text
            flashcard.data = "answer"
        else:
            flashcard.content = question_text
            flashcard.data = "question"
        page.update()

    def change_card(forward: bool):
        nonlocal current_card_index
        if forward and current_card_index < len(flashcard_list) - 1:
            current_card_index += 1
        elif not forward and current_card_index > 0:
            current_card_index -= 1
        update_card_content()

    def update_card_content():
        nonlocal current_card_index
        if flashcard_list:
            current_flashcard = flashcard_list[current_card_index]
            question_text.value = current_flashcard["question"]
            answer_text.value = current_flashcard["answer"]
            flashcard.content = question_text
            flashcard.data = "question"
            progress_text.value = f"{current_card_index + 1}/{len(flashcard_list)}"
            page.update()

    question_text = ft.Text(size=24, weight="bold", text_align=ft.TextAlign.CENTER, color=ft.colors.PURPLE_900)
    answer_text = ft.Text(size=22, text_align=ft.TextAlign.CENTER, color=ft.colors.PURPLE_900)
    
    flashcard = ft.Container(
        content=question_text,
        data="question", 
        width=340,
        height=200,
        bgcolor=ft.colors.PURPLE_100,
        border_radius=15,
        padding=20,
        alignment=ft.alignment.center,
        on_click=flip_card,
    )

    progress_text = ft.Text(color=ft.colors.PURPLE_900, weight="bold")

    def go_back(_):
        page.go("/flashcards")

    content = ft.Column(
        controls=[
            ft.Container(content=flashcard, alignment=ft.alignment.center),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.ElevatedButton(
                        text="Previous",
                        on_click=lambda _: change_card(False),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=15),
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.PURPLE_900,
                        ),
                    ),
                    ft.ElevatedButton(
                        text="Next",
                        on_click=lambda _: change_card(True),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=15),
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.PURPLE_900,
                        ),
                    ),
                ],
            ),
            ft.Container(content=progress_text, alignment=ft.alignment.center),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        spacing=20,
    )

    view = ft.View(
        route=f"/flashcards/{category}",
        bgcolor=ft.colors.WHITE,
        appbar=ft.AppBar(
            title=ft.Text(f"{category} Flashcards"),
            leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back),
            bgcolor=ft.colors.PURPLE_900,
            color=ft.colors.WHITE,
        ),
        padding=ft.padding.all(20),
        controls=[content],
    )

    # Khởi tạo nội dung flashcard ngay khi view được tạo
    update_card_content()

    return view