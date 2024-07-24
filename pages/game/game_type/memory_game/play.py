import flet as ft
import random

class MemoryGame(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.items = 0
        self.card_1 = None
        self.card_2 = None
        self.correct_pairs = 0
        self.timer = 0
        self.timer_running = False
        self.difficulty = "easy"
        self.animals = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯"]
        self.game_started = False

    def build(self):
        self.title = ft.Text("Memory Game", size=40, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER)
        self.timer_text = ft.Text("00:00", size=24, color=ft.colors.WHITE)
        self.game_grid = ft.GridView(
            expand=1,
            max_extent=70,
            child_aspect_ratio=1,
            spacing=5,
            run_spacing=5,
            visible=False
        )
        self.difficulty_radio = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="easy", label="Easy", fill_color=ft.colors.WHITE),
                ft.Radio(value="medium", label="Medium", fill_color=ft.colors.WHITE),
                ft.Radio(value="hard", label="Hard", fill_color=ft.colors.WHITE),
            ]),
            value="easy",
        )
        self.start_button = ft.ElevatedButton("Start Game", on_click=self.start_game, style=ft.ButtonStyle(color=ft.colors.BLACK, bgcolor=ft.colors.WHITE))

        return ft.Container(
            width=400,
            height=800,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#6A1B9A", "#E91E63"]
            ),
            content=ft.Column([
                self.title,
                ft.Container(height=20),
                self.timer_text,
                ft.Container(height=20),
                self.game_grid,
                ft.Container(height=20),
                self.difficulty_radio,
                ft.Container(height=20),
                self.start_button,
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def start_game(self, e):
        if not self.game_started:
            self.difficulty = self.difficulty_radio.value
            self.items = 6 if self.difficulty == "easy" else 12 if self.difficulty == "medium" else 20
            self.correct_pairs = 0
            self.timer = 0
            self.timer_running = True
            self.update_timer()
            self.create_game_grid()
            self.difficulty_radio.visible = False
            self.start_button.text = "Restart Game"
            self.game_started = True
            self.game_grid.visible = True
        else:
            self.reset_game()
        self.update()

    def create_game_grid(self):
        self.game_grid.controls.clear()
        animals = random.sample(self.animals, self.items // 2) * 2
        random.shuffle(animals)
        for i, animal in enumerate(animals):
            card = ft.Container(
                content=ft.Text("?", size=30, color=ft.colors.BLACK),
                width=60,
                height=60,
                bgcolor=ft.colors.WHITE,
                border_radius=5,
                alignment=ft.alignment.center,
                data=animal,
                on_click=lambda e, i=i: self.flip_card(e, i)
            )
            self.game_grid.controls.append(card)

    def flip_card(self, e, index):
        if not self.game_started or self.card_1 and self.card_2:
            return

        e.control.content.value = e.control.data
        e.control.bgcolor = ft.colors.LIGHT_BLUE_200
        e.control.update()

        if not self.card_1:
            self.card_1 = (index, e.control)
        else:
            self.card_2 = (index, e.control)
            self.page.add_future(ft.sleep(0.5), self.check_match)

    def check_match(self, _):
        if self.card_1[1].data == self.card_2[1].data:
            self.card_1[1].bgcolor = ft.colors.GREEN_200
            self.card_2[1].bgcolor = ft.colors.GREEN_200
            self.correct_pairs += 1
            if self.correct_pairs == self.items // 2:
                self.game_over()
        else:
            self.card_1[1].content.value = "?"
            self.card_2[1].content.value = "?"
            self.card_1[1].bgcolor = ft.colors.WHITE
            self.card_2[1].bgcolor = ft.colors.WHITE

        self.card_1[1].update()
        self.card_2[1].update()
        self.card_1 = None
        self.card_2 = None

    def game_over(self):
        self.timer_running = False
        dlg = ft.AlertDialog(
            title=ft.Text("Congratulations!"),
            content=ft.Text(f"You completed the game in {self.timer_text.value}!"),
            actions=[
                ft.TextButton("Play Again", on_click=self.close_dlg_and_restart),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def close_dlg_and_restart(self, e):
        self.page.dialog.open = False
        self.page.update()
        self.reset_game()

    def reset_game(self):
        self.game_started = False
        self.difficulty_radio.visible = True
        self.start_button.text = "Start Game"
        self.game_grid.controls.clear()
        self.game_grid.visible = False
        self.timer_text.value = "00:00"
        self.timer_running = False
        self.update()

    def update_timer(self):
        if self.timer_running:
            self.timer += 1
            mins, secs = divmod(self.timer, 60)
            self.timer_text.value = f"{mins:02d}:{secs:02d}"
            self.timer_text.update()
            self.page.add_future(ft.sleep(1), self.update_timer)

def main(page: ft.Page):
    page.title = "Memory Game"
    page.window_width = 400
    page.window_height = 800
    page.window_resizable = False
    page.add(MemoryGame())

ft.app(target=main)