import re
from collections import Counter
from transliterate import translit
from abc import ABC, abstractmethod


# Абстрактний клас для аналізу тексту
class TextAnalysis(ABC):
    @abstractmethod
    def analyze(self, text):
        pass


# Клас для аналізу відносної частоти вживання словоформ у тексті
class WordRelativeFrequency(TextAnalysis):
    def analyze(self, text):
        words = re.findall(r'\b\w+\b', text.lower())
        word_counts = Counter(words)
        total_words = len(words)
        relative_frequencies = {word: count / total_words * 100 for word, count in word_counts.items()}
        result = "\n".join(f"{word}: {frequency:.2f}%" for word, frequency in relative_frequencies.items())
        return f"Відносна частота вживання словоформ у тексті:\n{result}"


# Клас для транслітерації тексту з української мови
class Transliteration(TextAnalysis):
    def analyze(self, text):
        transliterated_text = translit(text, 'uk', reversed=True)
        return f"Транслітерований текст:\n{transliterated_text}"


# Клас для підрахунку кількості унікальних слів у тексті
class UniqueWordCounter(TextAnalysis):
    def analyze(self, text):
        words = re.findall(r'\b\w+\b', text.lower())
        total_unique_words = len(set(words))
        word_counts = Counter(words)
        unique_list = "\n".join(f"{word}: {count}" for word, count in word_counts.items())
        return f"Загальна кількість унікальних слів: {total_unique_words}\nСписок унікальних слів та їх кількості вживань в тексті:\n{unique_list}"


# Клас для керування аналізом тексту за допомогою різних методів
class TextAnalyzer:
    def __init__(self, method: TextAnalysis):
        self._method = method

    def set_method(self, method: TextAnalysis):
        self._method = method

    def process(self, text):
        return self._method.analyze(text)
