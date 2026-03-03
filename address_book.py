from collections import UserDict
from datetime import datetime
from typing import Any, Optional

from birthdays import get_upcoming_birthdays


class Field:
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str) -> None:
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str) -> None:
        if not value.isdigit() or len(value) != 10:
            raise ValueError(f"Phone number must contain exactly 10 digits, got: {value}")
        super().__init__(value)


class Birthday(Field):
    value: datetime

    def __init__(self, value: str) -> None:
        try:
            super().__init__(datetime.strptime(value, "%d.%m.%Y"))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Optional[Birthday] = None

    def add_phone(self, phone_number: str) -> None:
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)
        else:
            raise ValueError(f"Phone {phone_number} not found.")

    def edit_phone(self, old_number: str, new_number: str) -> None:
        phone = self.find_phone(old_number)
        if phone:
            phone.value = Phone(new_number).value
        else:
            raise ValueError(f"Phone {old_number} not found.")

    def find_phone(self, phone_number: str) -> Optional[Phone]:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday: str) -> None:
        """Додає або оновлює день народження контакту (формат DD.MM.YYYY)."""
        self.birthday = Birthday(birthday)

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones)
        birthday_str = str(self.birthday) if self.birthday else "—"
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones_str}, "
            f"birthday: {birthday_str}"
        )


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Record '{name}' not found.")

    def get_upcoming_birthdays(self) -> list[dict]:
        """
        Повертає список контактів із днями народження протягом наступних 7 днів.
        Використовує get_upcoming_birthdays() з модуля birthdays.
        """
        users = []
        for record in self.data.values():
            if record.birthday:
                users.append({
                    "name": record.name.value,
                    "birthday": record.birthday.value.strftime("%Y.%m.%d"),
                })
        return get_upcoming_birthdays(users)


if __name__ == '__main__':
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("15.04.1990")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("20.05.1992")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")

    # Виведення найближчих днів народження
    upcoming_birthdays = book.get_upcoming_birthdays()
    print("Upcoming birthdays:", upcoming_birthdays)
