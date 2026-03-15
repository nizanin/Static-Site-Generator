from utils import copy_directory
from page_generator import generate_pages_recursive

def main():
    # Kopiujemy wszystkie statyczne pliki
    copy_directory("static", "public")

    # Tutaj idzie reszta generatora HTML
    # generate_site()
    print("Done! The public/ directory is ready.")

    generate_pages_recursive(
        "content",
        "template.html",
        "public"
    )

if __name__ == "__main__":
    main()