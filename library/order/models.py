from django.db import models
from django.utils import timezone
from authentication.models import CustomUser
from book.models import Book


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)
    plated_end_at = models.DateTimeField()

    def __str__(self):
        return f"'id': {self.id}, 'user': CustomUser(id={self.user.id}), 'book': Book(id={self.book.id}), 'created_at': '{self.created_at}', 'end_at': '{self.end_at}', 'plated_end_at': '{self.plated_end_at}'"

    def __repr__(self):
        return f"Order(id={self.id})"

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.id,
            'book': self.book.id,
            'created_at': self.created_at,
            'end_at': self.end_at,
            'plated_end_at': self.plated_end_at,
        }

    @staticmethod
    def create(user, book, plated_end_at):
        if not user.id or not book.id:
            return None
        if Order.objects.filter(book=book, end_at__isnull=True).exists():
            return None
        order = Order(user=user, book=book, plated_end_at=plated_end_at)
        order.save()
        return order

    @staticmethod
    def get_by_id(order_id):
        return Order.objects.filter(id=order_id).first()

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at:
            self.plated_end_at = plated_end_at
        if end_at:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        return list(Order.objects.filter(end_at__isnull=True))

    @staticmethod
    def delete_by_id(order_id):
        order = Order.objects.filter(id=order_id).first()
        if order:
            order.delete()
            return True
        return False
