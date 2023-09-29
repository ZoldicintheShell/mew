import markdown2
import re
from weasyprint import HTML, CSS
from PIL import Image
from sys import argv, stderr

# Path arguments are relative paths to the root of mewtwo py projects 
#
# python3 md_to_pdf.py <style_path> <output_path>


def main():
    if (len(argv) != 3):
        print('Arguments error.', file=stderr)
        return 1

    style_path = argv[1]
    output_path = argv[2]

    # Charger le contenu du fichier Markdown
    with open("input.md", "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    # Convertir le Markdown en HTML
    html_content = markdown2.markdown(md_content)

    # Rechercher les balises d'images Markdown et remplacer par des balises HTML
    html_content_with_images = re.sub(r'!\[.*?\]\((.*?)\)', r'<img src="\1" />', html_content)

    # Charger le contenu du fichier CSS
    with open(style_path, "r", encoding="utf-8") as css_file:
        custom_css = css_file.read()

    # Générer le PDF à partir du HTML avec mise en page personnalisée
    final_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    {custom_css}
    </style>
    </head>
    <body>
    {html_content_with_images}
    </body>
    </html>
    """

    html = HTML(string=final_html, base_url="./")  # L'argument base_url aide à résoudre les chemins relatifs
    pdf_bytes = html.write_pdf()

    # Enregistrer le PDF résultant
    with open(output_path, "wb") as pdf_file:
        pdf_file.write(pdf_bytes)

    print("Conversion terminée.")


if __name__ == '__main__':
    main()