import flet as ft
from flet import (
    AppBar, ElevatedButton, View, Text, Column, Container, Row, colors, Page, Icon, icons, IconButton
)

def get_view(page: Page):
    is_dark = page.theme_mode == ft.ThemeMode.DARK

    def get_container(icon, title, description, color, route):
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Icon(name=icon, color=color, size=40),
                        padding=ft.padding.only(right=15, bottom=22),
                    ),
                    Column(
                        controls=[
                            Text(title, size=22, weight="bold", color=colors.WHITE if is_dark else colors.BLACK),
                            Text(description, size=16, color=colors.WHITE70 if is_dark else colors.BLACK54),
                        ],
                        spacing=5,
                        expand=True
                    ),
                    ElevatedButton(
                        "Play",
                        on_click=lambda _: page.go(route),
                        style=ft.ButtonStyle(
                            color=colors.WHITE,
                            bgcolor=color,
                            shape=ft.RoundedRectangleBorder(radius=20),
                            padding=ft.padding.symmetric(horizontal=15, vertical=10),
                        )
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.all(20),
            bgcolor=colors.BLACK if is_dark else colors.WHITE,
            border_radius=ft.border_radius.all(20),
            margin=ft.margin.only(bottom=20),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.colors.with_opacity(0.4, ft.colors.WHITE if is_dark else ft.colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
        )

    return View(
        "/game",
        [
            AppBar(
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color="#FFFFFF",
                    on_click=lambda _: page.go("/home")
                ),
                title=Text("Games", color=colors.WHITE, size=28, weight="bold"),
                bgcolor=colors.PURPLE_900,
                center_title=True,
                toolbar_height=60,
            ),
            Container(
                content=Column(
                    controls=[
                        get_container(icons.PERSON_OUTLINE, "Hanging Man", "Guess the word before it's too late!", "#6A0DAD", "/game/hangging_man"),
                        get_container(icons.APPLE, "Fruit Crush", "Match fruits to score points!", "#FF4136", "/game/fruit_crush"),
                        get_container(icons.MEMORY, "Memory Game", "Test your memory by matching pairs!", "#FF851B", "/game/memory_game"),
                    ],
                    spacing=20,
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
                padding=ft.padding.symmetric(horizontal=20, vertical=30),
                bgcolor=colors.BLACK if is_dark else colors.WHITE,
                expand=True,
            )
        ],
    )

# Phần main có thể giữ nguyên hoặc điều chỉnh như sau:
# def main(page: Page):
#     page.title = "Game Menu"
#     page.window_width = 400
#     page.window_height = 850
#     page.window_resizable = False
#     page.theme_mode = ft.ThemeMode.LIGHT  # hoặc DARK tùy theo mong muốn

#     def route_change(e):
#         page.views.clear()
#         page.views.append(get_view(page))
#         page.update()

#     page.on_route_change = route_change
#     page.go(page.route)

# ft.app(target=main)