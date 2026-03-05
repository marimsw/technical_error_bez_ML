import pandas as pd
import re


def create_technical_errors_file(input_file, output_file):
    """
    Создает новый файл только с записями, содержащими варианты "техническая ошибка",
    и меняет значение в столбце 'группа' на "техническая ошибка"
    """

    # Регулярное выражение для поиска всех вариантов "техническая ошибка"
    pattern = re.compile(
        r'техническ[а-я]+\s+ошибк[а-я]+|ошибк[а-я]+\s+техническ[а-я]+',
        re.IGNORECASE | re.UNICODE
    )

    try:
        # Читаем Excel файл
        print(f"Чтение файла: {input_file}")
        df = pd.read_excel(input_file)

        # Проверяем наличие необходимых столбцов
        required_columns = ['текст_ответа', 'группа']
        for col in required_columns:
            if col not in df.columns:
                print(f"Ошибка: В файле отсутствует столбец '{col}'")
                print(f"Доступные столбцы: {', '.join(df.columns)}")
                return

        # Применяем фильтр к столбцу 'текст_ответа'
        text_responses = df['текст_ответа'].fillna('').astype(str)

        # Создаем маску для строк, содержащих варианты "техническая ошибка"
        mask = text_responses.apply(lambda x: bool(pattern.search(x)))

        # Применяем маску
        filtered_df = df[mask].copy()  # .copy() чтобы избежать предупреждений

        # Изменяем значение в столбце 'группа' на "техническая ошибка"
        filtered_df['группа'] = 'техническая ошибка'

        # Сохраняем результат
        filtered_df.to_excel(output_file, index=False)

        # Выводим статистику
        total_rows = len(df)
        filtered_rows = len(filtered_df)

        print(f"\nРезультаты:")
        print(f"Всего строк в исходном файле: {total_rows}")
        print(f"Найдено строк с 'техническая ошибка' и вариантами: {filtered_rows}")
        print(f"\nНовый файл сохранен: {output_file}")
        print(f"В столбце 'группа' всем строкам присвоено значение: 'техническая ошибка'")

        # Показываем примеры найденных записей
        if filtered_rows > 0:
            print("\nПримеры найденных записей (первые 5):")
            examples = filtered_df[['id_заявки', 'текст_ответа', 'группа']].head(5)
            for idx, row in examples.iterrows():
                text = str(row['текст_ответа'])[:80] + "..." if len(str(row['текст_ответа'])) > 80 else str(
                    row['текст_ответа'])
                print(f"ID: {row['id_заявки']} | Группа: {row['группа']} | Текст: {text}")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


def main():
    # Настройки
    input_file = input('Введите имя файла который изначальный: ')  # Исходный файл
    output_file = "technical_errors_only.xlsx"  # Новый файл только с техническими ошибками

    create_technical_errors_file(input_file, output_file)


if __name__ == "__main__":
    main()
