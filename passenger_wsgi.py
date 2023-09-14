import telebot
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 
import hashlib

# Ваш токен бота
TOKEN = '6692758440:AAHQwcdQiUXX9QfLRZaMyFxrrX8Q2bIo2sg'

# Створення об'єкту бота
bot = telebot.TeleBot(TOKEN)

# Список адміністраторів (ви можете додавати інші ідентифікатори користувачів)
admins = [5465901451, 5641289225, 5149489797, 5451869956]  # Замініть ці ідентифікатори на свої

# Шлях до файлу, який ви хочете відстежувати
file_path_to_watch = '/home/whitever/public_html/details/result.log'  # Змінено назву змінної

# Змінна для збереження попереднього хеша файла
previous_hash = None

# Змінна для збереження попереднього вмісту файла
previous_content = None

# Клас для обробки змін файлу
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global previous_hash, previous_content  # Оголошуємо, що будемо використовувати глобальні змінні
        # Перевіряємо, чи це файл, який нас цікавить
        if event.src_path == file_path_to_watch:
            # Отримуємо хеш поточної версії файла
            current_hash = get_file_hash(file_path_to_watch)
            # Порівнюємо хеш поточної версії з попереднім хешем
            if current_hash != previous_hash:
                # Отримуємо текст змін в файлі
                with open(file_path_to_watch, 'r') as file:
                    current_content = file.read()
                # Знаходимо різницю між поточним та попереднім вмістом
                diff = find_text_difference(previous_content, current_content)
                # Відправляємо повідомлення адміну зі змінами
                for admin_id in admins:
                    bot.send_message(admin_id, f"Знайдено зміни у файлі:\n{diff}")
                # Оновлюємо попередній хеш і вміст
                previous_hash = current_hash
                previous_content = current_content

def get_file_hash(file_path):
    # Обчислюємо хеш файла за допомогою SHA-256
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

def find_text_difference(previous_text, current_text):
    # Знаходимо різницю між попереднім і поточним текстом
    # Наприклад, можна використовувати бібліотеку difflib
    import difflib
    d = difflib.Differ()
    diff = list(d.compare(previous_text.splitlines(), current_text.splitlines()))
    return '\n'.join(line for line in diff if line.startswith('+ '))

# Початковий вміст файлу
with open(file_path_to_watch, 'r') as file:
    previous_content = file.read()





# Додайте код для перевірки файлу та відправки його користувачам тут

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in admins:
        bot.send_message(message.chat.id, "Ви адміністратор бота і можете користуватись ним.")
    else:
        bot.send_message(message.chat.id, "Ви не маєте доступу до цього бота.")

# Додайте код для перевірки файлу та відправки його користувачам тут

@bot.message_handler(commands=['getfile'])
def get_file(message):
    # Перевіряємо, чи є користувач адміністратором
    if message.chat.id in admins:
        # Локальний шлях до вашого файлу на сервері
        local_file_path = '/home/whitever/public_html/details/result.log'  # Змінено шлях до локального файлу
        
        try:
            # Відкриваємо файл і відправляємо його користувачу
            with open(local_file_path, 'rb') as file:  # Змінено шлях до локального файлу
                bot.send_document(message.chat.id, file, caption="Ось ваш файл!")
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Файл не знайдено.")
    else:
        bot.send_message(message.chat.id, "Ви не маєте доступу до цієї команди.")

if __name__ == '__main__':
    # Створюємо об'єкт обсервера
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(file_path_to_watch), recursive=False)
    observer.start()

    try:
        # Починаємо бота
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        # Зупиняємо обсервер та виходимо
        observer.stop()
    observer.join()