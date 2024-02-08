from src.api import SuperJobAPI, HeadHunterAPI
from src.saver import JsonSaver


def user_interaction():
    search_query = input("Введите поисковый запрос: ")
    sas = HeadHunterAPI(search_query)
    asa = SuperJobAPI(search_query)
    vacancies_hh = sas.get_vacancies()
    vacancies_sj = asa.get_vacancies()
    json_saver = JsonSaver("/try")
    json_saver.add_vacancies(vacancies_hh)
    json_saver.add_vacancies(vacancies_sj)
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    for vacancy in json_saver.get_top_vacancies_by_name(filter_words, top_n):
        print_vacancy(vacancy)


def print_vacancy(vacancy):
    print(f"""
Name: {vacancy['name']}
Salary: {vacancy['salary']}
Url: {vacancy['url']}
Requirement: {vacancy['requirement']}
Responsibility: {vacancy['responsibility']}
""")
