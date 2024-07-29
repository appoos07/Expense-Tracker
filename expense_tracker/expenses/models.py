from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Expense(models.Model):
    SPLIT_CHOICES = [
        ('EQUAL', 'Equal'),
        ('EXACT', 'Exact'),
        ('PERCENTAGE', 'Percentage'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    split_type = models.CharField(max_length=10, choices=SPLIT_CHOICES)
    participants = models.ManyToManyField('User', related_name='expenses')
    date_created = models.DateTimeField(auto_now_add=True)

    def calculate_splits(self, amounts=None, percentages=None):
        if self.split_type == 'EQUAL':
            return self._split_equal()
        elif self.split_type == 'EXACT' and amounts:
            return self._split_exact(amounts)
        elif self.split_type == 'PERCENTAGE' and percentages:
            return self._split_percentage(percentages)
        else:
            raise ValueError("Invalid split type or missing required data")

    def _split_equal(self):
        num_participants = self.participants.count()
        if num_participants == 0:
            raise ValueError("No participants to split the expense")
        equal_amount = self.amount / num_participants
        return {user: equal_amount for user in self.participants.all()}

    def _split_exact(self, amounts):
        if len(amounts) != self.participants.count():
            raise ValueError("Number of amounts does not match number of participants")
        return {user: amounts[i] for i, user in enumerate(self.participants.all())}

    def _split_percentage(self, percentages):
        if sum(percentages) != 100:
            raise ValueError("Percentages do not sum to 100")
        return {user: self.amount * (percentages[i] / 100) for i, user in enumerate(self.participants.all())}
