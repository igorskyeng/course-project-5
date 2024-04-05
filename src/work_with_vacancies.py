import json
import os

from abc import ABC, abstractmethod
from data.data_hhru import HeadHunterAPI


class JSONSaver(ABC):

    @abstractmethod
    def save_vacancy(self):
        pass

    @abstractmethod
    def info_vacancy(self):
        pass

    @abstractmethod
    def delete_vacancy(self):
        pass


class VacancyFilter:
    """Класс для расчетов вакансий по введенным пользователем атрибутов."""

    def __init__(self, vacancies_name: str = 'Python', number_of_vacancies: int = 100,
                 salary_from: int = 50000, salary_to: int = 100000) -> None:
        """
        :param vacancies_name: Название вакансии.
        :param number_of_vacancies: Количесвто вакансий для поиска.
        :param salary_from: Максимальная  заработная плата.
        :param salary_to: Минимальная  заработная плата.
        """
        self.__vacancies_name = vacancies_name
        self.__number_of_vacancies = number_of_vacancies
        self.__salary_from = salary_from
        self.__salary_to = salary_to
        self.__vacancies_from_to_salary = []

    def __str__(self):
        JSONVacancies.info_vacancy(1)
        return 'Успешный вывод.'

    def __repr__(self):
        return (f'Название вакансии: {self.__vacancies_name}\nКоличесвто вакансий для поиска: '
                f'{self.__number_of_vacancies}\nМаксимальная заработная плата: {self.__salary_from}\n'
                f'Минимальная заработная плата: {self.__salary_to}\n')

    def sort_by_salary_vacancies(self, list_of_vacancies: list) -> list:
        """
        Сортировка вакансий по заработной плате.
        :param list_of_vacancies: Список вакансий.
        :return: Отсортированный список вакансий по заработной плате.
        """
        for item in range(0, len(list_of_vacancies)):
            if list_of_vacancies[item]['salary'] is not None:

                if (list_of_vacancies[item]['salary']['from'] is not None and
                        list_of_vacancies[item]['salary']['to'] is not None):

                    if (list_of_vacancies[item]['salary']['from'] >= self.__salary_from and
                            list_of_vacancies[item]['salary']['to'] <= self.__salary_to):
                        self.__vacancies_from_to_salary.append(list_of_vacancies[item])

        return self.__vacancies_from_to_salary


class JSONVacancies(JSONSaver):
    """Класс для сохранения, удаления и вывыда информации по вакансиям."""

    def __str__(self):
        JSONVacancies.info_vacancy(1)
        return 'Успешный вывод.'

    @staticmethod
    def save_vacancy(name_file: str = 'vacancy_dict.json', vacancies_dict_json: list = '') -> None:
        """
        Сохранение вакансий.
        :param name_file: Имя файла для записи вакансий.
        :param vacancies_dict_json: Словарь вакансий.
        """
        if type(vacancies_dict_json) is list:
            vacancies_dict_json = json.dumps(vacancies_dict_json, indent=2, ensure_ascii=False)

        file_json = open(name_file, 'w', encoding='UTF=8')
        file_json.write(vacancies_dict_json)
        file_json.close()

    def info_vacancy(self) -> None:
        """
        Вывод информации по вакансиям.
        """
        list_of_vacancies = HeadHunterAPI.load_vacancies_from_json()

        for item in range(0, len(list_of_vacancies)):
            print(f"\n{item+1}-ая выкансия:\nНазвание вакансии: {list_of_vacancies[item]['name']}\n"
                  f"Название компании: {list_of_vacancies[item]['employer']['name']}\n"
                  f"Заработная плата: {list_of_vacancies[item]['salary']['from']}-"
                  f"{list_of_vacancies[item]['salary']['to']} {list_of_vacancies[item]['salary']['currency']}\n"
                  f"Расписание: {list_of_vacancies[item]['schedule']['name']}\n"
                  f"Работа: {list_of_vacancies[item]['employment']['name']}\n"
                  f"Требования: {list_of_vacancies[item]['snippet']['requirement']}\n"
                  f"Ответственность: {list_of_vacancies[item]['snippet']['responsibility']}\n"
                  f"Ссылка на вакансию: {list_of_vacancies[item]['apply_alternate_url']}\n")

    @staticmethod
    def delete_vacancy(deleted_vacancy: int = 1) -> list:
        """
        Удаление вакансии по номеру.
        :param deleted_vacancy: Номер вакансии на удаление.
        :return: Список вакансий без удаленной.
        """
        list_of_vacancies = HeadHunterAPI.load_vacancies_from_json()
        deleted_vacancy -= 1

        if len(list_of_vacancies) > 1:
            del list_of_vacancies[deleted_vacancy]

        return list_of_vacancies
