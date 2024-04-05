import json
import requests

from abc import ABC, abstractmethod


class Vacancy(ABC):

    @abstractmethod
    def load_vacancies_from_hhru(self):
        pass

    @abstractmethod
    def load_vacancies_from_json(self):
        pass


class HeadHunterAPI(Vacancy):
    """
    Класс для Загрузки вакансий из сайта hh.ru и их чтения с фалйла.
    """

    def __str__(self):
        message = 'Класс для Загрузки вакансий из сайта hh.ru и их чтения с фалйла.'
        return 'Класс для Загрузки вакансий из сайта hh.ru и их чтения с фалйла.'
    @staticmethod
    def load_vacancies_from_hhru(vacancies_name: str = 'Python', number_of_vacancies: int = 100) -> str:
        """
        Создает словарь вакансий загруженных из сайта hh.ru.
        :param vacancies_name: Название вакансии.
        :param number_of_vacancies: Количество вакансий для поиска.
        :return: Словарь вакансий.
        """
        if isinstance(vacancies_name, str):
            key_response = {'text': f'NAME:{vacancies_name}', 'area': 1, 'per_page': number_of_vacancies, }
            vacancies_dict = requests.get(f'https://api.hh.ru/vacancies', key_response)
            vacancies_dict_json = json.loads(vacancies_dict.text)['items']

        else:
            vacancies_dict_json = "Vacancy not found"

        vacancies_dict_json = json.dumps(vacancies_dict_json, indent=2, ensure_ascii=False)

        return vacancies_dict_json

    @staticmethod
    def load_vacancies_from_json(name_file: str = 'vacancy_dict.json') -> list:
        """
        Создает список вакансий прочитанных из указанного файла.
        :param name_file: Имя файла для чтения.
        :return: Список вакансий.
        """
        list_of_vacancies = ''

        with open('vacancy_dict.json', 'r', encoding='UTF=8') as file:
            for line in file:
                list_of_vacancies += line

        list_of_vacancies = json.loads(list_of_vacancies)
        file.close()

        return list_of_vacancies
