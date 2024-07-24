import flet as ft
from flet import (
    AppBar, ElevatedButton, View, Text, Column, Container, Row, colors, Page, Icon, icons, Switch, padding, border_radius, IconButton, margin, ThemeMode
)

def get_view(page: Page):
    def toggle_theme(e):
        page.theme_mode = ThemeMode.DARK if page.theme_mode == ThemeMode.LIGHT else ThemeMode.LIGHT
        page.update()

    def get_icon_color():
        return colors.WHITE if page.theme_mode == ThemeMode.DARK else colors.PURPLE_900

    return View(
        "/profile_user",
        [
            AppBar(
                leading=IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color=colors.WHITE,
                    on_click=lambda _: page.go("/home")
                ),
                title=Text("Profile", color=colors.WHITE, size=28, weight="bold"),
                bgcolor=colors.PURPLE_900,
                center_title=True,
                toolbar_height=70,
                elevation=2,
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
                                        bgcolor=colors.WHITE70,
                                        border_radius=border_radius.all(30),
                                    ),
                                    Container(width=10),
                                    Column(
                                        controls=[
                                            Text("Team3", size=24, weight="bold"),
                                            Text("Team3@gmail.com", size=16),
                                        ],
                                        spacing=5,
                                        expand=True,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    Container(width=10),
                                    IconButton(
                                        icon=icons.EDIT,
                                        icon_size=24,
                                        icon_color=get_icon_color,
                                        tooltip="Edit Profile",
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            padding=padding.all(20),
                            border_radius=border_radius.all(10),
                            margin=margin.symmetric(vertical=10),
                        ),
                        # Preferences Section
                        Container(
                            content=Column(
                                controls=[
                                    Row(
                                        controls=[
                                            Icon(name=icons.DARK_MODE, size=32, color=get_icon_color),
                                            Container(width=10),
                                            Text("Dark theme", expand=True, color=colors.PURPLE_900),
                                            Switch(value=page.theme_mode == ThemeMode.DARK, on_change=toggle_theme),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    Container(height=10),
                                    Row(
                                        controls=[
                                            Icon(name=icons.NOTIFICATIONS, size=32, color=get_icon_color),
                                            Container(width=10),
                                            Text("Notifications", expand=True, color=colors.PURPLE_900),
                                            IconButton(icon=icons.CHEVRON_RIGHT, icon_color=get_icon_color),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    Container(height=10),
                                    Row(
                                        controls=[
                                            Icon(name=icons.LANGUAGE, size=32, color=get_icon_color),
                                            Container(width=10),
                                            Text("Language", expand=True, color=colors.PURPLE_900),
                                            IconButton(icon=icons.CHEVRON_RIGHT, icon_color=get_icon_color),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    Container(height=10),
                                    Row(
                                        controls=[
                                            Icon(name=icons.SETTINGS, size=32, color=get_icon_color),
                                            Container(width=10),
                                            Text("Settings", expand=True, color=colors.PURPLE_900),
                                            IconButton(icon=icons.CHEVRON_RIGHT, icon_color=get_icon_color),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ],
                                spacing=10,
                            ),
                            padding=padding.symmetric(vertical=10),
                            border_radius=border_radius.all(10),
                            margin=margin.only(bottom=20),
                        ),
                        # More Section
                        Container(
                            content=Column(
                                controls=[
                                    Row(
                                        controls=[
                                            Icon(name=icons.DESCRIPTION, size=32, color=get_icon_color),
                                            Container(width=10),
                                            Text("Terms & Conditions", expand=True, color=colors.PURPLE_900),
                                            IconButton(icon=icons.CHEVRON_RIGHT, icon_color=get_icon_color),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    Container(height=10),
                                    Row(
                                        controls=[
                                            Icon(name=icons.HELP, size=32, color=get_icon_color),
                                            Container(width=10),
                                            Text("Help & Support", expand=True, color=colors.PURPLE_900),
                                            IconButton(icon=icons.CHEVRON_RIGHT, icon_color=get_icon_color),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ],
                                spacing=10,
                            ),
                            padding=padding.symmetric(vertical=10),
                            border_radius=border_radius.all(10),
                            margin=margin.only(bottom=20),
                        ),
                        # Login Section
                        Row(
                            controls=[
                                ElevatedButton(
                                    "Log Out",
                                    on_click=lambda _: page.go("/home"),
                                    style=ft.ButtonStyle(
                                        color=colors.WHITE,
                                        bgcolor={"": colors.PURPLE_900, "hovered": colors.PURPLE_900},
                                        padding=padding.symmetric(vertical=12, horizontal=25),
                                        shape=ft.RoundedRectangleBorder(radius=5),
                                        elevation=2,
                                    ),
                                    expand=False,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    spacing=20,
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
                padding=padding.all(20),
                expand=True,
            ) 
        ],
    )