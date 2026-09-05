import random
import time


def validate_board(numbers):
  if len(numbers) != 25:
    raise ValueError("Enter exactly 25 numbers.")
  if any(number < 1 or number > 25 for number in numbers):
    raise ValueError("Every number must be between 1 and 25.")
  if len(set(numbers)) != 25:
    raise ValueError("Each number must be used only once.")


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


class BingoGame:
  def __init__(self, board):
    validate_board(board)
    self.board = board
    self.called_numbers = set()
    self.numbers_to_call = list(range(1, 26))
    random.shuffle(self.numbers_to_call)

  def call_number(self):
    if not self.numbers_to_call:
      return None
    number = self.numbers_to_call.pop()
    self.called_numbers.add(number)
    return number

  def state(self, latest=None):
    return {
      "board": self.board,
      "called": list(self.called_numbers),
      "latest": latest,
      "bingo": has_bingo(self.board, self.called_numbers),
      "finished": not self.numbers_to_call,
    }


if __name__ == "__main__":
  board = get_board()
  if board is None:
    print("Thanks for playing!")
  else:
    game = BingoGame(board)
    while game.numbers_to_call:
      show_board(game.board, game.called_numbers)
      next_number = game.call_number()
      print(f"\nLatest called number: {next_number}")

      if has_bingo(game.board, game.called_numbers):
        show_board(game.board, game.called_numbers)
        print("BINGO!")
        break

      time.sleep(1)
    else:
      show_board(game.board, game.called_numbers)
      print("All numbers have been called!")