import csv
import os


def search_csv(input_file, output_file, search_text, encoding="utf-8", delimiter=","):
    """
    Ищет строки, содержащие search_text, в input_file и сохраняет
    уникальные (не повторяющиеся полностью) найденные строки в output_file.
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

        for row in reader:
            # Собираем строку в одну для проверки на совпадение и для поиска текста
            row_as_text = delimiter.join(row)

            if search_text.lower() in row_as_text.lower():
                # Ключ для проверки дубликатов - кортеж из значений строки
                row_key = tuple(row)

                if row_key in seen_rows:
                    skipped_duplicates += 1
                    continue

                seen_rows.add(row_key)
                writer.writerow(row)
                found_count += 1

    print(f"Готово!")
    print(f"Найдено уникальных строк: {found_count}")
    print(f"Пропущено дубликатов: {skipped_duplicates}")
    print(f"Результат сохранён в: {output_file}")


if __name__ == "__main__":
    print("=== Поиск строк в CSV файле ===\n")

    # Запрос пути к исходному файлу
    while True:
        input_file = input("Введите путь к исходному CSV файлу: ").strip().strip('"')
        if os.path.isfile(input_file):
            break
        print(f"Файл не найден: {input_file}\nПопробуйте ещё раз.\n")

    # Запрос пути к файлу результата
    output_file = input("Введите путь для сохранения результата (например, result.csv): ").strip().strip('"')
    if not output_file:
        output_file = "result.csv"

    # Запрос текста для поиска
    while True:
        search_text = input("Введите текст/слово для поиска: ").strip()
        if search_text:
            break
        print("Текст для поиска не может быть пустым.\n")

    # Необязательные параметры с значениями по умолчанию
    encoding = input("Кодировка файлов (Enter — по умолчанию utf-8): ").strip() or "utf-8"
    delimiter = input("Разделитель CSV (Enter — по умолчанию ','): ").strip() or ","

    print()
    search_csv(input_file, output_file, search_text, encoding=encoding, delimiter=delimiter)
