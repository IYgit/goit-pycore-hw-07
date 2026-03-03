"""
Бот-асистент для управління адресною книгою.

Підтримувані команди:
  add [ім'я] [телефон]              — додати контакт або телефон
  change [ім'я] [старий] [новий]   — змінити телефон
  phone [ім'я]                      — показати телефони
  all                               — показати всі контакти
  add-birthday [ім'я] [DD.MM.YYYY]  — додати дату народження
  show-birthday [ім'я]              — показати дату народження
  birthdays                         — дні народження на наступні 7 днів
  hello                             — привітання
  close / exit                      — вийти
"""

from address_book import AddressBook, Record


# ──────────────────────────── Decorator ────────────────────────────

def input_error(func):
    """Декоратор для перехоплення типових помилок введення."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError, KeyError) as e:
            return str(e)
    return wrapper


# ──────────────────────────── Helpers ────────────────────────────

def parse_input(user_input: str) -> tuple[str, list[str]]:
    """Розбирає рядок введення на команду та список аргументів."""
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


# ──────────────────────────── Handlers ────────────────────────────

@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """Додає новий контакт або телефон до існуючого."""
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    """Змінює старий телефон на новий для вказаного контакту."""
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found.")
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    """Показує всі телефони вказаного контакту."""
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found.")
    if not record.phones:
        return f"{name} has no phones."
    return "; ".join(p.value for p in record.phones)


@input_error
def show_all(args: list[str], book: AddressBook) -> str:
    """Повертає всі контакти адресної книги."""
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    """Додає або оновлює день народження контакту."""
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found.")
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    """Показує день народження вказаного контакту."""
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found.")
    if record.birthday is None:
        return f"{name} has no birthday set."
    return str(record.birthday)


@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    """Показує контакти, яких потрібно привітати протягом наступних 7 днів."""
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next 7 days."
    lines = [f"{item['name']}: {item['congratulation_date']}" for item in upcoming]
    return "\n".join(lines)


# ──────────────────────────── Main ────────────────────────────

def main() -> None:
    """Головний цикл бота-асистента."""
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if not command:
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
