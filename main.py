import toga
import pyperclip

from utils import markdown_to_text, get_api_key
from toga.style.pack import CENTER, COLUMN, ROW, Pack
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.llms import ChatMessage
from google.genai.types import Tool, GenerateContentConfig, UrlContext

model_id = "gemini-2.5-flash-preview-05-20"

url_context_tool = Tool(
    url_context = UrlContext()
)

config = GenerateContentConfig(
    tools=[url_context_tool],
    response_modalities=["TEXT"],
)

llm = GoogleGenAI(model=model_id, generation_config=config, api_key = get_api_key())

class Graze(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow()

        self.webview = toga.WebView(
            on_webview_load=self.on_webview_loaded, style=Pack(flex=1)
        )
        self.url_input = toga.TextInput(
            value="https://clelia.dev/", style=Pack(flex=1)
        )
        self.ai_summary = toga.Label(
            text="AI summary will be shown here", style=Pack(flex=1)
        )

        self.icon = toga.Icon(path="browser-ai.png")

        box = toga.Box(
            children=[
                toga.Box(
                    children=[
                        self.url_input,
                        toga.Button(
                            "Go",
                            on_press=self.load_page,
                            style=Pack(width=50, margin_left=5),
                        ),
                    ],
                    style=Pack(
                        direction=ROW,
                        align_items=CENTER,
                        margin=5,
                    ),
                ),
                self.webview,
                toga.Box(
                    children=[
                        self.ai_summary,
                        toga.Button(
                            "Copy",
                            on_press=self.copy_to_clipboard,
                            style=Pack(width=50, margin_left=5),
                        ),
                    ],
                    style=Pack(
                        height=200,
                        direction=ROW,
                        align_items=CENTER,
                        margin=5,
                    ),
                ),
            ],
            style=Pack(direction=COLUMN),
        )

        self.main_window.content = box
        self.webview.url = self.url_input.value

        # Show the main window
        self.main_window.show()

    def load_page(self, widget):
        self.ai_summary.text = "AI Summary of the Website:\n\n"+"Processing..."
        self.webview.url = self.url_input.value

    def on_webview_loaded(self, widget):
        self.url_input.value = self.webview.url
        response = llm.chat([ChatMessage(role="user", content=f"Can you please summarize the context of this URL: {self.url_input.value}?")])
        self.ai_summary.text = "AI Summary of the Website:\n\n"+markdown_to_text(response.message.blocks[0].text)

    def copy_to_clipboard(self, widget) -> None:
        pyperclip.copy(self.ai_summary.text)

def main():
    return Graze("AI Browser", "browser.clelia.dev")


if __name__ == "__main__":
    main().main_loop()
