import flet as ft
from flet import Page, ThemeMode, colors
from pages import home, aitutor, profile, quizz, start
from pages.flashcard import flashcards_view, flashcard_detail_view
from pages.game import hehe
from pages.game.game_type.hangging_man.play import get_hangging_man_view

import warnings
warnings.filterwarnings("ignore")

def main(page: Page):
    print("Starting the application...")
    page.title = "Flashcards App"


    # page.theme_mode = ThemeMode.LIGHT
    # page.theme = ft.Theme(color_scheme_seed=colors.PURPLE_900)
    # page.dark_theme = ft.Theme(color_scheme_seed=colors.PURPLE_900)

    # Thiết lập kích thước cửa sổ cố định
    page.window_width = 400
    page.window_height = 820
    page.window_resizable = False
    page.theme_mode = "dark"

    def route_change(e):
        print(f"Route changed to: {page.route}")
        page.views.clear()

        if page.route == "/":
            page.views.append(start.get_view(page))
        elif page.route == "/home":
            page.views.append(home.get_view(page))
        elif page.route == "/flashcards":
            page.views.append(flashcards_view.get_view(page))
        elif page.route == "/quizz":
            page.views.append(quizz.get_view(page))
        elif page.route == "/aitutor":
            page.views.append(aitutor.get_view(page))
        elif page.route == "/game":
            page.views.append(hehe.get_view(page))
        elif page.route == "/profile_user":
            page.views.append(profile.get_view(page))
            page.update()
        elif page.route.startswith("/flashcards/"):
            category = page.route.split("/")[-1]
            page.views.append(flashcard_detail_view.get_flashcard_detail_view(page, category))
        elif page.route == "/game/hangging_man":
            page.views.append(get_hangging_man_view(page))
        elif page.route == "/game/fruit_crush":
            pass # Xử lý route cho Fruit Crush
        elif page.route == "/game/memory_game":
            pass # Xử lý route cho Memory Game
        
        page.update()


    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)