from pathlib import Path
from pydoc import html

from markdown_helpers import extract_title, markdown_to_html_node


def generate_page(from_path: Path, template_path: Path, dest_path: Path, base_path: Path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_path_content = ""
    template_path_content = ""

    with open(from_path, 'r') as file:
        from_path_content = file.read()

    with open(template_path, 'r') as file:
        template_path_content = file.read()

    html_content = markdown_to_html_node(from_path_content).to_html()
    title = extract_title(from_path_content)

    template_content = template_path_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_content)

    template_content = template_content.replace("href='/", f"href='{base_path}/")
    template_content = template_content.replace("src='/", f"src='{base_path}/")

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    dest_path.touch()

    with open(dest_path, 'w') as file:
        file.write(template_content)

def generate_pages_recursive(dir_path_content: Path, template_path: Path, dest_dir_path: Path, base_path: Path):

    for content in dir_path_content.iterdir():
        if content.is_file() and content.suffix == ".md":
            generate_page(dir_path_content / content.name, template_path, dest_dir_path / (content.stem + ".html"), base_path)
        elif content.is_dir():
            generate_pages_recursive(dir_path_content / content.name, template_path, dest_dir_path / content.name, base_path)
