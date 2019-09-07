from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


class Walker(ExportModelOperationsMixin('walker'), models.Model):
    name = models.CharField(max_length=127)
    email = models.CharField(max_length=127)

    def __str__(self):
        return f'{self.name} // {self.email} ({self.id})'


class Dog(ExportModelOperationsMixin('dog'), models.Model):
    SIZE_XS = 'xs'
    SIZE_SM = 'sm'
    SIZE_MD = 'md'
    SIZE_LG = 'lg'
    SIZE_XL = 'xl'
    DOG_SIZES = (
        (SIZE_XS, 'xsmall'),
        (SIZE_SM, 'small'),
        (SIZE_MD, 'medium'),
        (SIZE_LG, 'large'),
        (SIZE_XL, 'xlarge'),
    )

    size = models.CharField(max_length=31, choices=DOG_SIZES, default=SIZE_MD)
    name = models.CharField(max_length=127)
    age = models.IntegerField()

    def __str__(self):
        return f'{self.name} // {self.age}y ({self.size})'


class Walk(ExportModelOperationsMixin('walk'), models.Model):
    dog = models.ForeignKey(Dog, related_name='walks', on_delete=models.CASCADE)
    walker = models.ForeignKey(Walker, related_name='walks', on_delete=models.CASCADE)

    distance = models.IntegerField(default=0, help_text='walk distance (in meters)')

    start_time = models.DateTimeField(null=True, blank=True, default=None)
    end_time = models.DateTimeField(null=True, blank=True, default=None)

    @property
    def is_complete(self):
        return self.end_time is not None

    def __str__(self):
        return f'{self.walker.name} // {self.dog.name} @ {self.start_time} ({self.id})'
