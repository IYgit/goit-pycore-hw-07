"""
Модуль для визначення майбутніх днів народження колег.
"""

from datetime import datetime, timedelta
from typing import List, TypedDict


def get_upcoming_birthdays(users: List[dict[str, str]]) -> List[dict[str, str]]:
    """
    Визначає, кого з колег потрібно привітати з днем народження протягом наступних 7 днів.

    Функція аналізує дні народження користувачів і визначає, чиї дні народження
    випадають на найближчі 7 днів включно з поточним днем. Якщо день народження
    припадає на вихідний (субота або неділя), дата привітання переноситься
    на наступний понеділок.

    Args:
        users (list): Список словників з інформацією про користувачів.
                     Кожен словник має ключі:
                     - 'name' (str): ім'я користувача
                     - 'birthday' (str): дата народження у форматі 'РРРР.ММ.ДД'

    Returns:
        list: Список словників з інформацією про привітання.
              Кожен словник містить:
              - 'name' (str): ім'я користувача
              - 'congratulation_date' (str): дата привітання у форматі 'РРРР.ММ.ДД'

    Examples:
        >>> users = [
        ...     {"name": "John Doe", "birthday": "1985.01.23"},
        ...     {"name": "Jane Smith", "birthday": "1990.01.27"}
        ... ]
        >>> # Якщо сьогодні 2024.01.22
        >>> result = get_upcoming_birthdays(users)
        >>> len(result)
        2
    """
    # Отримуємо поточну дату (без часу)
    today = datetime.today().date()

    # Список для зберігання результатів
    upcoming_birthdays = []

    # Проходимо по кожному користувачу
    for user in users:
        # Конвертуємо дату народження із рядка у datetime об'єкт
        birthday_date = datetime.strptime(user["birthday"], "%Y.%m.%d").date()

        # Отримуємо день народження в поточному році.
        # Обробляємо випадок 29 лютого: якщо поточний рік не високосний,
        # святкування переноситься на 1 березня.
        try:
            birthday_this_year = birthday_date.replace(year=today.year)
        except ValueError:
            # 29 лютого у не-високосному році → переносимо на 1 березня
            birthday_this_year = birthday_date.replace(year=today.year, month=3, day=1)

        # Якщо день народження вже минув цього року, беремо наступний рік
        if birthday_this_year < today:
            try:
                birthday_this_year = birthday_date.replace(year=today.year + 1)
            except ValueError:
                # 29 лютого у не-високосному наступному році → 1 березня
                birthday_this_year = birthday_date.replace(year=today.year + 1, month=3, day=1)

        # Обчислюємо різницю в днях між днем народження і поточною датою
        days_until_birthday = (birthday_this_year - today).days

        # Перевіряємо, чи день народження в найближчі 7 днів (включно з сьогодні)
        if 0 <= days_until_birthday <= 7:
            # Визначаємо дату привітання
            congratulation_date = birthday_this_year

            # Перевіряємо, чи день народження припадає на вихідний
            # weekday(): 0 = понеділок, 5 = субота, 6 = неділя
            weekday = congratulation_date.weekday()

            if weekday == 5:  # Субота
                # Переносимо на понеділок (додаємо 2 дні)
                congratulation_date += timedelta(days=2)
            elif weekday == 6:  # Неділя
                # Переносимо на понеділок (додаємо 1 день)
                congratulation_date += timedelta(days=1)

            # Додаємо до списку результатів
            upcoming_birthdays.append({
                "name": user["name"],
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
            })

    return upcoming_birthdays


