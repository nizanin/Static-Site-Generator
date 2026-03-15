from utils import copy_directory
from page_generator import generate_page

def main():
    # Kopiujemy wszystkie statyczne pliki
    copy_directory("static", "public")

    # Tutaj idzie reszta generatora HTML
    # generate_site()
    print("Done! The public/ directory is ready.")

    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html"
    )

if __name__ == "__main__":
    main()