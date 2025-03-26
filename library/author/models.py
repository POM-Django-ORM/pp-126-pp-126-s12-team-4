from dataclasses import fields
from django.core.exceptions import ValidationError

from django.db import models


class Author(models.Model):
    """
        This class represents an Author. \n
        Attributes:
        -----------
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes last name of the author
        type surname: str max_length=20
        param patronymic: Describes middle name of the author
        type patronymic: str max_length=20
    """
    name = models.CharField(max_length=20, blank=True, default='')
    surname = models.CharField(max_length=20, blank=True, default='')
    patronymic = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        """
        Magic method is redefined to show all information about Author.
        :return: author id, author name, author surname, author patronymic
        """
        return f"'id': {self.id}, 'name': '{self.name}', 'surname': '{self.surname}', 'patronymic': '{self.patronymic}'"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Author object.
        :return: class, id
        """
        return f"Author(id={self.id})"

    @staticmethod
    def get_by_id(author_id):
        """
        :param author_id: SERIAL: the id of a Author to be found in the DB
        :return: author object or None if a user with such ID does not exist
        """
        return Author.objects.filter(id=author_id).first()

    @staticmethod
    def delete_by_id(author_id):
        """
        :param author_id: an id of a author to be deleted
        :type author_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        del_count, _ = Author.objects.filter(id=author_id).delete()
        return del_count > 0

    @staticmethod
    def create(name, surname, patronymic):
        """
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: a new author object which is also written into the DB
        """
        author = Author(name=name, surname=surname, patronymic=patronymic)
        try:
            # Полная валидация полей модели
            author.full_clean()
            author.save()
            return author
        except ValidationError:
            return None

    def to_dict(self):
        """
        :return: author id, author name, author surname, author patronymic
        :Example:
        | {
        |   'id': 8,
        |   'name': 'fn',
        |   'surname': 'mn',
        |   'patronymic': 'ln',
        | }
        """
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic
        }

    def update(self,
               name=None,
               surname=None,
               patronymic=None):
        """
        Updates author in the database with the specified parameters.
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: None
        """
        # Save current fields in order to be able to back up
        original = {
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic,
        }

        # Обновляем поля, если переданы новые значения
        attrs = {
            'name': name,
            'surname': surname,
            'patronymic': patronymic,
        }

        for attr, value in attrs.items():
            if value is not None:
                setattr(self, attr, value)

        try:
            self.full_clean()
            self.save()
        except ValidationError:
            for attr, value in original.items():
                setattr(self, attr, value)

        self.refresh_from_db()

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all authors
        """
        return Author.objects.all()
