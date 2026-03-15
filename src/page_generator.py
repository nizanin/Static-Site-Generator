import os
from block_markdown import markdown_to_html_node  # Twój parser
from utils import extract_title  # zakładając, że extract_title jest w osobnym pliku

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Wczytaj markdown
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Wczytaj template
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Konwertuj markdown na HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Wyciągnij tytuł
    title = extract_title(markdown_content)

    # Zamień placeholdery w template
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Utwórz katalogi, jeśli nie istnieją
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Zapisz plik
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Page generated at {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(entry_path):
            # jeśli katalog → rekurencja
            generate_pages_recursive(entry_path, template_path, dest_path)

        elif entry.endswith(".md"):
            # zmień rozszerzenie na .html
            dest_file = dest_path.replace(".md", ".html")

            generate_page(
                entry_path,
                template_path,
                dest_file
            )