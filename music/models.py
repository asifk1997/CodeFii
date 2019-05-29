from django.contrib.auth.models import Permission, User
from django.db import models
import datetime

class Problemset(models.Model):
    user = models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    curator = models.CharField(max_length=250)
    problemset_title = models.CharField(max_length=500)
    problemset_type = models.CharField(max_length=100)
    problemset_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.problemset_title + ' - ' + self.curator


class Problem(models.Model):
    problemset= models.ForeignKey(Problemset, on_delete=models.CASCADE)
    problem_title = models.CharField(max_length=250)
    problem_file = models.FileField(default='')
    problem_expected_output = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.problem_title


class Submission(models.Model):
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    user = models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    code = models.FileField(default='')
    my_output= models.FileField(default='')
    verdict = models.BooleanField()
    time= models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.problem.problem_title + " - " +self.time