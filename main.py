import flet as ft
import json
import urllib.request
import urllib.parse
import os

# A simple beautiful AI Chat App for Android
def main(page: ft.Page):
    page.title = "Antigravity Mobile"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0E1117"
    page.window_width = 400
    page.window_height = 800

    chat_messages = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    user_input = ft.TextField(
        hint_text="Ask Antigravity...",
        expand=True,
        border_radius=20,
        filled=True,
        bgcolor="#1E232B",
        border_color="transparent"
    )

    API_KEY = "sk-or-v1-xxxxxxxxxx" # Set your API key here or via settings

    def send_message(e):
        if not user_input.value:
            return
        
        msg = user_input.value
        user_input.value = ""
        page.update()

        # Add user message
        chat_messages.controls.append(
            ft.Container(
                content=ft.Text(msg, color="white"),
                bgcolor="#2563EB",
                padding=10,
                border_radius=10,
                alignment=ft.alignment.center_right,
                margin=ft.margin.only(left=50)
            )
        )
        
        # Thinking bubble
        thinking = ft.Text("Thinking...", italic=True, color="grey")
        chat_messages.controls.append(thinking)
        page.update()

        # Call OpenRouter API (using standard lib to avoid extra dependencies for mobile if possible, 
        # but requests is fine too. Using urllib for zero-dependency standard.)
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            data = {
                "model": "google/gemma-2-9b-it:free",
                "messages": [{"role": "user", "content": msg}]
            }
            req = urllib.request.Request(url, json.dumps(data).encode('utf-8'))
            req.add_header('Content-Type', 'application/json')
            if API_KEY and API_KEY != "sk-or-v1-xxxxxxxxxx":
                req.add_header('Authorization', f'Bearer {API_KEY}')

            try:
                response = urllib.request.urlopen(req)
                res_data = json.loads(response.read().decode('utf-8'))
                ai_text = res_data['choices'][0]['message']['content']
            except Exception as e:
                ai_text = "API Error. Please check your internet connection or add your OpenRouter API Key in the source code."

            # Remove thinking
            chat_messages.controls.remove(thinking)
            
            # Add AI message
            chat_messages.controls.append(
                ft.Container(
                    content=ft.Markdown(ai_text, selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED),
                    bgcolor="#1A1D24",
                    padding=10,
                    border_radius=10,
                    margin=ft.margin.only(right=50)
                )
            )
        except Exception as ex:
            chat_messages.controls.remove(thinking)
            chat_messages.controls.append(ft.Text(f"Error: {ex}", color="red"))

        page.update()

    send_btn = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color="#2563EB",
        on_click=send_message
    )

    page.add(
        ft.AppBar(title=ft.Text("Antigravity AI"), bgcolor="#0E1117"),
        chat_messages,
        ft.Row([user_input, send_btn])
    )

ft.app(target=main)
