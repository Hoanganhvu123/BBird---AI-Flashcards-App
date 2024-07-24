import flet as ft
from pages import home, aitutor, profile, quizz, start
import sys
import os
from flet import (
    AppBar, ElevatedButton, View, Text, Column, Container, Row, colors, Page, Icon, icons, IconButton, GridView
)

import warnings
warnings.filterwarnings("ignore")


def get_view(page: Page):
    search_results = ft.Column()

    def update_search_results(e):
        query = e.control.value.lower()
        search_results.controls.clear()
        if query:
            search_results.controls.append(
                ft.ListTile(
                    title=ft.Text("Flash Card"),
                    on_click=lambda _: page.go("/flashcards")
                )
            )
        search_results.update()

    def create_category_card(icon, text):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=40, color="#4A148C"),  # Thay đổi màu icon
                ft.Text(text, size=14, weight="bold", color="#4A148C")  # Thay đổi màu text
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            width=150,  # Điều chỉnh kích thước
            height=150,  # Điều chỉnh kích thước
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            padding=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=4,
                color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )

    return ft.View(
        "/flashcards",
        [
            ft.AppBar(
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color=colors.PURPLE_900,
                    on_click=lambda _: page.go("/home")
                ),
                title=Text("Flashcards", color=colors.WHITE, size=24, weight="bold"),
                center_title=True,
                bgcolor=ft.colors.PURPLE_900,
                toolbar_height=60,
            ),
            ft.Container(
                content=ft.Column([
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
                    ft.Text("Search Flashcards", size=24, weight="bold", color="#4A148C"),  # Thay đổi màu text
                    ft.Text("It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout.", 
                            size=14, color=ft.colors.BLACK54),
                    ft.Container(
                        content=ft.TextField(
                            hint_text="Search Here",
                            on_change=update_search_results,
                            prefix_icon=ft.icons.SEARCH,
                            border_color="#4A148C",  # Thay đổi màu border
                            focused_border_color="#4A148C",  # Thay đổi màu border khi focus
                            bgcolor=ft.colors.WHITE,
                            border_radius=30,
                        ),
                        padding=ft.padding.only(top=20, bottom=20)
                    ),
                    search_results,
                    ft.Row([
                        ft.Text("Flashcard Categories", size=20, weight="bold", color="#4A148C"),  # Thay đổi màu text
                        ft.ElevatedButton(
                            "View All",
                            style=ft.ButtonStyle(
                                bgcolor="#4A148C",  # Thay đổi màu background button
                                color=ft.colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=20),
                            )
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.GridView(
                        expand=1,
                        runs_count=2,
                        max_extent=120,
                        spacing=30,  # Tăng giá trị spacing để tăng khoảng cách theo chiều ngang
                        run_spacing=20,  # Tăng giá trị run_spacing để tăng khoảng cách theo chiều dọc
                        child_aspect_ratio=1.0,
                        controls=[
                            create_category_card(ft.icons.FUNCTIONS, "Math"),
                            create_category_card(ft.icons.SCIENCE, "Science"),
                            create_category_card(ft.icons.BUSINESS_CENTER, "Business"),
                            create_category_card(ft.icons.COMPUTER, "Computer"),
                            create_category_card(ft.icons.BOOK, "Literature"),
                            create_category_card(ft.icons.TRANSLATE, "Language"),
                        ],
                    )
                ], spacing=20),
                padding=20,
                bgcolor="#FFFFFF",
                expand=True,  # Đảm bảo container mở rộng để hiển thị tất cả nội dung
            )
        ],
    )

def main(page: ft.Page):
    page.title = "Profile User"
    page.window_width = 400
    page.window_height = 850
    page.window_resizable = False

    def route_change(e):
        page.views.clear()
        page.views.append(get_view(page))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
