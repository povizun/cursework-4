class Vacancy:
    def __init__(self, source, name, link, salary, requirement, responsibility):
        self.source = source
        self.name = name
        self.url = link
        if salary is None:
            self.salary = 0
            self.currency = "RUB"
        elif salary["to"] is None or salary["to"] == 0:
            self.salary = salary["from"]
            self.currency = salary["currency"]
        elif salary["from"] is None or salary["from"] == 0:
            self.salary = salary["to"]
            self.currency = salary["currency"]
        else:
            self.salary_from = salary["from"]
            self.salary_to = salary["to"]
            self.salary = round((salary["to"] + salary["from"]) / 2)
            self.currency = salary["currency"]
        self.requirement = requirement
        self.responsibility = responsibility

    def get_vacancy_dict(self):
        """
        Возвращает данные вакансии в виде словаря
        :return:
        """
        return {"url": self.url, "name": self.name, "salary": [self.salary, self.currency],
                "requirement": self.requirement, "responsibility": self.responsibility}

    def __str__(self):
        return self.name

    def __repr__(self):
        return {'name': self.name, 'url': self.url}

    def __lt__(self, other):
        return self.salary < other.salary

    def __le__(self, other):
        return self.salary <= other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    def __ge__(self, other):
        return self.salary >= other.salary

    def __eq__(self, other):
        return self.salary == other.salary
