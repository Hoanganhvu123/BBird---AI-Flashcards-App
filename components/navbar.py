import flet as ft

def get_navbar():
    return ft.Row([
        ft.ElevatedButton("Home", on_click=lambda _: ft.get_page().go("/")),
        ft.ElevatedButton("Flashcards", on_click=lambda _: ft.get_page().go("/flashcards")),
    ])
