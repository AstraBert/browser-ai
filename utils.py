import markdown
import textwrap

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from os import environ as ENV

def get_api_key() -> str:
    google_api_key = ENV.get("GOOGLE_API_KEY", None)
    if google_api_key is None:
        load_dotenv()
        google_api_key = ENV.get("GOOGLE_API_KEY", None)
        if not google_api_key:
            raise ValueError("There is no GOOGLE_API_KEY declared among the environmental variables")
    return google_api_key

def markdown_to_text(md_string, line_length=200):
    html = markdown.markdown(md_string)

    soup = BeautifulSoup(html, 'html.parser')
    plain_text = soup.get_text()

    cleaned_text = '\n\n'.join(
        paragraph.strip() for paragraph in plain_text.split('\n\n')
        if paragraph.strip()
    )

    wrapped_paragraphs = []
    for paragraph in cleaned_text.split('\n\n'):
        if paragraph.strip():
            wrapped = textwrap.fill(
                paragraph,
                width=line_length,
                break_long_words=False,
                break_on_hyphens=True
            )
            wrapped_paragraphs.append(wrapped)

    return '\n\n'.join(wrapped_paragraphs)
