import os
import flet as ft
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import logging
import json
import re

logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Initialize AI model
os.environ['GOOGLE_API_KEY'] = "AIzaSyCvYf_U35Yk_kEuKJRGWFkfc5-oGS0Cmi0"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=1)

# Define prompt template for generating questions
question_template = """
Generate a multiple-choice question based on the following text:
{text}

Your response MUST be in JSON format as follows:
{{
    "question": "The question text here",
    "options": {{
        "A": "Option A text",
        "B": "Option B text",
        "C": "Option C text",
        "D": "Option D text"
    }},
    "correct_answer": "The correct answer letter (A, B, C, or D)"
}}

Rules:
1. The question must be related to the given text.
2. Provide exactly 4 options (A, B, C, D).
3. Only one option should be correct.
4. The correct answer should be indicated by its letter only (A, B, C, or D).
5. Ensure all parts of the JSON format are present and correctly structured.
"""
question_prompt = ChatPromptTemplate.from_template(question_template)

def generate_questions(text, num_questions=3):
    questions = []
    for i in range(num_questions):
        try:
            chain = question_prompt | llm
            result = chain.invoke({"text": text})
            result_content = result.content if hasattr(result, 'content') else str(result)
            logging.info(f"Question {i+1} result: {result_content}")
            
            result_content = re.sub(r'^```json\s*|\s*```$', '', result_content.strip())
            
            parsed_question = json.loads(result_content)
            questions.append(parsed_question)
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON for question {i+1}: {str(e)}")
            logging.error(f"Problematic JSON: {result_content}")
        except Exception as e:
            logging.error(f"Error generating question {i+1}: {str(e)}")
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
        
        option_icons = {"A": "A.", "B": "B.", "C": "C.", "D": "D."}
        for key, value in question_data["options"].items():
            option = ft.Radio(
                value=key, 
                label=f"{option_icons[key]} {value}",
                label_style=ft.TextStyle(color=ft.colors.PURPLE_900)
                
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
        result_container.visible = True
        page.update()

    def restart_quiz(e):
        nonlocal current_question_index, score
        current_question_index = 0
        score = 0
        result_container.visible = False
        welcome_container.visible = True
        question_container.visible = False
        page.update()

    def show_snack_bar(message):
        page.snack_bar = ft.SnackBar(content=ft.Text(message))
        page.snack_bar.open = True
        page.update()


    #Chỉnh sửa giao diện ô Generate Question
    text_input = ft.TextField(label="Enter text for quiz generation", multiline=True, color = ft.colors.BLACK)
    generate_button = ft.ElevatedButton(
        content=ft.Text(
            "Generate Questions", 
            size=15,  # Kích cỡ text
            weight="bold"  # Độ đậm của chữ
        ),
        on_click=generate_and_load_questions,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.WHITE,
            color=ft.colors.PURPLE_900,
            overlay_color=ft.colors.PURPLE_100,
        )
    )
    
    
    loading_indicator = ft.ProgressRing(visible=False)
    input_container = ft.Container(
        content=ft.Column([
            text_input,
            ft.Row([generate_button, loading_indicator], alignment=ft.MainAxisAlignment.CENTER),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        border=ft.border.all(2, ft.colors.PURPLE_900),
    )
    
    
    welcome_icon = ft.Icon(name=ft.icons.QUIZ, color=ft.colors.PURPLE_900, size=100)
    welcome_message = ft.Text("Sẵn sàng thử thách trí tuệ của bạn?", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_900)
    welcome_container = ft.Container(
        content=ft.Column([
            welcome_icon,
            welcome_message,
        ], alignment=ft.MainAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        expand=True
    )
    
    question_text = ft.Text(size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_900)
    options_group = ft.RadioGroup(content=ft.Column(), on_change=select_option)
    question_number = ft.Text(size=18, color=ft.colors.PURPLE_900)
    progress_bar = ft.ProgressBar(width=300, color=ft.colors.PURPLE_900, bgcolor=ft.colors.PURPLE_900)

    prev_button = ft.ElevatedButton("Previous", on_click=show_previous_question, icon=ft.icons.ARROW_BACK)
    next_button = ft.ElevatedButton("Next", on_click=show_next_question, icon=ft.icons.ARROW_FORWARD)

    question_container = ft.Container(
        content=ft.Column([
            question_number,
            progress_bar,
            question_text,
            options_group,
            ft.Row([prev_button, next_button], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding = 20,
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        border=ft.border.all(2, ft.colors.WHITE),
        expand=True,
        visible=False
    )

    result_text = ft.Text(size=24, color=ft.colors.PURPLE_900)
    restart_button = ft.ElevatedButton("Restart Quiz", on_click=restart_quiz, style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_600))
    
    result_container = ft.Container(
        content=ft.Column([result_text, restart_button], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        padding=20,
        bgcolor=ft.colors.PURPLE_900,
        border_radius=10,
        expand=True,
        visible=False
    )

    return ft.View(
        "/quizz",
        [
            ft.AppBar(
                leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda e: page.go("/home")),
                title=ft.Text("AI-Generated English Quiz", color=ft.colors.WHITE, size=20, weight="bold"),
                center_title=True,
                bgcolor=ft.colors.PURPLE_900,
                toolbar_height=60,
            ),
            ft.Container(
                controls=[
                    input_container,
                    welcome_container,
                    question_container,
                    result_container
                ],
            )
        ]
    )


def main(page: ft.Page):
    page.title = "Quizz"
    page.window.width = 400
    page.window.height = 850
    page.window_resizable = False

    def route_change(e):
        page.views.clear()
        page.views.append(get_view(page))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
