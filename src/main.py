from src.work_with_vacancies import VacancyFilter
from src.work_with_vacancies import JSONVacancies
from data.data_hhru import HeadHunterAPI
from src.db_manager import DBManager


def main1():
    """Main1 для работы с задачами Курсовой работы №5"""
    choice = input('Выберите нужное действие:\n'
                   '1 - получает список всех компаний и количество вакансий у каждой компании;\n'
                   '2 - получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и '
                   'ссылки на вакансию;\n'
                   '3 - получает среднюю зарплату по вакансиям;\n'
                   '4 - получает список всех вакансий, у которых зарплата выше средней по всем вакансиям;\n'
                   '5 - получает список всех вакансий, в названии которых содержатся переданные в метод слова, '
                   'например python.\n')

    if choice == '1':
        DBManager.get_companies_and_vacancies_count()

    elif choice == '2':
        DBManager.get_all_vacancies()

    elif choice == '3':
        DBManager.get_avg_salary()

    elif choice == '4':
        DBManager.get_vacancies_with_higher_salary()

    elif choice == '5':
        keyword = input('Введите название вакансии:\n')
        DBManager.get_vacancies_with_keyword(keyword)


def main2():
    """Main2 для работы с вакансиями (скачивания и сохранение)."""
    # Ввод названия вакансии.
    vacancies_name = str(input('Введите название вакансии:\n'))

    # Ввод количесвта вакансий на поиск.
    number_of_vacancies = int(input('\nВведите количесво вакансий для поиска:\n'))

    # Ввод максимальной заработной платы.
    salary_from = int(input('\nВведите минимальную заработную плату\n'))

    # Ввод минимальной заработной платы.
    salary_to = int(input('\nВведите максимальную заработную плату\n'))

    # Инициализация класса для работы с вакансиями.
    vacancy_filter = VacancyFilter(vacancies_name=vacancies_name, number_of_vacancies=number_of_vacancies,
                                   salary_from=salary_from, salary_to=salary_to)

    # Загрузка вакансий с сайта и сохранение их в файл.
    JSONVacancies.save_vacancy(vacancies_dict_json=HeadHunterAPI().load_vacancies_from_hhru(
        vacancies_name=vacancies_name, number_of_vacancies=number_of_vacancies))

    # Получение списка вакансий.
    hh_vacancies = HeadHunterAPI().load_vacancies_from_json()

    # Сортировка вакансий по заработной плате.
    hh_vacancies = vacancy_filter.sort_by_salary_vacancies(hh_vacancies)

    # Сохранение отсортированного списка вакансий.
    JSONVacancies.save_vacancy(vacancies_dict_json=hh_vacancies)

    # Вывод информации по отсортированным вакансиям.
    JSONVacancies.info_vacancy(1)

    # Ввод пользователем номер вакансии на удаление.
    deleted_vacancy = int(input('\nВведите вакансию, которую желаете удалить\n'))

    # Удаление выбранной пользователем вакансии.
    hh_vacancies = JSONVacancies.delete_vacancy(deleted_vacancy=deleted_vacancy)

    # Сохранение отсортированного списка вакансий.
    JSONVacancies.save_vacancy(vacancies_dict_json=hh_vacancies)

    # Вывод информации по отсортированным вакансиям
    JSONVacancies.info_vacancy(1)


main1()
