from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class Visualization(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_file = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE
    )

    chart_type = models.CharField(max_length=50)
    x_column = models.CharField(max_length=100)
    y_column = models.CharField(max_length=100)

    image = models.ImageField(upload_to='charts/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chart_type