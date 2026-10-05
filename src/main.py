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


def execute_command(command, args):
    if command is None:
        return True

    elif command == "exit":
        print("Выход из эмулятора оболочки")
        return False

    elif command in ["ls", "cd"]:
        print(f"Заглушка - Команда: {command}")
        print(f"Заглушка - Аргументы: {' '.join(args)}")
        return True

    else:
        print(f"Ошибка: команда '{command}' не найдена.")
        return True


def parse_argument():
    """Разбирает параметры командной строки.

    Returns:
        Объект с параметрами (vfs, script).
    """
    parser = argparse.ArgumentParser(description="Эмулятор оболочки ОС")

    parser.add_argument(
        "--vfs",
        type = str,
        default= None,
        help = "Путь к расположению VFS"
    )

    parser.add_argument(
            "--script",
            type = str,
            default= None,
            help = "Путь к скрипту"
        )

    return parser.parse_args()

def run_script(script_path):
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

                keep_going = execute_command(command, cmd_args)
                if not keep_going:
                    break

    except FileNotFoundError:
        print(f"Ошибка: файл {script_path} не найден")


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

def main():
    """Главная функция эмулятора."""
    args = parse_argument()

    print(f"VFS: {args.vfs}")
    print(f"Script: {args.script}")

    vfs = None
    if args.vfs:
        vfs = load_vfs(args.vfs)
        if vfs:
            print(f"VFS загружена. Файлов: {len(vfs.namelist())}")

    if args.script:
        run_script(args.script)
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

        keep_going = execute_command(command, cmd_args)
        if not keep_going:
            break

if __name__ == "__main__":
    main()