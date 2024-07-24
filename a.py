import os
import flet as ft
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

def get_view(page: ft.Page):
    search_results = ft.Column()
    flashcard_list = ft.Column()

    def update_search_results(e):
        query = e.control.value.lower()
        search_results.controls.clear()
        if query:
            search_results.controls.append(
                ft.ListTile(
                    title=ft.Text("Flash Card", color=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.BLACK),
                    on_click=lambda _: page.go("/flashcards")
                )
            )
        search_results.update()

    def create_category_card(icon, text):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=40, color=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else "#4A148C"),
                ft.Text(text, size=14, weight="bold", color=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else "#4A148C")
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            width=150,
            height=150,
            border_radius=10,
            bgcolor=ft.colors.BLACK87 if page.theme_mode == ft.ThemeMode.DARK else ft.colors.WHITE,
            padding=10,
            ink=True,
            on_click=lambda _: page.go(f"/flashcards/{text}")
        )

    def create_add_button():
        return ft.IconButton(
            icon=ft.icons.ADD,
            icon_color=ft.colors.WHITE,
            on_click=show_flashcard_dialog,
            tooltip="Add new flashcard",
        )

    def show_flashcard_dialog(e):
        def close_dialog(e):
            page.dialog.open = False
            page.update()

        def add_flashcard(e):
            if not term_input.value or not definition_input.value or not example_input.value:
                show_snack_bar("Please fill in all fields.")
                return

            flashcard_list.controls.append(
                ft.ListTile(
                    title=ft.Text(term_input.value, weight="bold"),
                    subtitle=ft.Text(definition_input.value),
                    trailing=ft.Text(f"Example: {example_input.value}")
                )
            )
            flashcard_list.update()
            close_dialog(e)

        term_input = ft.TextField(
            label="Term",
            color=ft.colors.BLACK if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
            width=200  # Adjust width as needed
        )
        definition_input = ft.TextField(
            label="Definition",
            multiline=True,
            color=ft.colors.BLACK if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
            width=200  # Adjust width as needed
        )
        example_input = ft.TextField(
            label="Example",
            multiline=True,
            color=ft.colors.BLACK if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
            width=200  # Adjust width as needed
        )

        add_button = ft.ElevatedButton(
            text="Add Flashcard",
            on_click=add_flashcard,
            style=ft.ButtonStyle(
                color={"": ft.colors.WHITE},
                bgcolor={"": ft.colors.PURPLE_900},
            ),
            width=200  # Adjust width to match the TextFields
        )

        dialog_content = ft.Column([
            term_input,
            definition_input,
            example_input,
            add_button
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)  # Align contents to center

        page.dialog = ft.AlertDialog(
            title=ft.Text("Create Flashcard"),
            content=ft.Container(
                content=dialog_content,
                width=220  # Adjust width to make the dialog narrower
            ),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog.open = True
        page.update()

    def show_snack_bar(message):
        page.snack_bar = ft.SnackBar(content=ft.Text(message))
        page.snack_bar.open = True
        page.update()

    return ft.View(
        "/flashcards",
        [
            ft.AppBar(
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color=ft.colors.WHITE,
                    on_click=lambda _: page.go("/home")
                ),
                title=ft.Text("Flashcards", color=ft.colors.WHITE, size=24, weight="bold"),
                center_title=True,
                bgcolor=ft.colors.PURPLE_900,
                actions=[create_add_button()],  # Add the create button to the AppBar
                toolbar_height=60,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Image(
                                    src="E:\\web\\flet-app\\assets\\images\\bbird.png",
                                    fit=ft.ImageFit.COVER,
                                    width=60,
                                    height=60,
                                ),
                                width=60,
                                height=60,
                                border_radius=30,
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            ),
                            ft.Text("Tìm kiếm Flashcards", size=24, weight="bold", color=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else "#4A148C")
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10
                    ),
                    ft.Text("Flashcards của BBird giúp bạn dễ dàng học từ mới một cách trực quan và sinh động 📚. Hãy khám phá các chủ đề khác nhau như Toán học, Khoa học, Kinh doanh, và nhiều hơn nữa nhé 🧠",
                            size=14, color=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.BLACK54),
                    ft.Container(
                        content=ft.TextField(
                            hint_text="Search Here",
                            on_change=update_search_results,
                            prefix_icon=ft.icons.SEARCH,
                            border_color=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else "#4A148C",
                            focused_border_color=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else "#4A148C",
                            bgcolor=ft.colors.BLACK87 if page.theme_mode == ft.ThemeMode.DARK else ft.colors.WHITE,
                            color=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.colors.BLACK,
                            border_radius=30,
                        ),
                        padding=ft.padding.only(top=20, bottom=20)
                    ),
                    search_results,
                    ft.Row([
                        ft.Text("Flashcard Categories", size=20, weight="bold", color=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else "#4A148C"),
                        ft.ElevatedButton(
                            text="View All",
                            style=ft.ButtonStyle(
                                color={"": ft.colors.WHITE},
                                bgcolor={"": "#4A148C"},
                                shape={"": ft.RoundedRectangleBorder(radius=20)},
                            )
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.GridView(
                        expand=1,
                        runs_count=3,
                        max_extent=120,
                        spacing=30,
                        run_spacing=20,
                        child_aspect_ratio=1.0,
                        controls=[
                            create_category_card(ft.icons.FUNCTIONS, "Math"),
                            create_category_card(ft.icons.SCIENCE, "Science"),
                            create_category_card(ft.icons.BUSINESS_CENTER, "Business"),
                            create_category_card(ft.icons.COMPUTER, "Computer"),
                            create_category_card(ft.icons.BOOK, "Literature"),
                            create_category_card(ft.icons.TRANSLATE, "Language"),
                        ],
                    ),
                    flashcard_list,
                ], spacing=20),
                padding=20,
                bgcolor=ft.colors.BLACK87 if page.theme_mode == ft.ThemeMode.DARK else ft.colors.WHITE,
                expand=True,
            )
        ],
    )

def main(page: ft.Page):
    page.title = "Flashcard Master"
    page.window.width = 400
    page.window.height = 850
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT

    def route_change(e):
        page.views.clear()
        page.views.append(get_view(page))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
