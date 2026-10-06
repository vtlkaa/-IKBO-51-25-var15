"""Модуль эмулятора оболочки ОС."""
import os
import argparse
import io
import zipfile


def expand_var(user_input):
    """Раскрывает переменные окружения в строке.
    Args:
        user_input: Строка, введённая пользователем.

    Returns:
        Строка с раскрытыми переменными окружения.
    """
    return os.path.expandvars(user_input)


def parse_command(expanded_input):
    """Разбирает команду на имя и аргументы.
    Args:
        expanded_input: Строка с раскрытыми переменными окружения.
    Returns:
        Кортеж (команда, аргументы).
    """
    parts = expanded_input.split()
    if not parts:
        return None, []
    return parts[0], parts[1:]


def execute_command(command, args, vfs, current_dir):
    if command is None:
        return True, current_dir
    elif command == "exit":
        print("Выход из эмулятора оболочки")
        return False, current_dir
    elif command == "ls":
        cmd_ls(vfs, current_dir)
        return True, current_dir
    elif command == "cd":
        new_dir = cmd_cd(args, vfs, current_dir)
        return True, new_dir
    elif command == "rev":
        cmd_rev(args)
        return True, current_dir
    elif command == "find":
        cmd_find(args, vfs)
        return True, current_dir
    elif command == "du":
        cmd_du(vfs, current_dir)
        return True, current_dir
    else:
        print(f"Ошибка: команда '{command}' не найдена.")
        return True, current_dir


def parse_argument():
    """Разбирает параметры командной строки.

    Returns:
        Объект с параметрами (vfs, script).
    """
    parser = argparse.ArgumentParser(description="Эмулятор оболочки ОС")

    parser.add_argument(
        "--vfs",
        type=str,
        default=None,
        help="Путь к расположению VFS"
    )

    parser.add_argument(
        "--script",
        type=str,
        default=None,
        help="Путь к скрипту"
    )

    return parser.parse_args()


def run_script(script_path, vfs, current_dir):
    try:
        with open(script_path, "r", encoding="UTF-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                print(f"my_vfs> {line}")

                expanded = expand_var(line)
                command, cmd_args = parse_command(expanded)

                if command is None:
                    continue

                keep_going, current_dir = execute_command(command, cmd_args, vfs, current_dir)
                if not keep_going:
                    break

    except FileNotFoundError:
        print(f"Ошибка: файл {script_path} не найден")

    return current_dir


def load_vfs(vfs_path):
    """Загружает VFS из ZIP-архива в память.

    Args:
        vfs_path: Путь к ZIP-архиву.

    Returns:
        Объект ZipFile, загруженный в память.
        None, если архив не найден.
    """
    try:
        with open(vfs_path, "rb") as f:
            data = f.read()

        buffer = io.BytesIO(data)
        archive = zipfile.ZipFile(buffer)
        return archive

    except FileNotFoundError:
        print(f"Ошибка: файл {vfs_path} не найден")
        return None


def cmd_ls(vfs, current_dir):
    """Выводит содержимое текущей директории."""
    names = vfs.namelist()
    items = set()
    for name in names:
        if name == current_dir:
            continue
        if name.startswith(current_dir):
            rest = name[len(current_dir):]
            first = rest.split("/")[0]
            if first:
                items.add(first + ("/" if "/" in rest else ""))
    for item in sorted(items):
        print(item)


def cmd_cd(args, vfs, current_dir):
    """Меняет текущую директорию.

    Args:
        args: аргументы команды.
        vfs: объект ZipFile.
        current_dir: текущая директория.

    Returns:
        Новая текущая директория.
    """
    if not args:
        print("Ошибка: укажите директорию")
        return current_dir

    target = args[0]
    new_dir = current_dir + target + "/"

    names = vfs.namelist()
    if new_dir in names:
        print(f"Переход в: {new_dir}")
        return new_dir
    else:
        print(f"Ошибка: директория '{target}' не найдена")
        return current_dir


def cmd_rev(args):
    """Реверсирует строку.

    Args:
        args: аргументы команды.
    """
    if not args:
        print("Ошибка: укажите строку")
        return

    text = args[0]
    print(text[::-1])


def cmd_find(args, vfs):
    """Ищет файлы по имени.

    Args:
        args: аргументы команды.
        vfs: объект ZipFile.
    """
    if not args:
        print("Ошибка: укажите имя файла")
        return

    target = args[0]
    names = vfs.namelist()
    found = False

    for name in names:
        if target in name:
            print(name)
            found = True

    if not found:
        print(f"Файл '{target}' не найден")


def cmd_du(vfs, current_dir):
    """Выводит размер файлов в текущей директории.

    Args:
        vfs: объект ZipFile.
        current_dir: текущая директория.
    """
    names = vfs.namelist()
    total = 0

    for name in names:
        if name == current_dir:
            continue
        if name.startswith(current_dir):
            rest = name[len(current_dir):]
            if "/" not in rest:
                data = vfs.read(name)
                size = len(data)
                print(f"{rest}: {size} байт")
                total += size

    print(f"Итого: {total} байт")


def main():
    """Главная функция эмулятора."""
    args = parse_argument()

    print(f"VFS: {args.vfs}")
    print(f"Script: {args.script}")

    vfs = None
    current_dir = None

    if args.vfs:
        vfs = load_vfs(args.vfs)
        if vfs:
            print(f"VFS загружена. Файлов: {len(vfs.namelist())}")
            names = vfs.namelist()
            if names:
                current_dir = names[0]

    if args.script:
        current_dir = run_script(args.script, vfs, current_dir)

    print("Добро пожаловать в эмулятор оболочки!")
    user_vfs = "my_vfs"

    while True:
        try:
            user_input = input(f"{user_vfs}> ")
        except KeyboardInterrupt:
            print("Для выхода введите 'exit'")
            continue

        expanded = expand_var(user_input)
        command, cmd_args = parse_command(expanded)

        keep_going, current_dir = execute_command(command, cmd_args, vfs, current_dir)
        if not keep_going:
            break


if __name__ == "__main__":
    main()