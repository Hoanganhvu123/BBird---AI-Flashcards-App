import os
import flet as ft
from flet import (
    AppBar, ElevatedButton, View, Text, Column, Container, Row, colors, alignment,
    padding, border_radius, Page, TextField, CircleAvatar, Icon, icons, margin, IconButton
)
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

import warnings
warnings.filterwarnings("ignore")

# Khởi tạo các biến môi trường và LLM
os.environ['GOOGLE_API_KEY'] = "AIzaSyCvYf_U35Yk_kEuKJRGWFkfc5-oGS0Cmi0"
os.environ['GROQ_API_KEY'] = "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"

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Định nghĩa prompt template
prompt_template = ChatPromptTemplate.from_template(
    """You are an English tutor who specializes in teaching beginners how to speak English 
    without focusing on grammar. Instead, you focus on helping learners to build their vocabulary 
    and use new words to form simple sentences. This method is very easy and effective for beginners 
    who have no prior knowledge of English. Whenever a learner asks a question, provide them with simple 
    words and examples of how to use those words in sentences. Avoid complex grammar rules and keep your 
    explanations straightforward and encouraging.\n
    Oke thats all thing u can do brooo. So lets talk to student as a closest friend broo. 
    USING MORE ICON and MEME IN CONSERVATION AND ALWAYS USING VIETNAMESE TO TALK WITH LEARNER BROOOO
    {history}\n
    Q: {input}\nA:"""
)

# Khởi tạo memory và chain
memory = ConversationBufferMemory(input_key="input", memory_key="history")
chain = ConversationChain(llm=llm, prompt=prompt_template, memory=memory)

# Biến toàn cục cho controls
messages = None
question_input = None

def create_user_message(question, page: Page):
    return Container(
        content=Text(question, size=16, color=colors.BLACK if page.theme_mode == ft.ThemeMode.LIGHT else colors.WHITE),
        alignment=alignment.center_right,
        border_radius=border_radius.all(20),
        bgcolor=colors.GREY_100 if page.theme_mode == ft.ThemeMode.LIGHT else colors.GREY_800,
        padding=padding.all(10),
        margin=margin.only(left=40, bottom=5),
        width=None,
        expand=False
    )

def create_bot_message(content, page: Page):
    return Container(
        content=Row(
            controls=[
                CircleAvatar(
                    content=Icon(icons.SMART_TOY, color=colors.WHITE, size=20),
                    bgcolor=colors.PURPLE_700 if page.theme_mode == ft.ThemeMode.LIGHT else colors.PURPLE_300,
                    radius=20,
                ),
                Container(
                    content=Text(content, size=16, color=colors.BLACK if page.theme_mode == ft.ThemeMode.LIGHT else colors.WHITE),
                    bgcolor=colors.GREY_100 if page.theme_mode == ft.ThemeMode.LIGHT else colors.GREY_800,
                    border_radius=border_radius.only(top_right=20, bottom_left=20, bottom_right=20),
                    padding=padding.all(10),
                    expand=False,
                    width=250,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        margin=margin.only(right=40, bottom=5),
    )

def handle_question_submit(e, page: Page):
    question = question_input.value
    if not question:
        return

    user_message = create_user_message(question, page)
    messages.controls.append(user_message)
    question_input.value = ""
    question_input.update()

    response = chain({"input": question})

    bot_message = create_bot_message(response["response"], page)
    messages.controls.append(bot_message)
    messages.update()

def get_view(page: Page):
    global messages, question_input

    messages = Column(
        scroll="auto",
        expand=True,
        spacing=10,
    )

    messages_container = Container(
        content=messages,
        expand=True,
        bgcolor=colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else colors.BLACK87
    )

    question_input = TextField(
        hint_text="Hỏi gì đi bạn ơi... 😊",
        expand=True,
        border_color=colors.PURPLE_200 if page.theme_mode == ft.ThemeMode.LIGHT else colors.PURPLE_700,
        focused_border_color=colors.PURPLE_400 if page.theme_mode == ft.ThemeMode.LIGHT else colors.PURPLE_300,
        border_radius=30,
        text_style=ft.TextStyle(color=colors.BLACK if page.theme_mode == ft.ThemeMode.LIGHT else colors.WHITE),
        hint_style=ft.TextStyle(color=colors.BLACK54 if page.theme_mode == ft.ThemeMode.LIGHT else colors.WHITE70),
        on_submit=lambda e: handle_question_submit(e, page)
    )

    return View(
        "/aitutor",
        [
            AppBar(
                leading=Row(
                    controls=[
                        IconButton(
                            icon=ft.icons.ARROW_BACK,
                            icon_color=colors.WHITE,
                            on_click=lambda _: page.go("/home")
                        ),
                        Icon(ft.icons.PSYCHOLOGY_ALT, color=colors.WHITE)
                    ],
                    spacing=5
                ),
                title=Text("AI Tutor 🧠", color=colors.WHITE, size=24, weight="bold"),
                center_title=True,
                bgcolor=colors.PURPLE_900,
                toolbar_height=60,
            ),
            Container(
                content=Column(
                    controls=[
                        messages_container,
                        Row(
                            controls=[
                                question_input,
                                ElevatedButton(
                                    "Gửi 🚀",
                                    on_click=lambda e: handle_question_submit(e, page),
                                    style=ft.ButtonStyle(
                                        color=colors.WHITE,
                                        bgcolor=colors.PURPLE_900 if page.theme_mode == ft.ThemeMode.LIGHT else colors.PURPLE_700,
                                        padding=20,
                                        shape=ft.RoundedRectangleBorder(radius=30)
                                    )
                                )
                            ],
                            spacing=10
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    expand=True
                ),
                expand=True,
                padding=padding.all(20),
                bgcolor=colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else colors.BLACK87,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=colors.PURPLE_100 if page.theme_mode == ft.ThemeMode.LIGHT else colors.PURPLE_900,
                    offset=ft.Offset(0, 0),
                ),
            )
        ],
    )

# # Phần main để chạy ứng dụng (nếu cần)
# def main(page: Page):
#     page.title = "AI Tutor"
#     page.theme_mode = ft.ThemeMode.DARK  # Hoặc LIGHT tùy theo mong muốn
#     page.update()

#     def route_change(route):
#         page.views.clear()
#         page.views.append(get_view(page))
#         page.update()

#     page.on_route_change = route_change
#     page.go('/aitutor')

# ft.app(target=main)