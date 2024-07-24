import flet as ft
import random
import threading
from countdown import *

imageSource = ""
imageDestination = ""
idSource = 0
idDestination = 0

width = 8
score = 0
highScore=0
seconds=15 #time in seconds
candyImages = [
    "assets/apple-fruit.png",
    "assets/papaya-fruit.png",
    "assets/orange-fruit.png",
    "assets/kiwi-fruit.png",
    "assets/watermelon-fruit.png",
    "assets/lemon-fruit.png",
]

def main(page: ft.Page):
    page.title = "Fruit Crush"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    page.window_height = 700
    page.window_width = 950
    page.window_resizable = False
    

    def checkRowForFour():
        global score
        for i in range(61):
            rowOfFour = [i, i + 1, i + 2, i + 3]
            decidedImage = squares.controls[i].image_src
            isBlank = True if squares.controls[i].image_src == "" else False
            notValid = [
                5,
                6,
                7,
                13,
                14,
                15,
                21,
                22,
                23,
                29,
                30,
                31,
                37,
                38,
                39,
                45,
                46,
                47,
                53,
                54,
                55,
            ]
            if i in notValid:
                continue
            if all(
                [
                    (squares.controls[index].image_src == decidedImage and not isBlank)
                    for index in rowOfFour
                ]
            ):
                score += 4
                score_display.value = str(score)
                for i in rowOfFour:
                    squares.controls[i].image_src = ""
        page.update()

    def checkColumnForFour():
        global score
        global width
        for i in range(40):
            columnOfFour = [i, i + width, i + width * 2, i + width * 3]
            decidedImage = squares.controls[i].image_src
            isBlank = True if squares.controls[i].image_src == "" else False
            if all(
                [
                    (squares.controls[index].image_src == decidedImage and not isBlank)
                    for index in columnOfFour
                ]
            ):
                score += 4
                score_display.value = str(score)
                for i in columnOfFour:
                    squares.controls[i].image_src = ""
        page.update()

    def checkRowForThree():
        global score
        for i in range(62):
            rowOfThree = [i, i + 1, i + 2]
            decidedImage = squares.controls[i].image_src
            isBlank = True if squares.controls[i].image_src == "" else False
            notValid = [6, 7, 14, 15, 22, 23, 30, 31, 38, 39, 46, 47, 54, 55]
            if i in notValid:
                continue
            if all(
                [
                    (squares.controls[index].image_src == decidedImage and not isBlank)
                    for index in rowOfThree
                ]
            ):
                score += 3
                score_display.value = str(score)
                for i in rowOfThree:
                    squares.controls[i].image_src = ""
        page.update()

    def checkColumnForThree():
        global score
        global width
        for i in range(48):
            columnForThree = [i, i + width, i + width * 2]
            decidedImage = squares.controls[i].image_src
            isBlank = True if squares.controls[i].image_src == "" else False
            if all(
                [
                    (squares.controls[index].image_src == decidedImage and not isBlank)
                    for index in columnForThree
                ]
            ):
                score += 3
                score_display.value = str(score)
                for i in columnForThree:
                    squares.controls[i].image_src = ""
        page.update()

    def moveIntoSquareBelow():
        global width
        # drop candies once some have been cleared
        for i in range(56):
            if squares.controls[i + width].image_src == "":
                squares.controls[i + width].image_src = squares.controls[i].image_src
                squares.controls[i].image_src = ""
                firstRow = [0, 1, 2, 3, 4, 5, 6, 7]
                isFirstRow = True if i in firstRow else False
                if isFirstRow and squares.controls[i].image_src == "":
                    randomImage = random.choice(candyImages)
                    squares.controls[i].image_src = randomImage
        page.update()

    def check_infinite():
        checkRowForFour()
        checkColumnForFour()
        checkRowForThree()
        checkColumnForThree()
        moveIntoSquareBelow()

    def setInterval(func, time):
        e = threading.Event()
        while not e.wait(time):
            func()

    def exchange():
        global imageSource
        global imageDestination
        global idSource
        global idDestination
        global width
        # Is a valid move?
        validMoves = [idSource - 1, idSource - width, idSource + 1, idSource + width]
        if idDestination in validMoves:  # To move
            squares.controls[idDestination].image_src = imageSource
            squares.controls[idSource].image_src = imageDestination
            squares.controls[idDestination].update()
            squares.controls[idSource].update()

        squares.controls[idSource].bgcolor = ""
        squares.controls[idDestination].bgcolor = ""
        squares.controls[idDestination].update()
        squares.controls[idSource].update()
        imageSource = ""
        imageDestination = ""
        idSource = 0
        idDestination = 0

    def clickCandy(e):
        global imageSource
        global imageDestination
        global idSource
        global idDestination
        e.control.bgcolor = "black54"
        e.control.update()
        if imageSource == "":
            imageSource = e.control.image_src
            idSource = e.control.key
        else:
            imageDestination = e.control.image_src
            idDestination = e.control.key
            exchange()

    def fillSquares(): 
        for i in range(width * width):
            randomImage = random.choice(candyImages)
            square = ft.Container(
                key=i,
                image_src=randomImage,
                width=50,
                height=50,
                border_radius=5,
                on_click=clickCandy,
            )
            squares.controls.append(square)
        
    def close_stargame(e):
        dlg_startgame.open = False
        dlg_startgame.update()
        countdown.start()
        setInterval(check_infinite, 0.10)
        page.update()

    def end_game():
        global score
        global highScore
        if score>highScore:
            highScore=score
            highscore_display.value=str(score)
            result=f"New Score: {score}"
        else:
            result=f"Score: {score}"
        page.dialog=dlg_endgame
        dlg_endgame.content.value=f"{result}"
        dlg_endgame.open=True
        page.update()
    
    def new_game(e):
        global score
        global seconds
        score=0
        page.dialog=dlg_endgame
        dlg_endgame.open=False
        dlg_endgame.update()
        countdown.reset(seconds)
        score_display.value="0"
        squares.controls.clear()
        fillSquares()
        page.update()
        page.dialog=dlg_startgame
        dlg_startgame.open=True
        page.update()

