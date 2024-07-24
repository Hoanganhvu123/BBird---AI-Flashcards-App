import os
import flet as ft
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import logging
import json
import re
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Initialize AI model 
os.environ['GOOGLE_API_KEY'] = "AIzaSyCvYf_U35Yk_kEuKJRGWFkfc5-oGS0Cmi0"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=1)

question_template = """
Generate 10 multiple-choice questions based on the following text:

Text: {text}

Your response MUST be in JSON format as follows:
[
    {{
        "question": "The question text here",
        "options": {{
            "A": "Option A text", 
            "B": "Option B text",
            "C": "Option C text",
            "D": "Option D text"  
        }},
        "correct_answer": "The correct answer letter (A, B, C, or D)"
    }},
    ...
]
"""


question_prompt = ChatPromptTemplate.from_template(question_template)

def generate_questions(text: str, num_questions: int = 10) -> List[Dict[str, Any]]:
    questions = []
    try:
        # Tạo câu hỏi mới dựa trên template
        chain = question_prompt | llm 
        result = chain.invoke({"text": text})
        result_content = result.content if hasattr(result, 'content') else str(result)
        logging.info(f"Questions result: {result_content}")
        
        # Loại bỏ phần bao quanh JSON nếu có
        result_content = re.sub(r'^```json\s*|\s*```$', '', result_content.strip())
        
        # Phân tích JSON để lấy danh sách câu hỏi
        parsed_questions = json.loads(result_content)  
        questions.extend(parsed_questions)
        
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON: {str(e)}")
        logging.error(f"Problematic JSON: {result_content}")  
    except Exception as e:
        logging.error(f"Error generating questions: {str(e)}")
    
    return questions

