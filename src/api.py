from abc import ABC, abstractmethod
import requests
from src.vacancy import Vacancy


class API(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(API):
    def __init__(self, text_to_find):
        headers = {"User-Agent": "AM"}
        response = requests.get("https://api.hh.ru/vacancies", headers=headers,
                                params=f"per_page=20&text={text_to_find}")
        self.unprocessed_vacancies = response.json()
        self.vacancies = None

    def get_vacancies(self):
        """
        Получает вакансии через API HH, создает объекты вакансий и возвращает их лист
        :return:
        """
        list_of_vacancies = []
        for item in self.unprocessed_vacancies["items"]:
            name = item['name']
            link = f"https://hh.ru/vacancy/{item['id']}"
            salary = item['salary']
            requirement = item['snippet']['requirement']
            responsibility = item['snippet']['responsibility']
            vacancy = Vacancy("HeadHunter", name, link, salary, requirement, responsibility)
            list_of_vacancies.append(vacancy)
        self.vacancies = list_of_vacancies
        return list_of_vacancies


class SuperJobAPI(API):
    def __init__(self, text_to_find):
        headers = {"X-Api-App-Id": "v3.r.138141026.cb9ed961b12b2b06f37d2b8b307549d5e7545874."
                                   "99e783b6e45c8012ce1496bb16a59af316c53a80"}
        response = requests.get("https://api.superjob.ru/2.0/vacancies/",
                                headers=headers, params=f"count=20&keyword={text_to_find}")
        self.unprocessed_vacancies = response.json()
        self.vacancies = []

    def get_vacancies(self):
        """
        Получает вакансии через API SJ, создает объекты вакансий и возвращает их лист
        :return:
        """
        list_of_vacancies = []
        for unprocessed_vacancy in self.unprocessed_vacancies["objects"]:
            name = unprocessed_vacancy['profession']
            link = unprocessed_vacancy['link']
            salary = {"from": unprocessed_vacancy["payment_from"],
                      "to": unprocessed_vacancy["payment_to"],
                      "currency": unprocessed_vacancy["currency"]}
            requirement = ""
            if unprocessed_vacancy['place_of_work']['id'] != 0:
                requirement += f"Место работы: {unprocessed_vacancy['place_of_work']['title']}. "
            if unprocessed_vacancy['education']['id'] != 0:
                requirement += f"Нужно иметь {unprocessed_vacancy['education']['title']} образование. "
            if unprocessed_vacancy['experience']['id'] != 0:
                requirement += f"Опыт работы: {unprocessed_vacancy['experience']['title']}. "
            if requirement == "":
                requirement = "Нет указанных требований"
            responsibility = unprocessed_vacancy['candidat']
            vacancy = Vacancy("SuperJob", name, link, salary, requirement, responsibility)
            list_of_vacancies.append(vacancy)
        self.vacancies = list_of_vacancies
        return list_of_vacancies
