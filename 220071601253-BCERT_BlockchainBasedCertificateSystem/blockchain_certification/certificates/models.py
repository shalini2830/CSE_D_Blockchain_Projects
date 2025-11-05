from django.db import models


class Certificate(models.Model):
    student_name = models.CharField(max_length=255)
    course_name = models.CharField(max_length=255)
    issue_date = models.DateField()
    certificate_id = models.CharField(max_length=100, unique=True)
    blockchain_hash = models.CharField(max_length=256)
    status = models.CharField(max_length=50, default='Valid')
    issuer = models.ForeignKey('users.Institution', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.certificate_id} - {self.student_name} : {self.course_name}"


