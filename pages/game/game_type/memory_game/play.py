# import flet as ft
# import random
# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import ChatPromptTemplate

# # Khởi tạo AI model
# os.environ['GOOGLE_API_KEY'] = "YOUR_GOOGLE_API_KEY"
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7)

# # Template để tạo cặp icon-text
# icon_text_template = """
# Generate {num_pairs} pairs of icons and related words. Each pair should consist of an emoji icon and a related word.
# The word should be in English and suitable for a B1 level English learner.

# Format the response as a JSON array of objects, each with 'icon' and 'word' keys.

# Example:
# [
#     {{"icon": "🐶", "word": "dog"}},
#     {{"icon": "🚗", "word": "car"}},
#     ...
# ]
# """

# icon_text_prompt = ChatPromptTemplate.from_template(icon_text_template)

# def generate_icon_text_pairs(num_pairs):
#     try:
#         chain = icon_text_prompt | llm
#         result = chain.invoke({"num_pairs": num_pairs})
#         return eval(result.content)
#     except Exception as e:
#         print(f"Error generating pairs: {e}")
#         return []

# class MemoryGame(ft.UserControl):
#     def __init__(self):
#         super().__init__()
#         self.pairs = []
#         self.flipped = []
#         self.matched = set()
#         self.score = 0
#         self.timer = 0
#         self.timer_running = False
#         self.difficulty = "easy"
#         self.game_started = False

#     def build(self):
#         self.title = ft.Text("Icon-Text Memory Game", size=30, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER)
#         self.score_text = ft.Text(f"Score: {self.score}", size=20, color=ft.colors.WHITE)
#         self.timer_text = ft.Text("00:00", size=20, color=ft.colors.WHITE)
#         self.game_grid = ft.GridView(
#             expand=1,
#             max_extent=100,
#             child_aspect_ratio=1,
#             spacing=5,
#             run_spacing=5,
#             visible=False
#         )
#         self.difficulty_radio = ft.RadioGroup(
#             content=ft.Row([
#                 ft.Radio(value="easy", label="Easy", fill_color=ft.colors.WHITE),
#                 ft.Radio(value="medium", label="Medium", fill_color=ft.colors.WHITE),
#                 ft.Radio(value="hard", label="Hard", fill_color=ft.colors.WHITE),
#             ]),
#             value="easy",
#         )
#         self.start_button = ft.ElevatedButton("Start Game", on_click=self.start_game, style=ft.ButtonStyle(color=ft.colors.BLACK, bgcolor=ft.colors.WHITE))

#         return ft.Container(
#             width=400,
#             height=800,
#             expand=True,
#             gradient=ft.LinearGradient(
#                 begin=ft.alignment.top_center,
#                 end=ft.alignment.bottom_center,
#                 colors=["#6A1B9A", "#E91E63"]
#             ),
#             content=ft.Column([
#                 self.title,
#                 ft.Row([self.score_text, self.timer_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
#                 ft.Container(
#                     content=self.game_grid,
#                     expand=True,
#                     alignment=ft.alignment.center
#                 ),
#                 self.difficulty_radio,
#                 self.start_button,
#             ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
#         )

#     def start_game(self, e):
#         if not self.game_started:
#             self.difficulty = self.difficulty_radio.value
#             num_pairs = 4 if self.difficulty == "easy" else 8 if self.difficulty == "medium" else 12
#             self.pairs = generate_icon_text_pairs(num_pairs)
#             self.score = 0
#             self.score_text.value = f"Score: {self.score}"
#             self.timer = 0
#             self.timer_running = True
#             self.update_timer()
#             self.create_game_grid()
#             self.difficulty_radio.visible = False
#             self.start_button.text = "Restart Game"
#             self.game_started = True
#             self.game_grid.visible = True
#         else:
#             self.reset_game()
#         self.update()

#     def create_game_grid(self):
#         self.game_grid.controls.clear()
#         all_items = [(pair['icon'], 'icon') for pair in self.pairs] + [(pair['word'], 'word') for pair in self.pairs]
#         random.shuffle(all_items)
#         for i, (item, item_type) in enumerate(all_items):
#             card = ft.Container(
#                 content=ft.Text("?", size=30, color=ft.colors.BLACK),
#                 width=80,
#                 height=80,
#                 bgcolor=ft.colors.WHITE,
#                 border_radius=5,
#                 alignment=ft.alignment.center,
#                 data={'item': item, 'type': item_type},
#                 on_click=lambda e, i=i: self.flip_card(e, i)
#             )
#             self.game_grid.controls.append(card)

#     def flip_card(self, e, index):
#         if not self.game_started or index in self.flipped or index in self.matched:
#             return

#         e.control.content.value = e.control.data['item']
#         e.control.bgcolor = ft.colors.LIGHT_BLUE_200
#         e.control.update()

#         self.flipped.append(index)

#         if len(self.flipped) == 2:
#             self.page.add_future(ft.sleep(0.5), self.check_match)

#     def check_match(self, _):
#         idx1, idx2 = self.flipped
#         card1, card2 = self.game_grid.controls[idx1], self.game_grid.controls[idx2]
        
#         if (card1.data['type'] != card2.data['type'] and 
#             any(pair['icon'] == card1.data['item'] and pair['word'] == card2.data['item'] for pair in self.pairs) or
#             any(pair['icon'] == card2.data['item'] and pair['word'] == card1.data['item'] for pair in self.pairs)):
#             self.matched.update([idx1, idx2])
#             card1.bgcolor = ft.colors.GREEN_200
#             card2.bgcolor = ft.colors.GREEN_200
#             self.score += 1
#             self.score_text.value = f"Score: {self.score}"
#             if len(self.matched) == len(self.pairs) * 2:
#                 self.game_over()
#         else:
#             card1.content.value = "?"
#             card2.content.value = "?"
#             card1.bgcolor = ft.colors.WHITE
#             card2.bgcolor = ft.colors.WHITE

#         self.flipped = []
#         card1.update()
#         card2.update()
#         self.score_text.update()

#     def game_over(self):
#         self.timer_running = False
#         dlg = ft.AlertDialog(
#             title=ft.Text("Congratulations!"),
#             content=ft.Text(f"You completed the game in {self.timer_text.value} with a score of {self.score}!"),
#             actions=[
#                 ft.TextButton("Play Again", on_click=self.close_dlg_and_restart),
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#         )
#         self.page.dialog = dlg
#         dlg.open = True
#         self.page.update()

#     def close_dlg_and_restart(self, e):
#         self.page.dialog.open = False
#         self.page.update()
#         self.reset_game()

#     def reset_game(self):
#         self.game_started = False
#         self.difficulty_radio.visible = True
#         self.start_button.text = "Start Game"
#         self.game_grid.controls.clear()
#         self.game_grid.visible = False
#         self.score = 0
#         self.score_text.value = f"Score: {self.score}"
#         self.timer_text.value = "00:00"
#         self.timer_running = False
#         self.flipped = []
#         self.matched = set()
#         self.update()

#     def update_timer(self):
#         if self.timer_running:
#             self.timer += 1
#             mins, secs = divmod(self.timer, 60)
#             self.timer_text.value = f"{mins:02d}:{secs:02d}"
#             self.timer_text.update()
#             self.page.add_future(ft.sleep(1), self.update_timer)

# # def main(page: ft.Page):
# #     page.title = "Icon-Text Memory Game"
# #     page.window_width = 400
# #     page.window_height = 800
# #     page.window_resizable = False
# #     page.padding = 0
# #     memory_game = MemoryGame()
# #     page.add(memory_game)
# #     page.update()

# # ft.app(target=main)