def get_view(page: ft.Page):
    quiz_questions = []
    current_question_index = 0
    score = 0

    def generate_and_load_questions(e):
        nonlocal quiz_questions, current_question_index, score

        if not text_input.value: 
            show_snack_bar("Please enter some text to generate questions.")
            return

        loading_indicator.visible = True  
        generate_button.disabled = True
        page.update()

        try:
            quiz_questions = generate_questions(text_input.value)
            current_question_index = 0
            score = 0

            if quiz_questions:
                welcome_container.visible = False
                question_container.visible = True 
                load_question()
            else:
                raise Exception("No questions generated")
        except Exception as e:
            show_snack_bar(f"Failed to generate questions: {str(e)}")
        finally:
            loading_indicator.visible = False
            generate_button.disabled = False
            page.update()

    def load_question():
        if not quiz_questions:
            return
        
        question_data = quiz_questions[current_question_index]
        question_number.value = f"Question {current_question_index + 1} of {len(quiz_questions)}"
        question_text.value = question_data["question"]
        options_group.content.controls.clear()
        
        option_icons = {"A": "A.", "B":"B.", "C":"C.", "D":"D."}
        for key, value in question_data["options"].items():
            option = ft.Radio(
                value=key, 
                label=f"{option_icons[key]} {value}",
                label_style=ft.TextStyle(color=ft.colors.PURPLE_900 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE)  
            )
            options_group.content.controls.append(option)
        
        options_group.value = None
        progress_bar.value = (current_question_index + 1) / len(quiz_questions) 
        page.update()

    def check_answer(selected_option):
        correct_answer = quiz_questions[current_question_index]["correct_answer"]
        is_correct = selected_option == correct_answer
        message = "Correct! 🎉" if is_correct else f"Incorrect. 😕 The correct answer is {correct_answer}."
        return is_correct, message

    def show_result_dialog(message):  
        dialog = ft.AlertDialog(
            title=ft.Text("Result"),
            content=ft.Text(message),
        )
        page.dialog = dialog
        dialog.open = True  
        page.update()

    def select_option(e):
        selected_option = e.control.value
        is_correct, message = check_answer(selected_option)
        
        show_result_dialog(message)
        
        if is_correct:
            nonlocal score
            score += 1

    def close_dialog_and_next():
        page.dialog.open = False
        page.update()
        show_next_question()

    def show_next_question(e=None):  
        nonlocal current_question_index
        if current_question_index < len(quiz_questions) - 1:
            current_question_index += 1
            load_question()
        else:
            show_result()

    def show_previous_question(e=None):
        nonlocal current_question_index 
        if current_question_index > 0:
            current_question_index -= 1
            load_question()

    def show_result():
        question_container.visible = False
        result_text.value = f"You scored {score} out of {len(quiz_questions)}"  
     
        page.update()

    def restart_quiz(e):
        nonlocal current_question_index, score
        current_question_index = 0
        score = 0
        
        welcome_container.visible = True
        question_container.visible = False
        page.update()

    def show_snack_bar(message):
        page.snack_bar = ft.SnackBar(content=ft.Text(message)) 
        page.snack_bar.open = True
        page.update()

    text_input = ft.TextField(
        label="Enter text for quiz generation", 
        multiline=True, 
        color=ft.colors.BLACK if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE
    )
    generate_button = ft.ElevatedButton(
        content=ft.Text( 
            "Generate Questions", 
            size=15,
        ),
        on_click=generate_and_load_questions,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.PURPLE_900,
            color=ft.colors.PURPLE_900 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
            overlay_color=ft.colors.PURPLE_100,
        )
    )
    
    loading_indicator = ft.ProgressRing(visible=False)
    input_container = ft.Container(
        content=ft.Column([
            text_input,
            ft.Row([generate_button, loading_indicator], alignment=ft.MainAxisAlignment.CENTER),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        padding=30,
        bgcolor=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLACK87,
    )
    
    welcome_icon = ft.Icon(name=ft.icons.QUIZ, color=ft.colors.PURPLE_900 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.PURPLE_200, size=70)
    welcome_message = ft.Text(
        "Bạn đã sẵn sàng cùng BBird👍😎?", 
        size=20, 
        weight=ft.FontWeight.BOLD, 
        color=ft.colors.PURPLE_900 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE
    )   
    welcome_container = ft.Container(
        content=ft.Column([
            welcome_icon,
            welcome_message,
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLACK87,
        expand=True
    )
    
    question_text = ft.Text(
        size=24, 
        weight=ft.FontWeight.BOLD, 
        color=ft.colors.PURPLE_900 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE
    )
    options_group = ft.RadioGroup(content=ft.Column(), on_change=select_option)
    question_number = ft.Text(
        size=18, 
        color=ft.colors.PURPLE_900 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE
    )
    progress_bar = ft.ProgressBar(
        width=200, 
        color=ft.colors.PURPLE_900 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.PURPLE_200, 
        bgcolor=ft.colors.PURPLE_100 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.PURPLE_900
    )

    prev_button = ft.ElevatedButton(
        "Previous", 
        on_click=show_previous_question, 
        icon=ft.icons.ARROW_BACK,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.PURPLE_900,
            color=ft.colors.PURPLE_900 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
        )
    )
    next_button = ft.ElevatedButton(
        "Next", 
        on_click=show_next_question, 
        icon=ft.icons.ARROW_FORWARD,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.PURPLE_900,
            color=ft.colors.PURPLE_900 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE,
        )
    )

    question_container = ft.Container(
        content=ft.Column([
            question_number,
            progress_bar,
            question_text,
            options_group,
            ft.Row([prev_button, next_button], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        bgcolor=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLACK87,
        expand=True,
        visible=False
    )

    result_text = ft.Text(
        size=24, 
        color=ft.colors.PURPLE_900 if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.WHITE
    )

    


    return ft.View(
        "/quizz",
        [
            ft.AppBar(
                leading=ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=ft.colors.WHITE, on_click=lambda e: page.go("/home")),
                title=ft.Text("AI-Generated English Quiz", color=ft.colors.WHITE, size=20, weight="bold"),
                center_title=True,
                bgcolor=ft.colors.PURPLE_900,
                toolbar_height=60,
            ),
            ft.Column(
                controls=[
                    input_container,
                    welcome_container,
                    question_container,
                   
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True,
                # bgcolor=ft.colors.WHITE if page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.BLACK87,
            )
        ]
    )

# # Phần main có thể giữ nguyên hoặc điều chỉnh như sau:
# def main(page: ft.Page):
#     page.title = "AI-Generated English Quiz"
#     page.theme_mode = ft.ThemeMode.LIGHT  # hoặc DARK tùy theo mong muốn
#     page.update()

#     def route_change(route):  
#         page.views.clear()
#         page.views.append(get_view(page))
#         page.update()

#     page.on_route_change = route_change
#     page.go('/quizz')

# ft.app(target=main)