# Приклади використання
if __name__ == "__main__":
    print("=" * 70)
    print("Система привітань з днем народження")
    print("=" * 70)

    # Поточна дата
    today = datetime.today().date()
    print(f"\nПоточна дата: {today.strftime('%Y.%m.%d')} ({today.strftime('%A')})")

    # Приклад 1: Тестові дані з завдання
    print("\n" + "-" * 70)
    print("Приклад 1: Дні народження на цьому тижні")
    print("-" * 70)

    users = [
        {"name": "John Doe", "birthday": "1985.01.23"},
        {"name": "Jane Smith", "birthday": "1990.01.27"}
    ]

    print("\nСписок користувачів:")
    for user in users:
        print(f"  - {user['name']}: {user['birthday']}")

    upcoming_birthdays = get_upcoming_birthdays(users)
    print("\nСписок привітань на цьому тижні:")
    if upcoming_birthdays:
        for item in upcoming_birthdays:
            print(f"  - {item['name']}: {item['congratulation_date']}")
    else:
        print("  Немає днів народження на наступні 7 днів")

    # Приклад 2: Розширений тест з різними випадками
    print("\n" + "-" * 70)
    print("Приклад 2: Розширений тест")
    print("-" * 70)

    # Створюємо тестові дані відносно поточної дати
    extended_users = [
        {"name": "Олександр", "birthday": f"1990.{today.strftime('%m.%d')}"},  # Сьогодні
        {"name": "Марія", "birthday": f"1985.{(today + timedelta(days=1)).strftime('%m.%d')}"},  # Завтра
        {"name": "Петро", "birthday": f"1988.{(today + timedelta(days=3)).strftime('%m.%d')}"},  # Через 3 дні
        {"name": "Анна", "birthday": f"1992.{(today + timedelta(days=6)).strftime('%m.%d')}"},  # Через 6 днів
        {"name": "Іван", "birthday": f"1987.{(today + timedelta(days=8)).strftime('%m.%d')}"},  # Через 8 днів (не повинен потрапити)
        {"name": "Ольга", "birthday": f"1995.{(today - timedelta(days=1)).strftime('%m.%d')}"},  # Вчора (не повинен потрапити)
    ]

    print("\nСписок користувачів:")
    for user in extended_users:
        birth_date = datetime.strptime(user['birthday'], "%Y.%m.%d").date()
        days_diff = (birth_date.replace(year=today.year) - today).days
        if birth_date.replace(year=today.year) < today:
            days_diff = (birth_date.replace(year=today.year + 1) - today).days
        print(f"  - {user['name']}: {user['birthday']} (через {days_diff} днів)")

    upcoming_birthdays = get_upcoming_birthdays(extended_users)
    print("\nСписок привітань на наступні 7 днів:")
    if upcoming_birthdays:
        for item in upcoming_birthdays:
            congrat_date = datetime.strptime(item['congratulation_date'], "%Y.%m.%d").date()
            print(f"  - {item['name']}: {item['congratulation_date']} ({congrat_date.strftime('%A')})")
    else:
        print("  Немає днів народження на наступні 7 днів")

    # Приклад 3: Тест з вихідними днями
    print("\n" + "-" * 70)
    print("Приклад 3: День народження на вихідних")
    print("-" * 70)

    # Знаходимо найближчу суботу
    days_until_saturday = (5 - today.weekday()) % 7
    if days_until_saturday == 0:
        days_until_saturday = 7  # Якщо сьогодні субота, беремо наступну
    next_saturday = today + timedelta(days=days_until_saturday)
    next_sunday = next_saturday + timedelta(days=1)

    weekend_users = [
        {"name": "Дмитро", "birthday": f"1993.{next_saturday.strftime('%m.%d')}"},  # Субота
        {"name": "Світлана", "birthday": f"1991.{next_sunday.strftime('%m.%d')}"},  # Неділя
    ]

    print("\nСписок користувачів з днями народження на вихідних:")
    for user in weekend_users:
        birth_date = datetime.strptime(user['birthday'], "%Y.%m.%d").date()
        birth_this_year = birth_date.replace(year=today.year)
        if birth_this_year < today:
            birth_this_year = birth_date.replace(year=today.year + 1)
        print(f"  - {user['name']}: {user['birthday']} ({birth_this_year.strftime('%A')})")

    upcoming_birthdays = get_upcoming_birthdays(weekend_users)
    print("\nПривітання перенесені на робочий день:")
    if upcoming_birthdays:
        for item in upcoming_birthdays:
            congrat_date = datetime.strptime(item['congratulation_date'], "%Y.%m.%d").date()
            print(f"  - {item['name']}: {item['congratulation_date']} ({congrat_date.strftime('%A')})")
    else:
        print("  Немає днів народження на наступні 7 днів")

    # Приклад 4: Тест з датою народження 29 лютого
    print("\n" + "-" * 70)
    print("Приклад 4: День народження 29 лютого (високосна дата)")
    print("-" * 70)

    leap_users = [
        {"name": "Василь Стрибок", "birthday": "2000.02.29"},  # реальна дата 29.02
    ]

    print("\nСписок користувачів:")
    for user in leap_users:
        print(f"  - {user['name']}: {user['birthday']}")

    print(f"\nЦей рік ({today.year}) ", end="")
    import calendar
    if calendar.isleap(today.year):
        print("є високосним → привітання 29 лютого")
    else:
        print("НЕ є високосним → привітання переноситься на 1 березня")

    upcoming_birthdays = get_upcoming_birthdays(leap_users)

    # Для наочності перевіряємо всі наступні 365 днів, щоб точно знайти дату
    # (29.02 може не потрапляти в поточні 7 днів, тому покажемо очікувану дату окремо)
    from datetime import date
    check_year = today.year
    try:
        expected_date = date(check_year, 2, 29)
    except ValueError:
        expected_date = date(check_year, 3, 1)
    if expected_date < today:
        check_year += 1
        try:
            expected_date = date(check_year, 2, 29)
        except ValueError:
            expected_date = date(check_year, 3, 1)
    # Перенесення на понеділок, якщо вихідний
    if expected_date.weekday() == 5:
        expected_date += timedelta(days=2)
    elif expected_date.weekday() == 6:
        expected_date += timedelta(days=1)

    print(f"Очікувана дата привітання: {expected_date.strftime('%Y.%m.%d')} ({expected_date.strftime('%A')})")

    if upcoming_birthdays:
        print("\nПривітання потрапило в найближчі 7 днів:")
        for item in upcoming_birthdays:
            congrat_date = datetime.strptime(item['congratulation_date'], "%Y.%m.%d").date()
            print(f"  - {item['name']}: {item['congratulation_date']} ({congrat_date.strftime('%A')})")
    else:
        print("  День народження не в найближчі 7 днів.")

    print("\n" + "=" * 70)



