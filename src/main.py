import sys
from utils import copy_directory
from page_generator import generate_pages_recursive

def main():
    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    # Kopiujemy wszystkie statyczne pliki
    copy_directory("static", "docs")

    # Tutaj idzie reszta generatora HTML
    # generate_site()
    print("Done! The public/ directory is ready.")

    generate_pages_recursive(
        "content",
        "template.html",
        "docs",
        basepath
    )

if __name__ == "__main__":
    main()