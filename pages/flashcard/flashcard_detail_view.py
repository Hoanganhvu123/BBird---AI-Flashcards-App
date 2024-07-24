import flet as ft
from flet import (
    AppBar, ElevatedButton, View, Text, Column, Container, colors, IconButton,
    icons, Card, AnimatedSwitcher, alignment, border_radius, padding, margin,
    LinearGradient
)

def get_flashcard_detail_view(page: ft.Page, category: str):
    flashcards = {
        "Business": [
            {"question": "economy", "answer": "nền kinh tế 📈"},
            {"question": "market", "answer": "thị trường 🏪"},
            {"question": "investment", "answer": "đầu tư 💰"},
            {"question": "profit", "answer": "lợi nhuận 💵"},
            {"question": "entrepreneur", "answer": "doanh nhân 👔"},
            {"question": "merger", "answer": "sáp nhập 🔄"},
            {"question": "revenue", "answer": "doanh thu 📊"},
            {"question": "bankruptcy", "answer": "phá sản 💸"},
            {"question": "marketing", "answer": "tiếp thị 📣"},
            {"question": "innovation", "answer": "sự đổi mới 💡"}
        ],
        "Computer": [
            {"question": "hardware", "answer": "phần cứng 🖥️"},
            {"question": "software", "answer": "phần mềm 💾"},
            {"question": "database", "answer": "cơ sở dữ liệu 🗄️"},
            {"question": "network", "answer": "mạng lưới 🌐"},
            {"question": "algorithm", "answer": "thuật toán 📜"},
            {"question": "encryption", "answer": "mã hóa 🔐"},
            {"question": "programming", "answer": "lập trình 💻"},
            {"question": "cybersecurity", "answer": "an ninh mạng 🛡️"},
            {"question": "cloud computing", "answer": "điện toán đám mây ☁️"},
            {"question": "artificial intelligence", "answer": "trí tuệ nhân tạo 🤖"}
        ],
        "Math": [
            {"question": "addition", "answer": "phép cộng ➕"},
            {"question": "subtraction", "answer": "phép trừ ➖"},
            {"question": "multiplication", "answer": "phép nhân ✖️"},
            {"question": "division", "answer": "phép chia ➗"},
            {"question": "square root", "answer": "căn bậc hai √"},
            {"question": "equation", "answer": "phương trình 📐"},
            {"question": "area", "answer": "diện tích 📏"},
            {"question": "perimeter", "answer": "chu vi 📏"},
            {"question": "factorial", "answer": "giai thừa ❗"},
            {"question": "Pythagorean theorem", "answer": "định lý Pythagoras 📏"}
        ],
        "Science": [
            {"question": "atom", "answer": "nguyên tử ⚛️"},
            {"question": "molecule", "answer": "phân tử 🔬"},
            {"question": "gravity", "answer": "trọng lực 🌍"},
            {"question": "evolution", "answer": "tiến hóa 🧬"},
            {"question": "photosynthesis", "answer": "quang hợp 🌿"},
            {"question": "ecosystem", "answer": "hệ sinh thái 🌳"},
            {"question": "genetics", "answer": "di truyền học 🧬"},
            {"question": "thermodynamics", "answer": "nhiệt động học 🌡️"},
            {"question": "quantum mechanics", "answer": "cơ học lượng tử 🔭"},
            {"question": "relativity", "answer": "thuyết tương đối 🌌"}
        ],
        "Literature": [
            {"question": "novel", "answer": "tiểu thuyết 📖"},
            {"question": "poetry", "answer": "thơ ca 📜"},
            {"question": "drama", "answer": "kịch 🎭"},
            {"question": "fiction", "answer": "hư cấu 📚"},
            {"question": "non-fiction", "answer": "phi hư cấu 📘"},
            {"question": "protagonist", "answer": "nhân vật chính 👤"},
            {"question": "antagonist", "answer": "nhân vật phản diện 👿"},
            {"question": "plot", "answer": "cốt truyện 📝"},
            {"question": "theme", "answer": "chủ đề 🎨"},
            {"question": "metaphor", "answer": "phép ẩn dụ 🔍"}
        ],
        "Language": [
            {"question": "noun", "answer": "danh từ 📚"},
            {"question": "verb", "answer": "động từ 🏃"},
            {"question": "adjective", "answer": "tính từ 🌟"},
            {"question": "adverb", "answer": "trạng từ 🕒"},
            {"question": "pronoun", "answer": "đại từ 🤖"},
            {"question": "preposition", "answer": "giới từ 🧭"},
            {"question": "conjunction", "answer": "liên từ 🔗"},
            {"question": "interjection", "answer": "thán từ 💬"},
            {"question": "grammar", "answer": "ngữ pháp 📘"},
            {"question": "syntax", "answer": "cú pháp 🧩"}
        ]
    }

    flashcard_list = flashcards.get(category, [])
    current_card_index = 0

    def flip_card(e):
        content = flashcard.content
        if content.data == "question":
            content.content = answer_text
            content.data = "answer"
        else:
            content.content = question_text
            content.data = "question"
        flashcard.update()

    def change_card(forward: bool):
        nonlocal current_card_index
        if forward and current_card_index < len(flashcard_list) - 1:
            current_card_index += 1
        elif not forward and current_card_index > 0:
            current_card_index -= 1
        update_card_content()

    def update_card_content():
        current_flashcard = flashcard_list[current_card_index]
        question_text.value = current_flashcard["question"]
        answer_text.value = current_flashcard["answer"]
        flashcard.content.content = question_text
        flashcard.content.data = "question"
        progress_text.value = f"{current_card_index + 1}/{len(flashcard_list)}"
        page.update()

    question_text = Text(
        size=24,
        weight="bold",
        text_align="center", 
        color=colors.WHITE
    )
    answer_text = Text(
        size=22,
        text_align="center",
        color=colors.WHITE  
    )
    
    flashcard = ft.AnimatedSwitcher(
        content=ft.Container(
            content=question_text,
            data="question", 
            width=340,
            height=200,
            bgcolor=ft.colors.PURPLE_800 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.PURPLE_200,
            border_radius=ft.border_radius.all(15),
            padding=20,
            alignment=ft.alignment.center,
            on_click=flip_card,
        ),
        transition=ft.AnimatedSwitcherTransition.ROTATION,
        duration=300,
        reverse_duration=300,
        switch_in_curve=ft.AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN,
        switch_out_curve=ft.AnimationCurve.ELASTIC_IN,
    )

    progress_text = Text(
        color=colors.PURPLE_900 if page.theme_mode == ft.ThemeMode.LIGHT else colors.PURPLE_200,
        weight="bold"
    )

    def go_back(e):
        page.go("/flashcards")

    update_card_content()

    return View(
        "/flashcards/" + category,
        [
            AppBar(
                title=Text(category, color=colors.WHITE, size=24, weight="bold"),
                bgcolor=colors.PURPLE_900,
                leading=IconButton(icons.ARROW_BACK, on_click=go_back, icon_color=colors.WHITE),
                center_title=True,
            ),
            Container(
                expand=True,
                padding=padding.all(20),
                bgcolor=colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else colors.BLACK87,
                content=Column(
                    [
                        flashcard,
                        Container(height=20),
                        progress_text,
                        Container(height=20),
                        ft.Row(
                            [
                                IconButton(
                                    icon=icons.ARROW_BACK,
                                    on_click=lambda _: change_card(False),
                                    icon_color=colors.PURPLE_900 if page.theme_mode == ft.ThemeMode.LIGHT else colors.PURPLE_200,
                                    icon_size=30,
                                ),
                                IconButton(
                                    icon=icons.ARROW_FORWARD,
                                    on_click=lambda _: change_card(True),
                                    icon_color=colors.PURPLE_900 if page.theme_mode == ft.ThemeMode.LIGHT else colors.PURPLE_200,
                                    icon_size=30,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=40,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
        ],
    )

# def main(page: ft.Page):
#     page.title = "Flashcard Master"
#     page.window.width = 400
#     page.window.height = 850
#     page.window.resizable = False
#     page.theme_mode = ft.ThemeMode.LIGHT  # hoặc DARK tùy theo mong muốn

#     def route_change(e):
#         page.views.clear()
#         page.views.append(get_flashcard_detail_view(page, "Math"))
#         page.update()

#     page.on_route_change = route_change
#     page.go(page.route)

# ft.app(target=main)