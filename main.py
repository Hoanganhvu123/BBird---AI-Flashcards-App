import flet as ft
from flet import Page, ThemeMode, colors
from pages import home, aitutor, profile, quizz, start
from pages.flashcard import flashcards_view, flashcard_detail_view, flashcard_view_all 
from pages.game import hehe
from pages.game.game_type.hangging_man.play import get_hangging_man_view

import warnings
import logging

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

ROUTES = {
    "/": start.get_view,
    "/home": home.get_view,
    "/flashcards": flashcards_view.get_view,
    "/flashcards/view_all": flashcard_view_all.get_view,
    "/quizz": quizz.get_view,
    "/aitutor": aitutor.get_view,
    "/game": hehe.get_view,
    "/profile_user": profile.get_view,
    "/game/hangging_man": get_hangging_man_view
}

def main(page: Page):
    logging.info("Starting the application...")
    
    page.title = "Flashcards App"
    page.window_width = 400
    page.window_height = 820
    page.window_resizable = False
    
    def route_change(e):
        logging.info(f"Route changed to: {page.route}")
        page.views.clear()
         
        try:
            if page.route == "/flashcards/view_all":
                logging.info("Loading view_all flashcards")
                view = flashcard_view_all.get_view(page)
                page.views.append(view)
            elif page.route.startswith("/flashcards/"):
                category = page.route.split("/")[-1]
                logging.info(f"Loading flashcards for category: {category}")
                view = flashcard_detail_view.get_flashcard_detail_view(page, category)
                page.views.append(view)
            elif page.route in ROUTES:
                logging.info(f"Loading view for route: {page.route}")
                view = ROUTES[page.route](page)
                page.views.append(view)
            else:
                logging.warning(f"Route not found: {page.route}")
                # Handle undefined routes if needed
                 
            page.update()
        except Exception as ex:
            logging.error(f"Error in route_change: {str(ex)}")
     
    def view_pop(view):
        logging.info("View popped") 
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
     
    page.on_route_change = route_change
    page.on_view_pop = view_pop
     
    if not page.route or page.route == "/":
        logging.info("Setting initial route to /home")
        page.go("/home")
    else:
        logging.info(f"Initial route is {page.route}")
        page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main)