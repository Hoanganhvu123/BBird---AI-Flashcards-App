import flet as ft

def get_view(page: ft.Page):
    search_results = ft.Column()

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
                            on_click=lambda _: page.go("/flashcards/view_all"),  # Updated to route to the new view
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
                ], spacing=20),
                padding=20,
                bgcolor=ft.colors.BLACK87 if page.theme_mode == ft.ThemeMode.DARK else ft.colors.WHITE,
                expand=True,
            )
        ],
    )
