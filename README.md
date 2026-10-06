# -IKBO-51-25-var15

Практическая работа по конфигурационному управлению. Вариант 15. Эмулятор оболочки ОС.

## Общее описание

Эмулятор командной строки UNIX-подобной ОС. Реализован на Python в виде консольного приложения (CLI). Поддерживает работу с виртуальной файловой системой (VFS), раскрытие переменных окружения и основные команды shell.

## Поддерживаемые команды

| Команда | Описание |
|---|---|
| `ls` | Список файлов и директорий |
| `cd` | Смена текущей директории |
| `rev` | Реверс строк |
| `find` | Поиск файлов |
| `du` | Размер файлов в директории |
| `exit` | Выход из эмулятора |

## Параметры командной строки

| Параметр | Описание |
|---|---|
| `--vfs <путь>` | Путь к физическому расположению VFS |
| `--script <путь>` | Путь к стартовому скрипту |

## Команды для сборки и запуска

```bash
# Запуск эмулятора
python src/main.py

# Запуск через скрипт
bash run.sh

# Запуск тестов
pytest tests/
```

## Примеры использования

### Работа с VFS

```
my_vfs> ls
file1.txt
file2.txt
readme.md
my_vfs> cd level1
Переход в: vfs_deep/level1/
my_vfs> ls
level2/
my_vfs> exit
Выход из эмулятора оболочки
```

### Раскрытие переменных окружения

```
my_vfs> echo $USERPROFILE
C:\Users\vital
```

### Обработка ошибок

```
my_vfs> hello
Ошибка: команда 'hello' не найдена.
my_vfs> cd nonexistent
Ошибка: директория 'nonexistent' не найдена
my_vfs> find
Ошибка: укажите имя файла
```

---

## Этап 2. Конфигурация

**Цель:** сделать эмулятор настраиваемым.

### Требование 1. Параметры командной строки

Реализованы параметры:
- `--vfs` — путь к VFS.
- `--script` — путь к стартовому скрипту.

**Проверка:**
```powershell
python src/main.py --vfs vfs/vfs.zip
python src/main.py --vfs vfs/vfs.zip --script scripts/startup.txt
python src/main.py --help
```

### Требование 2. Стартовый скрипт

Реализована функция `run_script`, которая читает файл и выполняет команды последовательно. Ошибочные строки пропускаются.

**Проверка:**
```powershell
python src/main.py --script scripts/startup.txt
```

### Требование 3. Отладочный вывод параметров

При запуске выводятся значения `VFS` и `Script`.

**Проверка:**
```powershell
python src/main.py --vfs vfs/vfs.zip --script scripts/startup.txt
```

### Требование 4. Скрипты реальной ОС

Созданы `.sh`-скрипты для Git Bash:
- `scripts/test1.sh` — без параметров.
- `scripts/test2.sh` — с `--vfs`.
- `scripts/test3.sh` — с `--vfs` и `--script`.

**Проверка (Git Bash):**
```bash
cd /c/Users/vital/-IKBO-51-25-var15
bash scripts/test1.sh
bash scripts/test2.sh
bash scripts/test3.sh
```

---

## Этап 3. VFS

**Цель:** подключить виртуальную файловую систему.

### Требование 1. Все операции в памяти

Реализована функция `load_vfs`, которая загружает ZIP-архив в память через `io.BytesIO`. На диск ничего не распаковывается.

**Проверка:**
```powershell
python src/main.py --vfs vfs/vfs.zip
```

### Требование 2. ZIP-архив + base64/аналог

Источник VFS — ZIP-архив. ZIP хранит двоичные данные напрямую (аналог base64).

### Требование 3. Скрипты для разных VFS

Созданы 3 ZIP-архива:
- `vfs/vfs_minimal.zip` — 1 файл.
- `vfs/vfs_files.zip` — 4 файла.
- `vfs/vfs_deep.zip` — 3 уровня вложенности.

Созданы `.ps1`-скрипты для PowerShell:
- `scripts/test_vfs1.ps1`
- `scripts/test_vfs2.ps1`
- `scripts/test_vfs3.ps1`

**Проверка (PowerShell):**
```powershell
.\scripts\test_vfs1.ps1
.\scripts\test_vfs2.ps1
.\scripts\test_vfs3.ps1
```

### Требование 4. Стартовый скрипт для всех команд

Обновлён `scripts/startup.txt` с примерами всех команд.

**Проверка:**
```powershell
python src/main.py --vfs vfs/vfs_minimal.zip --script scripts/startup.txt
```

---

## Этап 4. Основные команды

**Цель:** поддержать команды, имитирующие работу в UNIX-подобной командной строке.

### Требование 1. Логика для `ls` и `cd`

Реализованы функции:
- `cmd_ls` — выводит содержимое текущей директории.
- `cmd_cd` — меняет текущую директорию.

**Проверка:**
```powershell
python src/main.py --vfs vfs/vfs_deep.zip
```

**Команды:**
```
ls
cd level1
ls
cd level2
ls
cd level3
ls
cd nonexistent
cd
exit
```

### Требование 2. Команды `rev`, `find`, `du`

Реализованы функции:
- `cmd_rev` — реверс строки.
- `cmd_find` — поиск файла в VFS.
- `cmd_du` — размер файлов в текущей директории.

**Проверка:**
```powershell
python src/main.py --vfs vfs/vfs_files.zip
```

**Команды:**
```
rev hello
rev world
rev
find file1.txt
find nonexistent
find
du
exit
```

### Требование 3. Стартовый скрипт

Обновлён `scripts/startup.txt` со всеми командами Этапа 4.

**Проверка:**
```powershell
python src/main.py --vfs vfs/vfs_deep.zip --script scripts/startup.txt
```

---

## Структура репозитория

```
-IKBO-51-25-var15/
├── .gitignore
├── README.md
├── run.sh
├── src/
│   └── main.py
├── scripts/
│   ├── startup.txt
│   ├── test1.sh
│   ├── test2.sh
│   ├── test3.sh
│   ├── test_vfs1.ps1
│   ├── test_vfs2.ps1
│   └── test_vfs3.ps1
├── tests/
└── vfs/
    ├── vfs.zip
    ├── vfs_minimal.zip
    ├── vfs_files.zip
    └── vfs_deep.zip
```

---
