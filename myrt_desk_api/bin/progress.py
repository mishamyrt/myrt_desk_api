"""Progress utils"""
from os import get_terminal_size

FILL = '█'
END = '\r'
TOTAL = 100.0

def print_progress (iteration: float) -> None:
    """Prints progress to stdout"""
    (columns, _) = get_terminal_size()
    length = columns - 9
    percent = (f"{100 * (iteration / TOTAL):.1f}")
    filled_length = int(length * iteration // TOTAL)
    fill_bar = FILL * filled_length + '-' * (length - filled_length)
    print(f'{END}|{fill_bar}| {percent}%', end=END)
    if iteration == TOTAL:
        print()
