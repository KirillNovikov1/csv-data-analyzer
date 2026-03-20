# CSV Data Analyzer

Python-проект для базового анализа CSV-файлов.

Скрипт читает CSV-файл, показывает основную информацию о таблице, находит числовые столбцы, рассчитывает статистику по каждому из них и сохраняет гистограммы в отдельную папку.

## Возможности

- чтение CSV-файла через `pandas`;
- вывод количества строк и столбцов;
- вывод списка всех столбцов;
- автоматический поиск числовых столбцов;
- расчёт среднего значения, медианы, стандартного отклонения и количества пропусков;
- сохранение гистограмм в PNG;
- запуск из командной строки.

## Структура проекта

```text
csv-data-analyzer/
├── analyze_dataframe.py      # основной скрипт
├── learning_3_original.py    # исходная версия файла
├── requirements.txt          # зависимости проекта
├── .gitignore
└── README.md
```

После запуска рядом со скриптом автоматически создаётся папка `histograms/` со всеми построенными графиками.

## Установка

```bash
git clone <ссылка-на-репозиторий>
cd csv-data-analyzer
pip install -r requirements.txt
```

## Использование

Запуск из командной строки:

```bash
python analyze_dataframe.py your_file.csv
```

Если нужно только сохранить графики без показа окна с диаграммами:

```bash
python analyze_dataframe.py your_file.csv --no-show
```

## Пример использования в коде

```python
from analyze_dataframe import analyze_dataframe

result = analyze_dataframe('your_file.csv', show_plots=False)
print(result['statistics'])
```

## Что возвращает функция

Функция `analyze_dataframe(file_path, show_plots=True)` возвращает словарь со следующими данными:

- `file_name` — имя анализируемого файла;
- `rows` — количество строк;
- `cols` — количество столбцов;
- `columns` — список всех столбцов;
- `numeric_columns` — список числовых столбцов;
- `statistics` — статистика по каждому числовому столбцу;
- `histogram_files` — список путей к сохранённым гистограммам.

Пример структуры `statistics`:

```python
{
    'age': {
        'mean': 29.41,
        'median': 28.0,
        'std': 5.72,
        'missing_values': 2,
    }
}
```

