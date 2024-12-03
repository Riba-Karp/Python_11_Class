import json
import csv
from datetime import datetime, date

from notes import Note
from tasks import Task
from contacts import Contact
from finance import FinanceRecord

class PersonalAssistant:
    def __init__(self):
        self.notes = []
        self.tasks = []
        self.contacts = []
        self.finance_records = []
        self.load_data()

    def load_data(self):
        self.notes = self.load_json("notes.json", Note)
        self.tasks = self.load_json("tasks.json", Task)
        self.contacts = self.load_json("contacts.json", Contact)
        self.finance_records = self.load_json("finance.json", FinanceRecord)

    def save_data(self):
        self.save_json("notes.json", self.notes)
        self.save_json("tasks.json", self.tasks)
        self.save_json("contacts.json", self.contacts)
        self.save_json("finance.json", self.finance_records)

    def load_json(self, filename, cls):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    if not all(key in item for key in cls.__init__.__code__.co_varnames[1:]):
                        raise ValueError(f"Некорректная структура данных в файле {filename}")
                return [cls(**item) for item in data]
        except (FileNotFoundError, ValueError) as e:
            print(f"Ошибка при загрузке данных из {filename}: {e}")
            return []

    def save_json(self, filename, data):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([item.to_dict() for item in data], f, ensure_ascii=False, indent=4)

    # Заметки
    def add_note(self, title, content):
        note_id = len(self.notes) + 1
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.notes.append(Note(note_id, title, content, timestamp))
        self.save_data()

    def view_notes(self):
        for note in self.notes:
            print(f"ID: {note.id}, Заголовок: {note.title}, Дата: {note.timestamp}")

    def view_note_details(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                print(f"ID: {note.id}")
                print(f"Заголовок: {note.title}")
                print(f"Содержимое: {note.content}")
                print(f"Дата: {note.timestamp}")
                return
        print(f"Заметка с ID {note_id} не найдена.")

    def edit_note(self, note_id, new_title, new_content):
        for note in self.notes:
            if note.id == note_id:
                if new_title:
                    note.title = new_title
                if new_content:
                    note.content = new_content
                self.save_data()
                print(f"Заметка с ID {note_id} успешно отредактирована.")
                return
        print(f"Заметка с ID {note_id} не найдена.")

    def delete_note(self, note_id):
        for i, note in enumerate(self.notes):
            if note.id == note_id:
                del self.notes[i]
                self.save_data()
                print(f"Заметка с ID {note_id} успешно удалена.")
                return
        print(f"Заметка с ID {note_id} не найдена.")

    def export_notes_to_csv(self, file_name):
        with open(file_name, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'title', 'content', 'timestamp'])
            for note in self.notes:
                writer.writerow([note.id, note.title, note.content, note.timestamp])
        print(f"Заметки успешно экспортированы в {file_name}.")

    def import_notes_from_csv(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Пропустить заголовок
                for row in reader:
                    note_id = int(row[0])
                    title = row[1]
                    content = row[2]
                    timestamp = row[3]
                    self.notes.append(Note(note_id, title, content, timestamp))
            self.save_data()
            print(f"Заметки успешно импортированы из {file_name}.")
        except FileNotFoundError:
            print(f"Файл {file_name} не найден.")
        except Exception as e:
            print(f"Ошибка при импорте заметок из файла {file_name}: {e}")

    def notes_menu(self):
        while True:
            print("\nУправление заметками:")
            print("1. Добавить заметку")
            print("2. Просмотреть заметки")
            print("3. Назад")
            choice = input("Выберите действие: ")
            if choice == "1":
                title = input("Введите заголовок: ")
                content = input("Введите содержимое: ")
                self.add_note(title, content)
            elif choice == "2":
                self.view_notes()
            elif choice == "3":
                break

    # Задачи
    def add_task(self, title, description, priority, due_date):
        task_id = len(self.tasks) + 1
        self.tasks.append(Task(task_id, title, description, False, priority, due_date))
        self.save_data()

    def view_tasks(self):
        priority_mapping_reverse = {
            '1': "Высокий",
            '2': "Средний",
            '3': "Низкий"
        }
        for task in self.tasks:
            priority_str = priority_mapping_reverse.get(task.priority, "Средний")
            print(
                f"ID: {task.id}, Заголовок: {task.title}, Статус: {'Выполнено' if task.done else 'Не выполнено'}, Приоритет: {priority_str}")

    def mark_task_done(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.done = True
                self.save_data()
                print(f"Задача с ID {task_id} отмечена как выполненная.")
                return
        print(f"Задача с ID {task_id} не найдена.")

    def edit_task(self, task_id, new_title, new_description, new_priority, new_due_date):
        for task in self.tasks:
            if task.id == task_id:
                if new_title:
                    task.title = new_title
                if new_description:
                    task.description = new_description
                if new_priority:
                    task.priority = new_priority
                if new_due_date:
                    task.due_date = new_due_date
                self.save_data()
                print(f"Задача с ID {task_id} успешно отредактирована.")
                return
        print(f"Задача с ID {task_id} не найдена.")

    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.save_data()
                print(f"Задача с ID {task_id} успешно удалена.")
                return
        print(f"Задача с ID {task_id} не найдена.")

    def export_tasks_to_csv(self, file_name):
        with open(file_name, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'title', 'description', 'done', 'priority', 'due_date'])
            for task in self.tasks:
                writer.writerow([task.id, task.title, task.description, task.done, task.priority, task.due_date])
        print(f"Задачи успешно экспортированы в {file_name}.")

    def import_tasks_from_csv(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    task_id = int(row[0])
                    title = row[1]
                    description = row[2]
                    done = row[3].lower() == 'true'
                    priority = row[4]
                    due_date = row[5]
                    self.tasks.append(Task(task_id, title, description, done, priority, due_date))
            self.save_data()
            print(f"Задачи успешно импортированы из {file_name}.")
        except FileNotFoundError:
            print(f"Файл {file_name} не найден.")

    def tasks_menu(self):
        while True:
            print("\nУправление задачами:")
            print("1. Добавить задачу")
            print("2. Просмотреть задачи")
            print("3. Назад")
            choice = input("Выберите действие: ")
            if choice == "1":
                title = input("Введите заголовок: ")
                description = input("Введите описание: ")
                while True:
                    try:
                        priority = input("Введите приоритет (1 - Высокий, 2 - Средний, 3 - Низкий): ")
                        if priority in ["1", "2", "3"]:
                            break
                        else:
                            print("Неверный приоритет. Введите 1, 2 или 3.")
                    except ValueError:
                        print("Неверный ввод. Введите число.")

                priority = input("Введите приоритет (Высокий/Средний/Низкий): ")
                due_date = input("Введите срок выполнения (ДД-ММ-ГГГГ): ")
                self.add_task(title, description, priority, due_date)
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                break

    # Контакты
    def add_contact(self, name, phone, email):
        contact_id = len(self.contacts) + 1
        self.contacts.append(Contact(contact_id, name, phone, email))
        self.save_data()

    def search_contact(self, query):
        results = []
        for contact in self.contacts:
            if query.lower() in contact.name.lower() or query in contact.phone:
                results.append(contact)
        return results

    def view_contacts(self):
        for contact in self.contacts:
            print(f"ID: {contact.id}, Имя: {contact.name}, Телефон: {contact.phone}, Email: {contact.email}")

    def edit_contact(self, contact_id, new_name, new_phone, new_email):
        for contact in self.contacts:
            if contact.id == contact_id:
                if new_name:
                    contact.name = new_name
                if new_phone:
                    contact.phone = new_phone
                if new_email:
                    contact.email = new_email
                self.save_data()
                print(f"Контакт с ID {contact_id} успешно отредактирован.")
                return
            print(f"Контакт с ID {contact_id} не найден.")

    def delete_contact(self, contact_id):
        for i, contact in enumerate(self.contacts):
            if contact.id == contact_id:
                del self.contacts[i]
                self.save_data()
                print(f"Контакт с ID {contact_id} успешно удален.")
                return
        print(f"Контакт с ID {contact_id} не найден.")

    def export_contacts_to_csv(self, file_name):
        with open(file_name, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'name', 'phone', 'email'])
            for contact in self.contacts:
                writer.writerow([contact.id, contact.name, contact.phone, contact.email])
        print(f"Контакты успешно экспортированы в {file_name}.")

    def import_contacts_from_csv(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Пропустить заголовок
                for row in reader:
                    contact_id = int(row[0])
                    name = row[1]
                    phone = row[2]
                    email = row[3]
                    self.contacts.append(Contact(contact_id, name, phone, email))
            self.save_data()
            print(f"Контакты успешно импортированы из {file_name}.")
        except FileNotFoundError:
            print(f"Файл {file_name} не найден.")

    def contacts_menu(self):
        while True:
            print("\nУправление контактами:")
            print("1. Добавить контакт")
            print("2. Просмотреть контакты")
            print("3. Поиск контакта")
            print("4. Редактировать контакт")
            print("5. Удалить контакт")
            print("6. Экспорт контактов в CSV")
            print("7. Импорт контактов из CSV")
            print("8. Назад")
            choice = input("Выберите действие: ")
            if choice == "1":
                name = input("Введите имя: ")
                phone = input("Введите телефон: ")
                email = input("Введите email: ")
                self.add_contact(name, phone, email)
            elif choice == "2":
                self.view_contacts()
            elif choice == "3":
                query = input("Введите имя или номер телефона для поиска: ")
                results = self.search_contact(query)
                if results:
                    print("Найденные контакты:")
                    for contact in results:
                        print(
                            f"ID: {contact.id}, Имя: {contact.name}, Телефон: {contact.phone}, Email: {contact.email}")
                else:
                    print("Контакты не найдены.")
            elif choice == "4":  # Редактирование контакта
                contact_id = int(input("Введите ID контакта для редактирования: "))
                new_name = input("Введите новое имя (или оставьте пустым): ")
                new_phone = input("Введите новый телефон (или оставьте пустым): ")
                new_email = input("Введите новый email (или оставьте пустым): ")
                self.edit_contact(contact_id, new_name, new_phone, new_email)
            elif choice == "5":  # Удаление контакта
                contact_id = int(input("Введите ID контакта для удаления: "))
                self.delete_contact(contact_id)
            elif choice == "6":  # Экспорт контактов в CSV
                file_name = input("Введите имя файла для экспорта: ")
                self.export_contacts_to_csv(file_name)
            elif choice == "7":  # Импорт контактов из CSV
                file_name = input("Введите имя файла для импорта: ")
                self.import_contacts_from_csv(file_name)
            elif choice == "8":
                break

    # Финансы
    def add_finance_record(self, type, amount, category, date, description):
        record_id = len(self.finance_records) + 1
        self.finance_records.append(FinanceRecord(record_id, type, amount, category, date, description))
        self.save_data()

    def view_finance_records(self, date_filter=None, category_filter=None):
        filtered_records = self.finance_records
        if date_filter:
            filtered_records = [record for record in filtered_records if record.date == date_filter]

        if category_filter:
            filtered_records = [record for record in filtered_records if record.category == category_filter]
        for record in filtered_records:
            print(
                f"ID: {record.id}, Тип: {record.type}, Сумма: {record.amount}, Категория: {record.category}, Дата: {record.date}")

    def import_finance_records_from_csv(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Пропустить заголовок
                for row in reader:
                    record_id = int(row[0])
                    type = row[1]
                    try:
                        amount = float(row[2])
                    except ValueError:
                        continue
                    category = row[3]
                    date = row[4]
                    description = row[5] if len(row) > 5 else ""
                    self.finance_records.append(FinanceRecord(record_id, amount, category, date, description))
            self.save_data()
            print(f"Финансовые записи успешно импортированы из {file_name}.")
        except FileNotFoundError:
            print(f"Файл {file_name} не найден.")
        except Exception as e:
            print(f"Ошибка при импорте финансовых записей из файла {file_name}: {e}")

    def export_finance_records_to_csv(self, file_name):
        with open(file_name, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'amount', 'category', 'date', 'description'])
            for record in self.finance_records:
                writer.writerow([record.id, record.amount, record.category, record.date, record.description])
        print(f"Финансовые записи успешно экспортированы в {file_name}.")

    def finance_menu(self):
        while True:
            print("\nУправление финансовыми записями:")
            print("1. Добавить запись")
            print("2. Просмотреть записи")
            print("3. Генерация отчета")
            print("4. Экспорт в CSV")
            print("5. Импорт из CSV")
            print("6. Назад")
            choice = input("Выберите действие: ")
            if choice == "1":
                while True:
                    record_type = input("Введите тип записи (доход/расход): ").lower()
                    if record_type in ("доход", "расход"):
                        break
                    else:
                        print("Неверный тип записи. Введите 'доход' или 'расход'.")
                amount = float(input("Введите сумму: "))
                category = input("Введите категорию: ")
                date = input("Введите дату (ДД-ММ-ГГГГ): ")
                description = input("Введите описание: ")
                self.add_finance_record(record_type, amount, category, date, description)
            elif choice == "2":
                date_filter = input("Введите дату для фильтрации (ДД-ММ-ГГГГ, или оставьте пустым): ")
                category_filter = input("Введите категорию для фильтрации (или оставьте пустым): ")
                self.view_finance_records(date_filter, category_filter)
            elif choice == "3":
                start_date_str = input("Введите дату начала периода (ДД-ММ-ГГГГ): ")
                end_date_str = input("Введите дату окончания периода (ДД-ММ-ГГГГ): ")
                self.generate_report(start_date_str, end_date_str)
            elif choice == "4":
                file_name = input("Введите имя файла для экспорта: ")
                self.export_finance_records_to_csv(file_name)
            elif choice == "5":
                file_name = input("Введите имя файла для импорта: ")
                self.import_finance_records_from_csv(file_name)
            elif choice == "6":
                break

    def generate_report(self, start_date_str, end_date_str):
        try:
            start_date = datetime.strptime(start_date_str, "%d-%m-%Y").date()
            end_date = datetime.strptime(end_date_str, "%d-%m-%Y").date()
        except ValueError:
            print("Ошибка: неверный формат даты. Используйте формат ДД-ММ-ГГГГ.")
            return

        filtered_records = [
            record for record in self.finance_records
            if isinstance(record.date, date) and start_date <= record.date <= end_date
        ]

        filtered_records = filtered_records or []

        print(f"Отчет за период с {start_date} по {end_date}:")

        if filtered_records:
            for record in filtered_records:
                print(f"  {record.date}: {record.type} - {record.amount} ({record.category})")

            total_income = sum(record.amount for record in filtered_records if record.type == "доход")
            total_expense = sum(record.amount for record in filtered_records if record.type == "расход")
            balance = total_income - total_expense

            print(f"  Доходы: {total_income}")
            print(f"  Расходы: {total_expense}")
            print(f"  Баланс: {balance}")
        else:
            print("  Записи не найдены.")

    # Калькулятор
    def calculator(self):
        while True:
            try:
                expression = input("Введите выражение (или 'выход' для возврата): ")
                if expression.lower() == "выход":
                    break
                result = eval(expression)
                print(f"Результат: {result}")
            except Exception as e:
                print(f"Ошибка: {e}")

    def main_menu(self):
        while True:
            print("\nДобро пожаловать в Персональный помощник!")
            print("1. Управление заметками")
            print("2. Управление задачами")
            print("3. Управление контактами")
            print("4. Управление финансовыми записями")
            print("5. Калькулятор")
            print("6. Выход")
            choice = input("Выберите действие: ")
            if choice == "1":
                self.notes_menu()
            elif choice == "2":
                self.tasks_menu()
            elif choice == "3":
                self.contacts_menu()
            elif choice == "4":
                self.finance_menu()
            elif choice == "5":
                self.calculator()
            elif choice == "6":
                print("До свидания!")
                break
            else:
                print("Неверный выбор.")

    def notes_menu(self):
        while True:
            print("\nУправление заметками:")
            print("1. Добавить новую заметку")
            print("2. Просмотреть все заметки")
            print("3. Просмотреть подробности заметки")
            print("4. Редактировать заметку")
            print("5. Удалить заметку")
            print("6. Экспорт заметок в CSV")
            print("7. Импорт заметок из CSV")
            print("8. Назад")
            choice = input("Выберите действие: ")
            if choice == "1":
                title = input("Введите заголовок: ")
                content = input("Введите содержимое: ")
                self.add_note(title, content)
            elif choice == "2":
                self.view_notes()
            elif choice == "3":
                note_id = int(input("Введите ID заметки: "))
                self.view_note_details(note_id)
            elif choice == "4":
                note_id = int(input("Введите ID заметки: "))
                new_title = input("Введите новый заголовок (или оставьте пустым): ")
                new_content = input("Введите новое содержимое (или оставьте пустым): ")
                self.edit_note(note_id, new_title, new_content)
            elif choice == "5":
                note_id = int(input("Введите ID заметки: "))
                self.delete_note(note_id)
            elif choice == "6":
                file_name = input("Введите имя файла для экспорта: ")
                self.export_notes_to_csv(file_name)
            elif choice == "7":
                file_name = input("Введите имя файла для импорта: ")
                self.import_notes_from_csv(file_name)
            elif choice == "8":
                break
            else:
                print("Неверный выбор.")

    def tasks_menu(self):
        while True:
            print("\nУправление задачами:")
            print("1. Добавить новую задачу")
            print("2. Просмотреть все задачи")
            print("3. Отметить задачу как выполненную")
            print("4. Редактировать задачу")
            print("5. Удалить задачу")
            print("6. Экспорт задач в CSV")
            print("7. Импорт задач из CSV")
            print("8. Назад")
            choice = input("Выберите действие: ")
            if choice == "1":
                title = input("Введите заголовок: ")
                description = input("Введите описание: ")
                priority = input("Введите приоритет (Высокий/Средний/Низкий): ")
                due_date = input("Введите срок выполнения (ДД-ММ-ГГГГ): ")
                self.add_task(title, description, priority, due_date)
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                task_id = int(input("Введите ID задачи: "))
                self.mark_task_done(task_id)
            elif choice == "4":
                task_id = int(input("Введите ID задачи: "))
                new_title = input("Введите новый заголовок (или оставьте пустым): ")
                new_description = input("Введите новое описание (или оставьте пустым): ")
                new_priority = input("Введите новый приоритет (или оставьте пустым): ")
                new_due_date = input("Введите новый срок выполнения (или оставьте пустым): ")
                self.edit_task(task_id, new_title, new_description, new_priority, new_due_date)
            elif choice == "5":
                task_id = int(input("Введите ID задачи: "))
                self.delete_task(task_id)
            elif choice == "6":
                file_name = input("Введите имя файла для экспорта: ")
                self.export_tasks_to_csv(file_name)
            elif choice == "7":
                file_name = input("Введите имя файла для импорта: ")
                self.import_tasks_from_csv(file_name)
            elif choice == "8":
                break
            else:
                print("Неверный выбор.")
