import csv
import os
from typing import List, Optional


def process_csv(input_file: str, output_file: str, mode: str,
                 search_words: Optional[List[str]] = None, match_mode: str = "any",
                 encoding: str = "utf-8", delimiter: str = ","):
    """
    Обрабатывает CSV файл в одном из двух режимов:

    mode == "search":
        Ищет строки, содержащие искомые слова (search_words), и сохраняет
        уникальные (не повторяющиеся полностью) найденные строки в output_file.
        match_mode:
            "any" - строка подходит, если есть ХОТЯ БЫ ОДНО слово из списка (ИЛИ)
            "all" - строка подходит, только если есть ВСЕ слова сразу (И)

    mode == "dedup":
        Просто копирует весь файл в output_file, убирая полностью
        одинаковые (дублирующиеся) строки, без какого-либо поиска.
    """
    seen_rows = set()
    found_count = 0
    skipped_duplicates = 0

    with open(input_file, "r", encoding=encoding, newline="") as infile, \
         open(output_file, "w", encoding=encoding, newline="") as outfile:

        reader = csv.reader(infile, delimiter=delimiter)
        writer = csv.writer(outfile, delimiter=delimiter)

        # Считываем и сразу записываем заголовок таблицы (первую строку),
        # чтобы в результате было видно, какая колонка за что отвечает
        header = next(reader, None)
        if header is not None:
            writer.writerow(header)

        if mode == "search" and not search_words:
            raise ValueError("Для режима поиска нужно передать хотя бы одно слово в search_words")

        for row in reader:
            if mode == "search":
                # Собираем строку в одну для поиска текста
                row_as_text = delimiter.join(row).lower()
                words_lower = [w.lower() for w in search_words]

                if match_mode == "all":
                    matched = all(w in row_as_text for w in words_lower)
                else:  # "any"
                    matched = any(w in row_as_text for w in words_lower)

                if not matched:
                    continue

            # Ключ для проверки дубликатов - кортеж из значений строки
            row_key = tuple(row)

            if row_key in seen_rows:
                skipped_duplicates += 1
                continue

            seen_rows.add(row_key)
            writer.writerow(row)
            found_count += 1

    print("\nГотово!")
    if mode == "search":
        print(f"Найдено уникальных строк: {found_count}")
    else:
        print(f"Сохранено уникальных строк (без учёта заголовка): {found_count}")
    print(f"Пропущено дубликатов: {skipped_duplicates}")
    print(f"Результат сохранён в: {output_file}")


def ask_input_file():
    while True:
        path = input("Введите путь к исходному CSV файлу: ").strip().strip('"')
        if os.path.isfile(path):
            return path
        print(f"Файл не найден: {path}\nПопробуйте ещё раз.\n")


def ask_output_file():
    path = input("Введите путь для сохранения результата (например, result.csv): ").strip().strip('"')
    return path or "result.csv"


def ask_encoding_and_delimiter():
    encoding = input("Кодировка файлов (Enter — по умолчанию utf-8): ").strip() or "utf-8"
    delimiter = input("Разделитель CSV (Enter — по умолчанию ','): ").strip() or ","
    return encoding, delimiter


if __name__ == "__main__":
    print("=== Обработка CSV файла ===\n")
    print("Выберите режим работы:")
    print("  1 - Поиск строк по слову/словам")
    print("  2 - Просто убрать дубликаты по всему файлу (без поиска)")

    while True:
        mode_choice = input("Ваш выбор (1/2): ").strip()
        if mode_choice in ("1", "2"):
            break
        print("Введите 1 или 2.\n")

    input_file = ask_input_file()
    output_file = ask_output_file()

    if mode_choice == "1":
        # Запрос слов для поиска
        raw_words = input(
            "Введите слово(-а) для поиска через запятую (например: Москва, Одесса): "
        ).strip()
        search_words = [w.strip() for w in raw_words.split(",") if w.strip()]

        while not search_words:
            raw_words = input("Список пуст. Введите хотя бы одно слово: ").strip()
            search_words = [w.strip() for w in raw_words.split(",") if w.strip()]

        match_mode = "any"
        if len(search_words) > 1:
            print("\nКак искать несколько слов?")
            print("  1 - Достаточно ХОТЯ БЫ ОДНОГО слова (ИЛИ)")
            print("  2 - Строка должна содержать ВСЕ слова сразу (И)")
            while True:
                logic_choice = input("Ваш выбор (1/2): ").strip()
                if logic_choice in ("1", "2"):
                    match_mode = "any" if logic_choice == "1" else "all"
                    break
                print("Введите 1 или 2.\n")

        encoding, delimiter = ask_encoding_and_delimiter()
        print()
        process_csv(input_file, output_file, mode="search", search_words=search_words,
                    match_mode=match_mode, encoding=encoding, delimiter=delimiter)

    else:
        encoding, delimiter = ask_encoding_and_delimiter()
        print()
        process_csv(input_file, output_file, mode="dedup",
                    encoding=encoding, delimiter=delimiter)