#************ UI Game ************
    dlg_startgame = ft.AlertDialog(
        modal=True,
        title=ft.Text(value="How to play", text_align=ft.TextAlign.CENTER,weight=ft.FontWeight.BOLD),
        content=ft.Image(src="assets/Tutorial.png", width=300, height=200),
        actions=[
            ft.TextButton("Play", on_click=close_stargame),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    dlg_endgame = ft.AlertDialog(
        modal=True,
        title=ft.Text(value="Game Over", text_align=ft.TextAlign.CENTER,weight=ft.FontWeight.BOLD),
        content=ft.Text(value="", text_align=ft.TextAlign.CENTER,weight=ft.FontWeight.BOLD),
        actions=[
            ft.TextButton("Replay", on_click=new_game),
            ft.TextButton("Exit", on_click=lambda e: page.window_destroy()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    score_display = ft.Text("0", size=30, weight=ft.FontWeight.BOLD)
    highscore_display= ft.Text("0",size=18,weight=ft.FontWeight.BOLD,)
    squares = ft.GridView(
            expand=None,
            runs_count=8,
            max_extent=70,
            child_aspect_ratio=1.0,
            spacing=0,
            run_spacing=0,
            width=560,
            height=560,
        )
    countdown= Countdown(seconds,end_game) 
    page.dialog=dlg_startgame
    dlg_startgame.open=True
    fillSquares()
    page.add(
        ft.Container(
            width=page.width,
            height=page.height,
            padding=20,
            image_src="assets/background.png",
            image_fit=ft.ImageFit.FILL,
            alignment=ft.alignment.center,
            content=ft.Row(
                width=900,
                height=700,
                controls=[
                    ft.Column(
                        [
                            ft.Container(
                                border=ft.border.all(3, "white54"),
                                border_radius=10,
                                width=150,
                                height=130,
                                bgcolor=ft.colors.TEAL,
                                content=ft.Column(
                                    [
                                        ft.Text(
                                            "Time", size=25, weight=ft.FontWeight.BOLD
                                        ),
                                        countdown,
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                alignment=ft.alignment.center,
                            ),
                            ft.Container(
                                border=ft.border.all(3, "white54"),
                                border_radius=10,
                                width=180,
                                height=160,
                                bgcolor=ft.colors.PINK_ACCENT,
                                content=ft.Column(
                                    [
                                       ft.Row([
                                           ft.Text("HighScore:",size=18,weight=ft.FontWeight.BOLD,),
                                           highscore_display,
                                       ],alignment=ft.MainAxisAlignment.CENTER),
                                        ft.Text(
                                            "Score", size=30, weight=ft.FontWeight.BOLD
                                        ),
                                        score_display,
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                alignment=ft.alignment.center,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    ft.Container(width=100),
                    ft.Container(
                        width=580,
                        height=580,
                        border_radius=10,
                        bgcolor=ft.colors.LIGHT_BLUE_300,
                        content=squares,
                        alignment=ft.alignment.center,
                    ),
                ],
            ),
        )
    )
    
if __name__ == "__main__":
    ft.app(target=main)
