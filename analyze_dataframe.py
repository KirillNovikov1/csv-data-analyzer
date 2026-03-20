from __future__ import annotations

from pathlib import Path
import argparse
import re

import matplotlib.pyplot as plt
import pandas as pd


OUTPUT_DIR_NAME = 'histograms'


def sanitize_filename(name: str) -> str:
    """Преобразует имя столбца в безопасное имя файла."""
    return re.sub(r'[^\w\-.]+', '_', str(name), flags=re.UNICODE).strip('_') or 'column'


def analyze_dataframe(file_path: str, show_plots: bool = True) -> dict:
    """Выполняет базовый анализ CSV-файла.

    Args:
        file_path: Путь к CSV-файлу.
        show_plots: Показывать ли гистограммы на экране.

    Returns:
        Словарь с общей информацией о файле, списком числовых столбцов,
        статистикой по каждому числовому столбцу и путями к сохранённым гистограммам.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f'Файл не найден: {file_path}')

    data = pd.read_csv(path)
    rows, cols = data.shape
    numeric_columns = data.select_dtypes(include='number').columns.tolist()

    print(f'Файл: {path.name}')
    print(f'Количество строк: {rows}')
    print(f'Количество столбцов: {cols}\n')

    print('Названия столбцов:')
    for column in data.columns:
        print(f'- {column}')

    print('\nЧисловые столбцы:')
    if numeric_columns:
        print(', '.join(map(str, numeric_columns)))
    else:
        print('Числовые столбцы не найдены.')

    output_dir = path.parent / OUTPUT_DIR_NAME
    output_dir.mkdir(exist_ok=True)

    statistics: dict[str, dict[str, float | int | None]] = {}
    histogram_files: list[str] = []

    for column in numeric_columns:
        series = data[column]
        column_stats = {
            'mean': round(series.mean(), 2) if not series.dropna().empty else None,
            'median': round(series.median(), 2) if not series.dropna().empty else None,
            'std': round(series.std(), 2) if not series.dropna().empty else None,
            'missing_values': int(series.isnull().sum()),
        }
        statistics[str(column)] = column_stats

        print(f'\nАНАЛИЗ СТОЛБЦА: {column}')
        print(f"Среднее значение: {column_stats['mean']}")
        print(f"Медиана: {column_stats['median']}")
        print(f"Стандартное отклонение: {column_stats['std']}")
        print(f"Пропусков: {column_stats['missing_values']}")

        plt.figure()
        plt.hist(series.dropna(), bins=30, edgecolor='black')
        plt.title(f'Гистограмма столбца {column}')
        plt.xlabel(str(column))
        plt.ylabel('Частота')
        plt.tight_layout()

        histogram_path = output_dir / f'histogram_{sanitize_filename(column)}.png'
        plt.savefig(histogram_path)
        histogram_files.append(str(histogram_path))

        if show_plots:
            plt.show()
        else:
            plt.close()

    return {
        'file_name': path.name,
        'rows': rows,
        'cols': cols,
        'columns': data.columns.tolist(),
        'numeric_columns': numeric_columns,
        'statistics': statistics,
        'histogram_files': histogram_files,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Базовый анализ CSV-файла.')
    parser.add_argument('file_path', help='Путь к CSV-файлу для анализа.')
    parser.add_argument(
        '--no-show',
        action='store_true',
        help='Не показывать графики на экране, только сохранить их в PNG.',
    )
    return parser


if __name__ == '__main__':
    args = build_parser().parse_args()
    result = analyze_dataframe(args.file_path, show_plots=not args.no_show)

    print('\nАнализ завершён.')
    print('Сохранено гистограмм:', len(result['histogram_files']))
