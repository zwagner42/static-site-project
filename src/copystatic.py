import shutil
from pathlib import Path

PUBLIC_PATH_CONST = "public"
STATIC_PATH_CONST = "static"

def static_to_public():
    clear_public()

    public_path = Path(PUBLIC_PATH_CONST)
    static_path = Path(STATIC_PATH_CONST)

    if public_path.exists() and static_path.exists():
        print("Copy static contents to public")
        print("-------------------------")
        copy_files(static_path, public_path)
        print("-------------------------")
    else:
        raise Exception("Path to static or public folder could not be found")


def copy_files(src: Path, destination: Path):
    for item in src.iterdir():
        if item.is_file():
            shutil.copy(item, destination)
            print(f"{item} copied to {destination}")
        elif item.is_dir():
            new_destination = destination / item.name
            new_destination.mkdir()
            print(f"New directory '{item.name}' created at {destination}")
            copy_files(src / item.name, new_destination)


def clear_public():
    public_path = Path(PUBLIC_PATH_CONST)
    print("Delete public contents")
    print("-------------------------")
    if public_path.exists():
        for item in public_path.iterdir():
            if item.is_file():
                file_name = item.name
                item.unlink()
                print(f"{file_name} deleted")
            elif item.is_dir():
                dir_name = item.name
                shutil.rmtree(public_path / dir_name)
                print(f"{dir_name} deleted along with inner content")

        print("-------------------------")

    else:
        print("Warning: public directory doesn't exist yet")
        return
