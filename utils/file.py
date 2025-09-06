import os


def abs_path_from_project(relative_path: str) -> str:
    """
    Возвращает абсолютный путь до файла относительно корня проекта.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, relative_path)
