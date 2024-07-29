import flet as ft
from flet import (
    AppBar, View, Text, Column, Container, Row, colors, Page, Icon, icons, Switch, padding, border_radius, IconButton, margin, ThemeMode
)

def get_view(page: Page):
    page.padding = 0
    page.theme = ft.Theme(color_scheme_seed=colors.PURPLE_900)
    page.theme_mode = ThemeMode.LIGHT  # Set default theme to light

    def toggle_theme(e):
        page.theme_mode = ThemeMode.DARK if page.theme_mode == ThemeMode.LIGHT else ThemeMode.LIGHT
        page.update()

    def get_icon_color():
        return colors.WHITE if page.theme_mode == ThemeMode.DARK else colors.PURPLE_900

    def get_text_color():
        return colors.WHITE if page.theme_mode == ThemeMode.DARK else colors.BLACK

    def get_bg_color():
        return colors.BLACK if page.theme_mode == ThemeMode.DARK else colors.WHITE

    return View(
        "/profile_user",
        [
            AppBar(
                leading=IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color=colors.WHITE,
                    on_click=lambda _: page.go("/home")
                ),
                title=Text("Profile", color=colors.WHITE, size=20, weight="bold"),
                bgcolor=colors.PURPLE_900,
                center_title=True,
                toolbar_height=60,
                elevation=0,
            ),
            Container(
                content=Column(
                    controls=[
                        # Profile Section
                        Container(
                            content=Row(
                                controls=[
                                    Container(
                                        content=Icon(name=icons.ACCOUNT_CIRCLE, size=60, color=colors.PURPLE_900),
                                        padding=padding.all(5),
                                        bgcolor=colors.WHITE,
                                        border_radius=border_radius.all(30),
                                    ),
                                    Container(width=15),
                                    Column(
                                        controls=[
                                            Text("Team3", size=20, weight="bold", color=get_text_color),
                                            Text("Team3@gmail.com", size=14, color=get_text_color),
                                        ],
                                        spacing=2,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            padding=padding.all(15),
                            margin=margin.only(bottom=15, top=5),
                            bgcolor=colors.with_opacity(0.05, colors.PURPLE_900),
                            border_radius=border_radius.all(10),
                        ),
                        # Preferences Section
                        Container(
                            content=Column(
                                controls=[
                                    _create_preference_row(icons.DARK_MODE, "Dark theme", Switch(value=False, on_change=toggle_theme), get_icon_color, get_text_color),
                                    _create_preference_row(icons.NOTIFICATIONS, "Notifications", IconButton(icon=icons.CHEVRON_RIGHT, icon_color=get_icon_color), get_icon_color, get_text_color),
                                    _create_preference_row(icons.LANGUAGE, "Language", IconButton(icon=icons.CHEVRON_RIGHT, icon_color=get_icon_color), get_icon_color, get_text_color),
                                    _create_preference_row(icons.SETTINGS, "Settings", IconButton(icon=icons.CHEVRON_RIGHT, icon_color=get_icon_color), get_icon_color, get_text_color),
                                ],
                                spacing=2,
                            ),
                            padding=padding.all(15),
                            border_radius=border_radius.all(10),
                            margin=margin.only(bottom=15),
                            bgcolor=colors.with_opacity(0.05, colors.PURPLE_900),
                        ),
                        # More Section
                        Container(
                            content=Column(
                                controls=[
                                    _create_preference_row(icons.DESCRIPTION, "Terms & Conditions", IconButton(icon=icons.CHEVRON_RIGHT, icon_color=get_icon_color), get_icon_color, get_text_color),
                                    _create_preference_row(icons.HELP, "Help & Support", IconButton(icon=icons.CHEVRON_RIGHT, icon_color=get_icon_color), get_icon_color, get_text_color),
                                ],
                                spacing=2,
                            ),
                            padding=padding.all(15),
                            border_radius=border_radius.all(10),
                            margin=margin.only(bottom=15),
                            bgcolor=colors.with_opacity(0.05, colors.PURPLE_900),
                        ),
                    ],
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=padding.symmetric(horizontal=15, vertical=10),
                expand=True,
                bgcolor=get_bg_color,
            ) 
        ],
    )

def _create_preference_row(icon, text, action_control, get_icon_color, get_text_color):
    return Container(
        content=Row(
            controls=[
                Icon(name=icon, size=20, color=get_icon_color),
                Container(width=10),
                Text(text, expand=True, color=get_text_color, size=14),
                action_control,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=padding.symmetric(vertical=12, horizontal=5),
    )

# def main(page: ft.Page):
#     page.title = "Profile User"
#     page.window_width = 400
#     page.window_height = 820
#     page.window_resizable = False

#     def route_change(e):
#         page.views.clear()
#         page.views.append(get_view(page))
#         page.update()

#     page.on_route_change = route_change
#     page.go(page.route)

# ft.app(target=main)