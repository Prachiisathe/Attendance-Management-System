from django.db import models
from django.core.validators import RegexValidator

name_validator = RegexValidator(
    regex=r'^[A-Za-z ]+$',
    message="Only letters allowed in name"
)


roll_validator = RegexValidator(
    regex=r'^[0-9]+$',
    message="Roll number must contain only digits"
)


phone_validator = RegexValidator(
    regex=r'^[0-9]{10}$',
    message="Phone must be 10 digits"
)

# Create your models here.
class Student(models.Model):
    student_name = models.CharField(max_length=100, validators=[name_validator])
    roll_no = models.CharField(max_length=20, unique=True,validators=[roll_validator])
    student_class = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10, validators=[phone_validator])


    def __str__(self):
        return self.student_name


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    date = models.DateField(auto_now_add=True)


    def __str__(self):


        return f"{self.student.student_name} - {self.date}"
