import flet as ft
import json
import logging
import sys

# Thiết lập logging để hiển thị trên console
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

# Đường dẫn đến file JSON chứa flashcards
JSON_PATH = r'E:\\web\\flet-app\\pages\\flashcard\\flashcards.json'

def load_flashcards():
    logging.info(f"Attempting to load flashcards from {JSON_PATH}")
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logging.info(f"Successfully loaded {len(data)} categories from JSON")
        return data
    except FileNotFoundError:
        logging.error(f"Error: File not found at {JSON_PATH}")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Error: Invalid JSON in file at {JSON_PATH}")
        return {}
    except Exception as e:
        logging.error(f"Unexpected error loading JSON: {str(e)}")
        return {}

def save_flashcards(flashcards):
    logging.info(f"Saving flashcards to {JSON_PATH}")
    try:
        with open(JSON_PATH, 'w', encoding='utf-8') as file:
            json.dump(flashcards, file, ensure_ascii=False, indent=4)
        logging.info("Successfully saved flashcards to JSON")
    except Exception as e:
        logging.error(f"Unexpected error saving JSON: {str(e)}")

def get_view(page: ft.Page):
    logging.info("Entering get_view function")
    all_flashcards = load_flashcards()
    categories = list(all_flashcards.keys())
    logging.info(f"Loaded {len(categories)} categories")

    def create_category_card(category):
        logging.debug(f"Creating card for category: {category}")
        icons = {
            "Math": ft.icons.FUNCTIONS,
            "Science": ft.icons.SCIENCE,
            "Business": ft.icons.BUSINESS_CENTER,
            "Computer": ft.icons.COMPUTER,
            "Literature": ft.icons.BOOK,
            "Language": ft.icons.TRANSLATE,
            "History": ft.icons.HISTORY_EDU,
            "Geography": ft.icons.PUBLIC,
            "Art": ft.icons.PALETTE,
            "Music": ft.icons.MUSIC_NOTE,
            "Technology": ft.icons.DEVICES,
            "Animals": ft.icons.PETS,
            "Plants": ft.icons.FOREST,
            "Food": ft.icons.FASTFOOD,
            "Colors": ft.icons.COLORIZE,
            "Weather": ft.icons.SUNNY,
        }

        return ft.Container(
            content=ft.Column([
                ft.Icon(icons.get(category, ft.icons.CATEGORY), size=48, color=ft.colors.PURPLE_900),
                ft.Text(category, size=16, weight="bold", color=ft.colors.PURPLE_900)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=150,
            height=150,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            ink=True,
            on_click=lambda _: show_flashcards(category)
        )

    def show_flashcards(category):
        logging.info(f"Showing flashcards for category: {category}")
        flashcards = all_flashcards[category]
        page.go(f"/flashcards/{category}")

    def show_create_flashcard_form():
        def save_flashcard(e):
            category = category_input.value
            title = title_input.value
            content = content_input.value
            if category not in all_flashcards:
                all_flashcards[category] = []
            all_flashcards[category].append({"title": title, "content": content})
            save_flashcards(all_flashcards)
            page.go("/flashcards/view_all")
        
        category_input = ft.TextField(label="Category")
        title_input = ft.TextField(label="Title")
        content_input = ft.TextField(label="Content", multiline=True)
        
        create_flashcard_form = ft.Column([
            category_input,
            title_input,
            content_input,
            ft.Row([
                ft.TextButton("Save", on_click=save_flashcard),
                ft.TextButton("Cancel", on_click=lambda _: page.go("/flashcards/view_all"))
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

        return create_flashcard_form

    def filter_flashcards(e):
        keyword = e.control.value.lower()
        filtered_categories = [cat for cat in categories if keyword in cat.lower()]
        category_grid.controls.clear()
        for category in filtered_categories:
            category_grid.controls.append(create_category_card(category))
        page.update()

    search_field = ft.TextField(
        label="Search flashcards",
        on_change=filter_flashcards,
        expand=False,
    )

    category_grid = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=20,
        run_spacing=20,
    )

    for category in categories:
        category_grid.controls.append(create_category_card(category))

    logging.info("Creating and returning View")
    return ft.View(
        "/flashcards/view_all",
        [
            ft.AppBar(
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color=ft.colors.WHITE,
                    on_click=lambda _: page.go("/flashcards")
                ),
                title=ft.Text("All Flashcards", color=ft.colors.WHITE, size=24, weight="bold"),
                center_title=True,
                bgcolor=ft.colors.PURPLE_900,
                actions=[
                    ft.IconButton(
                        icon=ft.icons.ADD,
                        icon_color=ft.colors.WHITE,
                        on_click=lambda _: page.add(ft.Container(
                            content=show_create_flashcard_form(),
                            padding=20,
                            bgcolor=ft.colors.WHITE,
                            expand=True,
                        ))
                    )
                ]
            ),
            ft.Container(
                content=ft.Column([
                    search_field,
                    category_grid,
                ], spacing=20),
                padding=20,
                bgcolor=ft.colors.WHITE,
                expand=True,
            )
        ],
    )

# Thêm hàm main để test
# def main(page: ft.Page):
#     try:
#         logging.info("Starting main function")
#         page.title = "Flashcards App"
#         view = get_view(page)
#         page.views.append(view)
#         page.update()
#         logging.info("View added successfully")
#     except Exception as e:
#         logging.error(f"Error in main function: {str(e)}")

# if __name__ == "__main__":
#     logging.info("Starting application")
#     ft.app(target=main)