"""
Student information for this assignment:

Replace Aarnav Chitari with your name.
On my/our honor, Vineet Burugu and Aarnav Chitari, this
programming assignment is my own work and I have not provided this code to
any other student.

I have read and understand the course syllabus's guidelines regarding Academic
Integrity. I understand that if I violate the Academic Integrity policy (e.g.
copy code from someone else, have the code generated by an LLM, or give my
code to someone else), the case shall be submitted to the Office of the Dean of
Students. Academic penalties up to and including an F in the course are likely.

UT EID 1: vsb433
UT EID 2: ac84787
"""

from abc import ABC, abstractmethod
import random

DAILY_EXPENSE = 60
HAPPINESS_THRESHOLD = 50
MANAGER_BONUS = 1000
TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD = 50
PERM_EMPLOYEE_PERFORMANCE_THRESHOLD = 25
RELATIONSHIP_THRESHOLD = 10
RELATIONSHIP_MIN = -20
INITIAL_PERFORMANCE = 75
INITIAL_HAPPINESS = 50
PERCENTAGE_MAX = 100
PERCENTAGE_MIN = 0
SALARY_ERROR_MESSAGE = "Salary must be non-negative."


class Employee(ABC):
    """
    Abstract base class representing a generic employee in the system.
    """

    def __init__(self, name, manager, salary, savings):
        self.relationships = {}
        self.savings = savings
        self.is_employed = True
        self.__name = name
        self.__manager = manager
        self.performance = INITIAL_PERFORMANCE
        self.happiness = INITIAL_HAPPINESS
        self.salary = salary

    @property
    def name(self):
        """
        Name
        """
        return self.__name

    @property
    def manager(self):
        """
        Manage
        """
        return self.__manager

    @property
    def performance(self):
        """
        Perf
        """
        return self._performance

    @performance.setter
    def performance(self, value):
        """
        Perf
        """
        self._performance = max(PERCENTAGE_MIN, min(PERCENTAGE_MAX, value))

    @property
    def happiness(self):
        """
        Happy
        """
        return self._happiness

    @happiness.setter
    def happiness(self, value):
        """
        Happy
        """
        self._happiness = max(PERCENTAGE_MIN, min(PERCENTAGE_MAX, value))

    @property
    def salary(self):
        """
        Salary
        """
        return self._salary

    @salary.setter
    def salary(self, value):
        """
        Salary
        """
        if value < 0:
            raise ValueError(SALARY_ERROR_MESSAGE)
        self._salary = value

    @abstractmethod
    def work(self):
        """
        Work
        """

    def interact(self, other):
        """
        interact
        """
        if other.name not in self.relationships:
            self.relationships[other.name] = 0

        if self.relationships[other.name] > RELATIONSHIP_THRESHOLD:
            self.happiness += 1
        elif self.happiness >= HAPPINESS_THRESHOLD and other.happiness >= HAPPINESS_THRESHOLD:
            self.relationships[other.name] += 1
        else:
            self.relationships[other.name] -= 1
            self.happiness -= 1

        self.relationships[other.name] = max(RELATIONSHIP_MIN, self.relationships[other.name])

    def daily_expense(self):
        """
        daily
        """
        self.happiness -= 1
        self.savings -= DAILY_EXPENSE

    def __str__(self):
        return (
            f"{self.name}\n\tSalary: ${self.salary}\n\tSavings: ${self.savings}\n"
            f"\tHappiness: {self.happiness}%\n\tPerformance: {self.performance}%"
        )


class Manager(Employee):
    """
    A subclass of Employee representing a manager.
    """
    def work(self):
        newperformance = random.randint(-5, 5)
        self.performance += newperformance
        if newperformance <= 0:
            self.happiness -= 1
            for employee in self.relationships.items():
                var = self.relationships[employee] - 1
                self.relationships[employee] = max(RELATIONSHIP_MIN, var)
        else:
            self.happiness += 1


class TemporaryEmployee(Employee):
    """
    A subclass of Employee representing a temporary employee.
    """
    def work(self):
        newperformance = random.randint(-15, 15)
        self.performance += newperformance
        if newperformance <= 0:
            self.happiness -= 2
        else:
            self.happiness += 1

    def interact(self, other):
        super().interact(other)

        if isinstance(other, Manager) and other is self.manager:
            if (other.happiness > HAPPINESS_THRESHOLD and self.performance
                >= TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD):
                self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                self.salary //= 2
                self.happiness -= 5
                if self.salary <= 0:
                    self.is_employed = False


class PermanentEmployee(Employee):
    """
    A subclass of Employee representing a permanent employee.
    """
    def work(self):
        newperformance = random.randint(-10, 10)
        self.performance += newperformance
        if newperformance >= 0:
            self.happiness += 1

    def interact(self, other):
        super().interact(other)

        if isinstance(other, Manager) and other is self.manager:
            if other.happiness <= HAPPINESS_THRESHOLD:
                self.happiness -= 1

            if (other.happiness > HAPPINESS_THRESHOLD and self.performance
                > PERM_EMPLOYEE_PERFORMANCE_THRESHOLD):
                self.savings += MANAGER_BONUS
