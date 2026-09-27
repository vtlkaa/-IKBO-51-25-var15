"""Модуль эмулятора оболочки ОС."""
import os

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

def main():
    print("Добро пожаловать в эмулятор оболочки!")
    user_vfs = "my_vfs"

    while True:

        user_input = input(f"{user_vfs}> ")
        expanded = expand_var(user_input)
        command, args = parse_command(expanded)

        if command is None:
            print("Пустая команда.")
        elif command == "exit":
            print("Выход из эмулятора оболочки.")
            break
        elif command in ["ls", "cd"]:
            print(f"Заглушка - Команда: {command}")
            print(f"Заглушка - Аргументы: {args}")
        else:
            print(f"Ошибка: команда '{command}' не найдена.")

if __name__ == "__main__":
    main()