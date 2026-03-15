from utils import copy_directory

def main():
    # Kopiujemy wszystkie statyczne pliki
    copy_directory("static", "public")

    # Tutaj idzie reszta generatora HTML
    # generate_site()
    print("Done! The public/ directory is ready.")

if __name__ == "__main__":
    main()