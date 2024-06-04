import tkinter as tk
from tkinter import filedialog
from src.text_processing.functions import *
from src.logger import *


class Interface:
    title: str = "TextExplorer"

    __app: tk.Tk  # Головне вікно додатку
    __text_editor: tk.Text  # Текстовий редактор
    __output_panel: tk.Text  # Панель для виводу результатів

    def __init__(self) -> None:
        self.__app = tk.Tk()  # Ініціалізація головного вікна
        self.__logger = Logger().get_logger()  # Ініціалізація логера
        self.__initialize_components()  # Ініціалізація компонентів інтерфейсу

    def __initialize_components(self):
        # Створення текстового редактора
        self.__text_editor = tk.Text(self.__app, height=15, width=100, bg='lightyellow', fg='black')
        self.__text_editor.pack(pady=20)

        # Створення панелі для виводу результатів
        self.__output_panel = tk.Text(self.__app, height=15, width=100, state=tk.DISABLED, bg='lightgrey', fg='black')
        self.__output_panel.pack(pady=20)

        # Створення меню
        menu_bar = tk.Menu(self.__app)
        self.__app.config(menu=menu_bar)

        # Додавання меню файлів
        file_menu = FileMenu(self.__app, self.__text_editor, self.__logger)
        menu_bar.add_cascade(label="Файл", menu=file_menu.menu)

        # Додавання меню операцій для аналізу
        run_menu = RunMenu(self.__app, self.__text_editor, self.__output_panel, self.__logger)
        menu_bar.add_cascade(label="Набір операцій для аналізу", menu=run_menu.menu)

    def run(self):
        self.__logger.info("Запуск додатку.")
        self.__app.title(self.title)
        self.__app.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.__app.mainloop()

    def __on_closing(self):
        self.__logger.info("Завершення роботи додатку.\n")
        self.__app.destroy()


class FileMenu:
    def __init__(self, parent, text_editor, logger):
        self.menu = tk.Menu(parent, tearoff=0)
        self.text_editor = text_editor
        self.logger = logger
        self.__add_commands()

    def __add_commands(self):
        # Додавання команди відкриття файлу
        self.menu.add_command(label="Відкрити", command=self.__open_file)
        # Додавання команди збереження файлу
        self.menu.add_command(label="Зберегти", command=self.__save_file)

    def __open_file(self):
        # Відкриття файлу через діалогове вікно
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, file.read())
            self.logger.info(f"Відкрито файл: {file_path}")

    def __save_file(self):
        # Збереження файлу через діалогове вікно
        file_path = filedialog.asksaveasfilename(defaultextension="txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_editor.get(1.0, tk.END))
            self.logger.info(f"Збережено файл: {file_path}")


class RunMenu:
    def __init__(self, parent, text_editor, output_panel, logger):
        self.menu = tk.Menu(parent, tearoff=0)
        self.text_editor = text_editor
        self.output_panel = output_panel
        self.logger = logger
        self.__add_commands()

    def __add_commands(self):
        # Додавання команд для аналізу тексту
        self.menu.add_command(label="Підрахунок відносної частоти вживання словоформ",
                              command=self.__relative_frequency_function)
        self.menu.add_command(label="Транслітерація з української мови на англійську",
                              command=self.__transliteration_function)
        self.menu.add_command(label="Підрахунок кількості унікальних слів", command=self.__count_words_function)

    def __process_text(self, method):
        # Отримання тексту з текстового редактора
        content = self.text_editor.get(1.0, tk.END)
        self.logger.info(f"Виконано операцію: {method.__class__.__name__}")

        # Створення об'єкта TextAnalyzer з переданим методом аналізу текст
        processor = TextAnalyzer(method)
        result = processor.process(content)

        # Відображення результату обробки тексту в панелі виводу
        self.output_panel.config(state=tk.NORMAL)
        self.output_panel.delete(1.0, tk.END)
        self.output_panel.insert(tk.END, result)
        self.output_panel.config(state=tk.DISABLED)
        self.logger.info(f"Результат обробки тексту: {result}")

    def __count_words_function(self):
        self.__process_text(UniqueWordCounter())

    def __transliteration_function(self):
        self.__process_text(Transliteration())

    def __relative_frequency_function(self):
        self.__process_text(WordRelativeFrequency())
