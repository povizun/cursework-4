from abc import ABC, abstractmethod
from config import ROOT_DIR
import json


class Saver(ABC):
    @abstractmethod
    def add_vacancies(self, vacancies):
        pass

    @abstractmethod
    def get_top_vacancies_by_name(self, key_words, top_n):
        pass

    @abstractmethod
    def clear_vacancies(self):
        pass


class JsonSaver(Saver):
    def __init__(self, file_name):
        self.file = f"{ROOT_DIR + file_name}.json"
        self.clear_vacancies()

    def add_vacancies(self, vacancies):
        """
        Сортирует вакансии и добавляет их в json файл
        :param vacancies:
        :return:
        """
        with open(self.file, "r") as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = []

        with open(self.file, "w", encoding="UTF-8") as file:
            for vacancy in vacancies:
                data.append(vacancy.get_vacancy_dict())

            sorted_data = sorted(data, key=lambda d: d['salary'][0], reverse=True)
            json.dump(sorted_data, file, indent=4, ensure_ascii=False)

    def get_top_vacancies_by_name(self, key_words, top_n):
        """
        Возвращает N вакансий, в которых есть хотя бы одно из заданных ключевых слов
        :param key_words:
        :param top_n:
        :return:
        """
        list_to_return = []
        with open(self.file, "r") as file:
            data = json.load(file)
            for vacancy in data:
                for word in key_words:
                    if word.lower() in vacancy["name"].lower() or word.lower() in vacancy["responsibility"].lower():
                        list_to_return.append(vacancy)
                        break
                if len(list_to_return) == 5:
                    break
        return list_to_return

    def clear_vacancies(self):
        """
        Очищает файл с вакансиями
        :return:
        """
        file = open(self.file, "w+", encoding="UTF-8")
        file.close()
