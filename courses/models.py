from django.db import models
from django.core import validators

# Create your models here.

class Department(models.Model):

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    name = models.CharField(verbose_name='name', max_length=255, unique=True)

    def __str__(self) -> str:
        return f'Department Name: {self.name}'


class Course(models.Model):

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['code']

    code_validator = validators.RegexValidator(
        regex=r'^[A-Z]{2,4}\s[A-Z]{1}\d{3}$',
        message='Course code must be in the format "CS F111" or "MATH F101"'
    )

    code = models.CharField(verbose_name='code', max_length=25, unique=True, validators=[code_validator])
    title = models.CharField(verbose_name='title', max_length=255)
    department = models.ForeignKey(to='courses.Department', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Course Code: {self.code}'


class Resource(models.Model):

    class Meta:
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'
        unique_together = ['course', 'title']

    class TypeChoices(models.TextChoices):
        PDF = 'PDF', 'PDF'
        VIDEO = 'VIDEO', 'Video'
        LINK = 'LINK', 'Link'
    
    course = models.ForeignKey(verbose_name='course', to='courses.Course', on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(verbose_name='title', max_length=255)
    type = models.CharField(verbose_name='type', choices=TypeChoices.choices, max_length=5)
    link = models.URLField(verbose_name='link', max_length=200, unique=True)

    def __str__(self) -> str:
        return f'Resource Title: {self.title}\nType: {self.type}\nLink: {self.link}'
