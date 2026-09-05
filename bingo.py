import random
import time


def get_board():
  print("Welcome to Python Text Bingo!")
  print("Enter 25 different numbers from 1 to 25.")

  numbers = []
  while len(numbers) < 25:
    remaining = 25 - len(numbers)
    entry = input(f"Enter {remaining} number(s), separated by spaces: ").strip()
    if entry.lower() == "q":
      return None

    try:
      new_numbers = [int(value) for value in entry.split()]
    except ValueError:
      print("Please enter whole numbers only.")
      continue

    if any(number < 1 or number > 25 for number in new_numbers):
      print("Every number must be between 1 and 25.")
      continue
    if len(numbers) + len(new_numbers) > 25:
      print(f"You only need {remaining} more number(s).")
      continue
    if len(set(new_numbers)) != len(new_numbers) or set(new_numbers) & set(numbers):
      print("Each number must be used only once.")
      continue

    numbers.extend(new_numbers)

  return numbers


def show_board(board, called_numbers):
  print("\n" + "=" * 32)
  print("          BINGO CARD")
  print("=" * 32)
  for row in range(5):
    cells = []
    for column in range(5):
      number = board[row * 5 + column]
      cells.append("[--]" if number in called_numbers else f"[{number:2d}]")
    print(" ".join(cells))
  print("=" * 32)


def has_bingo(board, called_numbers):
  lines = []
  lines.extend(board[row * 5:(row + 1) * 5] for row in range(5))
  lines.extend(board[column::5] for column in range(5))
  lines.append(board[0::6])
  lines.append(board[4::4])
  return any(all(number in called_numbers for number in line) for line in lines)


board = get_board()
if board is None:
  print("Thanks for playing!")
else:
  called_numbers = set()
  numbers_to_call = list(range(1, 26))
  random.shuffle(numbers_to_call)

  while numbers_to_call:
    show_board(board, called_numbers)
    next_number = numbers_to_call.pop()
    called_numbers.add(next_number)
    print(f"\nLatest called number: {next_number}")

    if has_bingo(board, called_numbers):
      show_board(board, called_numbers)
      print("BINGO!")
      break

    time.sleep(1)
  else:
    show_board(board, called_numbers)
    print("All numbers have been called!")