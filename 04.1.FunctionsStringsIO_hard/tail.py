import sys
import typing as tp
from pathlib import Path


def tail(filename: Path, lines_amount: int = 10, output: tp.IO[bytes] | None = None) -> None:
    if output is None:
        output = sys.stdout.buffer

    if lines_amount <= 0:
        return

    chunk_size = 8192
    buf = bytearray(chunk_size)

    with open(filename, 'rb') as f:
        f.seek(0, 2)
        file_size = f.tell()

        if file_size == 0:
            return

        f.seek(file_size - 1)
        ends_with_newline = (f.read(1) == b'\n')
        target = lines_amount + (1 if ends_with_newline else 0)

        newlines_found = 0
        pos = file_size
        start = 0
        found = False

        while pos > 0 and not found:
            read_size = min(chunk_size, pos)
            pos -= read_size
            f.seek(pos)
            n = f.readinto(memoryview(buf)[:read_size])
            mv = memoryview(buf)[:n]
            for i in range(n - 1, -1, -1):
                if mv[i] == 10:
                    newlines_found += 1
                    if newlines_found == target:
                        start = pos + i + 1
                        found = True
                        break

        f.seek(start)
        remaining = file_size - start
        while remaining > 0:
            to_read = min(chunk_size, remaining)
            n = f.readinto(memoryview(buf)[:to_read])
            output.write(memoryview(buf)[:n])
            remaining -= n
