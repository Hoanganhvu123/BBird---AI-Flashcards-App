import flet as ft

def get_view(page: ft.Page):
    # Define colors
    bg_color = ft.colors.with_opacity(0.95, ft.colors.PURPLE_900)
    text_color = ft.colors.WHITE
    button_color = ft.colors.BLUE_400

    # Create owl image
    owl_image = ft.Image(
        src="E:\\web\\flet-app\\assets\\images\\bbird.png",  # Replace with actual path to owl image
        width=150,
        height=150,
        fit=ft.ImageFit.CONTAIN,
    )

    return ft.View(
        bgcolor=bg_color,
        padding=ft.padding.symmetric(horizontal=20, vertical=40),
        controls=[
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("WELCOME", size=40, color=text_color, weight=ft.FontWeight.BOLD),
                    owl_image,
                    ft.Text("Welcome to BBird", size=24, color=text_color, weight=ft.FontWeight.W_500),
                    ft.Container(
                        content=ft.Text(
                            "Our mission is to promote student achievement and preparation for global competitiveness by fostering educational excellence and ensuring equal access.",
                            size=16,
                            color=text_color,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=ft.padding.only(left=20, right=20),
                    ),
                    
                    #Nút start
                    ft.ElevatedButton(
                        "Start",
                        on_click=lambda _: page.go("/home"),
                        style=ft.ButtonStyle(
                            color=text_color,
                            bgcolor=button_color,
                            padding=ft.padding.all(20),
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                        width=200,
                    )
                ]
            )
        ]
    )

# def main(page: ft.Page):
#     page.title = "Profile User"
#     page.window_width = 400
#     page.window_height = 800
#     page.window_resizable = False

#     def route_change(e):
#         page.views.clear()
#         page.views.append(get_view(page))
#         page.update()

#     page.on_route_change = route_change
#     page.go(page.route)

# ft.app(target=main)