import sys
import typing as tp
from pathlib import Path


def tail(filename: Path, lines_amount: int = 10, output: tp.IO[bytes] | None = None) -> None:
    if output is None:
        output = sys.stdout.buffer

    if lines_amount <= 0:
        return

    with open(filename, 'rb') as f:
        lines = f.readlines()

    start_index = max(0, len(lines) - lines_amount)
    
    for line in lines[start_index:]:
        # Нормализуем переносы строк: заменяем \r\n на \n для кроссплатформенности
        output.write(line.replace(b'\r\n', b'\n'))
