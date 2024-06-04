import logging


class Logger:
    _instance = None  # Змінна класу для зберігання єдиного екземпляру

    def __new__(cls):
        # Перевірка наявності екземпляра і створення нового, якщо його немає
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        # Створення об'єкта логера і встановлення рівня логування
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        handler = logging.FileHandler("text_analysis_log.txt", encoding="utf-8")
        # Встановлення формату для логів
        formatter = logging.Formatter("(%(asctime)s) %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    # Метод, який повертає екземпляр логера
    def get_logger(self):
        return self.logger
