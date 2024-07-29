import flet as ft
import random
import os
import json
import re
import logging
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

# Initialize AI model
os.environ['GOOGLE_API_KEY'] = "AIzaSyCvYf_U35Yk_kEuKJRGWFkfc5-oGS0Cmi0"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=1)

# Define prompt for generating questions
question_template = """
Generate a Hangman word and provide a very general hint. Use common words at B1 English level. The hint should be broad and simple.

Rules:
1. Words must be common nouns at B1 level.
2. Hints should be very general, using simple B1 vocabulary.
3. Avoid specific features in hints.

Examples:
1. Word: "dog", Hint: "An animal"
2. Word: "car", Hint: "A thing for travel"
3. Word: "book", Hint: "An object for learning"
4. Word: "water", Hint: "Something we drink"
5. Word: "friend", Hint: "A person we like"

The response should be in JSON format as follows:
{{
    "word": "The B1 level word to guess (a single word, no spaces)",
    "hint": "A simple, general hint using B1 level vocabulary"
}}
"""
question_prompt = ChatPromptTemplate.from_template(question_template)

def generate_word_and_hint() -> Dict[str, Any]:
    try:
        chain = question_prompt | llm
        result = chain.invoke({})
        result_content = result.content if hasattr(result, 'content') else str(result)
        logging.info(f"Generated result: {result_content}")
        
        result_content = re.sub(r'^```json\s*|\s*```$', '', result_content.strip())
        
        parsed_result = json.loads(result_content)
        return parsed_result
        
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON: {str(e)}")
        logging.error(f"Problematic JSON: {result_content}")
        return {"word": "ERROR", "hint": "Unable to generate hint"}
    except Exception as e:
        logging.error(f"Error generating word and hint: {str(e)}")
        return {"word": "ERROR", "hint": "Error occurred"}

# Global variables
word = ""
spaces = []
lives = 6

hangman_pics = [
    "hangman_0.png", "hangman_1.png", "hangman_2.png", "hangman_3.png", "hangman_4.png", "hangman_5.png", "hangman_6.png",
]

def get_hangging_man_view(page: ft.Page):
    global word, spaces, lives
    
    def generatespaces(word):
        return [ft.Text(value=i, size=35, weight=ft.FontWeight.BOLD) for i in word]

    def show_win_dialog():
        win_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Congratulations!"),
            content=ft.Text(f"You've guessed the word correctly! The word was: {word}"),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog),
                ft.TextButton("Continue", on_click=new_game),
            ],
        )
        page.dialog = win_dialog
        win_dialog.open = True
        page.update()

    def show_lose_dialog():
        lose_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Game Over"),
            content=ft.Text(f"You've run out of lives. The word was: {word}"),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog),
                ft.TextButton("Try Again", on_click=new_game),
            ],
        )
        page.dialog = lose_dialog
        lose_dialog.open = True
        page.update()

    def close_dialog(e):
        page.dialog.open = False
        page.update()

    def new_game(e=None):
        global word, spaces, lives
        if page.dialog:
            page.dialog.open = False
        lives = 6
        result = generate_word_and_hint()
        word = result["word"].upper()
        spaces = ["_"] * len(word)
        row_spaces.controls = generatespaces(spaces)
        hangman_image.src = f"E:\\web\\flet-app\\pages\\game\\game_type\\hangging_man\\assets\\{hangman_pics[6-lives]}"
        hint_text.value = f"Hint: {result['hint']}"
        page.update()

    def check_letter(e):
        global lives
        key_pressed = e.control.text
        existe_letra = False
        for idx, caracter in enumerate(word):
            if caracter == key_pressed:
                spaces[idx] = key_pressed
                existe_letra = True
        row_spaces.controls = generatespaces(spaces)
        if not existe_letra:
            lives -= 1
            hangman_image.src = f"E:\\web\\flet-app\\pages\\game\\game_type\\hangging_man\\assets\\{hangman_pics[6-lives]}"
        if "_" not in spaces:
            show_win_dialog()
        elif lives == 0:
            show_lose_dialog()
        page.update()

    def on_hover(e):
        e.control.bgcolor = "BLUE300" if e.data == "true" else "AMBER"
        e.control.update()

    def keyboard_items():
        return [
            ft.Container(
                content=ft.TextButton(
                    text=i,
                    on_click=check_letter,
                    style=ft.ButtonStyle(color=ft.colors.BLACK),
                ),
                width=45,
                height=45,
                bgcolor=ft.colors.AMBER,
                border_radius=ft.border_radius.all(5),
                on_hover=on_hover,
            ) for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ]

    back_button = ft.TextButton(
        text="Back",
        on_click=lambda _: page.go("/game"),
    )

    title = ft.Text(
        value="Guess the Word", size=35, text_align=ft.TextAlign.CENTER
    )
    row_spaces = ft.Row(
        controls=[],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    hangman_image = ft.Image(
        src=f"E:\\web\\flet-app\\pages\\game\\game_type\\hangging_man\\assets\\{hangman_pics[6]}",
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )
    hint_text = ft.Text(
        value="Hint: ", size=20, color=ft.colors.BLUE, text_align=ft.TextAlign.CENTER
    )

    keyboard = ft.Row(
        wrap=True,
        spacing=5,
        run_spacing=6,
        controls=keyboard_items(),
        width=500,
    )

    reset_button = ft.ElevatedButton(
        text="Reset Game",
        on_click=new_game,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE,
        )
    )

    container_main = ft.Container(
        width=500,
        height=800,
        padding=10,
        content=ft.Column(
            [
                back_button,
                title,
                row_spaces,
                ft.Container(height=5),
                hangman_image,
                hint_text,
                ft.Container(height=5),
                keyboard,
                ft.Container(height=10),
                reset_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
    page.theme_mode = "light"

    # Initialize game after adding controls to the page
    page.add(container_main)
    new_game()

    return ft.View(
        "/game/hangging_man",
        [container_main],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

# def main(page: ft.Page):
#     page.title = "Hangman Game"
#     page.window.width = 400
#     page.window.height = 850
#     page.window.resizable = False

#     def route_change(route):
#         page.views.clear()
#         page.views.append(get_hangging_man_view(page))
#         page.update()

#     page.on_route_change = route_change
#     page.go('/game')

# ft.app(target=main)