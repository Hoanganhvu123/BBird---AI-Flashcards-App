import flet as ft
import random

animals = [
    "CAT", "DOG", "BEE", "EAGLE", "SPIDER", "WASP", "WHALE", "BUFFALO", "DONKEY", "HORSE",
    "SQUID", "CAMEL", "CHAMELEON", "CRAB", "ZEBRA", "CROCODILE", "RABBIT", "DOLPHIN", "ELEPHANT",
    "SCORPION", "SPARROW", "FALCON", "HIPPO", "ANT", "JAGUAR", "LION", "WOLF", "BUTTERFLY", "BEAR", "BIRD",
]
hangman_pics = [
    "hangman_0.png", "hangman_1.png", "hangman_2.png", "hangman_3.png", "hangman_4.png", "hangman_5.png", "hangman_6.png",
]

word = random.choice(animals)
spaces = ["_"] * len(word)
lives = 6

def get_hangging_man_view(page: ft.Page):
    def generatespaces(word):
        items = []
        for i in word:
            items.append(
                ft.Text(
                    value=i,
                    size=35,
                    weight=ft.FontWeight.BOLD,
                )
            )
        return items

    def close_dlg(e):
        win.open = False
        lose.open = False
        page.update()

    def new_game(e):
        global word
        global spaces
        global lives
        lose.open = False
        win.open = False
        page.update()
        lives = 6
        word = random.choice(animals)
        spaces = ["_"] * len(word)
        row_spaces.controls = generatespaces(spaces)
        row_spaces.update()
        hangman_image.src = f"E:\\web\\flet-app\\pages\\game\\game_type\\hangging_man\\assets\\{hangman_pics[6-lives]}"
        hangman_image.update()

    def check_letter(e):
        global lives
        key_pressed = e.control.text
        existe_letra = False
        for idx, caracter in enumerate(word):
            if caracter == key_pressed:
                spaces[idx] = key_pressed
                existe_letra = True
                row_spaces.controls = generatespaces(spaces)
                row_spaces.update()
        if not existe_letra:
            lives = lives - 1
            hangman_image.src = f"E:\\web\\flet-app\\pages\\game\\game_type\\hangging_man\\assets\\{hangman_pics[6-lives]}"
            page.update()
        if "_" not in spaces:
            page.dialog = win
            win.open = True
            page.update()
        if lives == 0:
            page.dialog = lose
            lose.open = True
            page.update()

    def on_hover(e):
        e.control.bgcolor = "BLUE300" if e.data == "true" else "AMBER"
        e.control.update()

    def keyboard_items():
        items = []
        for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            items.append(
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
                )
            )
        return items

    win = ft.AlertDialog(
        modal=True,
        title=ft.Text("You Win!"),
        content=ft.Text("Do you want a new game?"),
        actions=[
            ft.TextButton("Yes", on_click=new_game),
            ft.TextButton("No", on_click=close_dlg),
        ],
    )
    lose = ft.AlertDialog(
        modal=True,
        title=ft.Text(f"You Lose!"),
        content=ft.Text("Do you want to try again?"),
        actions=[
            ft.TextButton("Yes", on_click=new_game),
            ft.TextButton("No", on_click=close_dlg),
        ],
    )

    # Nút Back
    back_button = ft.TextButton(
        text="Back",
        on_click=lambda _: page.go("/game"),
    )

    # On Load App
    title = ft.Text(
        value="The word is an Animal", size=35, text_align=ft.TextAlign.CENTER
    )
    row_spaces = ft.Row(
        controls=generatespaces(spaces),
        alignment=ft.MainAxisAlignment.CENTER,
    )
    hangman_image = ft.Image(
        src=f"E:\\web\\flet-app\\pages\\game\\game_type\\hangging_man\\assets\\{hangman_pics[1-lives]}",
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )
    cocodrile_image = ft.Image(
        src=f"E:\\web\\flet-app\\pages\\game\\game_type\\hangging_man\\assets\\cocodrile.png", width=200, height=50, fit=ft.ImageFit.CONTAIN
    )

    keyboard = ft.Row(
        wrap=True,
        spacing=5,
        run_spacing=6,
        controls=keyboard_items(),
        width=500,
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
                cocodrile_image,
                ft.Container(height=5),
                keyboard,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
    page.theme_mode = "light"

    return ft.View(
        "/game/hangging_man",
        [container_main],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )



# def main(page: ft.Page):
#     page.title = "Hangman Game"
#     # page.theme_mode = "light"
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