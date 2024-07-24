import flet as ft

def get_view(page: ft.Page):
    search_results = ft.Column()

    def update_search_results(e):
        query = e.control.value.lower()
        search_results.controls.clear()
        
        if query.startswith('f'):
            search_results.controls.append(
                ft.ListTile(
                    title=ft.Text("Flash Card", color=page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or ft.colors.BLACK),
                    on_click=lambda _: page.go("/flashcards")
                )
            )
        search_results.update()

    def create_card(icon, text, route, icon_color, text_color):
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(icon, size=40, color=icon_color),
                    alignment=ft.alignment.center,
                    width=150,
                ),
                ft.Container(
                    content=ft.Text(text, size=16, weight=ft.FontWeight.BOLD, color=text_color),
                    alignment=ft.alignment.center,
                    width=150,
                )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            width=150,
            height=150,
            border_radius=15,
            bgcolor=page.theme_mode == ft.ThemeMode.DARK and ft.colors.BLACK87 or ft.colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=4,
                color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
            on_click=lambda _: page.go(route)
        )

    return ft.View(
        "/home",
        controls=[
            # Thanh tiêu đề với nền tím và góc bo tròn
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Image(
                                src="E:\\web\\flet-app\\assets\\images\\bbird.png",  # Đường dẫn đến ảnh đại diện của người dùng
                                fit=ft.ImageFit.COVER,
                                width=60,
                                height=60,
                            ),
                            width=60,
                            height=60,
                            border_radius=30,
                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        ),
                        ft.Text("Hello, Team3!", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=ft.padding.all(10),
                border_radius=ft.border_radius.only(bottom_left=30, bottom_right=30),
                bgcolor=ft.colors.PURPLE_900,
                alignment=ft.alignment.center,
            ),
            
            # Ô tìm kiếm
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.TextField(
                                label="Search Here",
                                on_change=update_search_results,
                                prefix_icon=ft.icons.SEARCH,
                                border_color=page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C",
                                focused_border_color=page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C",
                                bgcolor=page.theme_mode == ft.ThemeMode.DARK and ft.colors.BLACK87 or ft.colors.WHITE,
                                color=page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or ft.colors.BLACK,
                                border_radius=30,
                            ),
                            padding=ft.padding.only(top=20, bottom=30)
                        ),
                        search_results,

                        # Phần hiển thị các khóa học
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Text("Explore All Courses", size=22, weight=ft.FontWeight.BOLD, color=page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C"),
                                            ft.ElevatedButton(
                                                "View All",
                                                style=ft.ButtonStyle(
                                                    bgcolor="#4A148C",
                                                    color=ft.colors.WHITE,
                                                    shape=ft.RoundedRectangleBorder(radius=30),
                                                )
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    ft.Row(
                                        controls=[
                                            create_card(ft.icons.SCHOOL, "Flash Card", "/flashcards", page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C", page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C"),  # Tím
                                            create_card(ft.icons.QUIZ, "Quiz", "/quizz", page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C", page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C"),  # Tím
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    ft.Row(
                                        controls=[
                                            create_card(ft.icons.SMART_TOY, "AI Tutor", "/aitutor", page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C", page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C"),  # Tím
                                            create_card(ft.icons.SPORTS_ESPORTS, "Games", "/game", page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C", page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C"),  # Tím
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                ],
                                spacing=25,
                            ),
                            padding=ft.padding.only(top=20, bottom=20),
                        ),
                    ],
                    spacing=15
                ),
                padding=25,
                bgcolor=page.theme_mode == ft.ThemeMode.DARK and ft.colors.BLACK87 or ft.colors.WHITE,  # Nền thay đổi theo theme
            ),

            # Thanh điều hướng dưới cùng
            ft.Stack(
                [
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.HOME_ROUNDED,
                                    icon_color=page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C",  # Tím
                                    icon_size=28,
                                    on_click=lambda _: page.go("/home")
                                ),
                                ft.IconButton(
                                    icon=ft.icons.SEARCH_ROUNDED,
                                    icon_color=page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C",  # Tím
                                    icon_size=28,
                                ),
                                ft.IconButton(
                                    icon=ft.icons.FAVORITE_ROUNDED,
                                    icon_color=page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C",  # Tím
                                    icon_size=28,
                                ),
                                ft.IconButton(
                                    icon=ft.icons.PERSON_ROUNDED,
                                    icon_color=page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C",  # Tím
                                    icon_size=28,
                                    on_click=lambda _: page.go("/profile_user")
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        ),
                        bgcolor=page.theme_mode == ft.ThemeMode.DARK and ft.colors.BLACK87 or ft.colors.WHITE,  # Nền thay đổi theo theme
                        border=ft.border.only(top=ft.BorderSide(1, page.theme_mode == ft.ThemeMode.DARK and ft.colors.WHITE or "#4A148C")),
                        padding=ft.padding.only(top=10, left=20, right=20, bottom=25),
                        height=70,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.FloatingActionButton(
                            content=ft.Icon(ft.icons.ADD_ROUNDED, size=30, color=ft.colors.WHITE),
                            bgcolor="#4A148C",
                            shape=ft.CircleBorder(),
                            width=65,
                            height=65,
                            on_click=lambda _: page.go("/add")
                        ),
                        alignment=ft.alignment.bottom_center,
                        offset=ft.Offset(0, -30),
                    ),
                ]
            )
        ],
        padding=0,
        bgcolor=page.theme_mode == ft.ThemeMode.DARK and ft.colors.BLACK87 or ft.colors.WHITE,  # Nền thay đổi theo theme
    )


# def main(page: ft.Page):
#     page.title = "Profile User"
#     page.window.width = 400
#     page.window.height = 850
#     page.window.resizable = False
#     page.theme_mode = "dark"

#     def route_change(e):
#         page.views.clear()
#         page.views.append(get_view(page))
#         page.update()

#     page.on_route_change = route_change
#     page.go(page.route)

# ft.app(target=main)
