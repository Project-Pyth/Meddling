from django.db import models
from django.contrib.auth.models import auth
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()


def upload_location(instance, filename):
    file_path = 'file/{category}/{filename}'.format(category=str(instance.cat), filename=filename)
    return file_path


# Create your models here.
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)


class Category(models.Model):
    categ_name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.categ_name


class File(models.Model):
    cat = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_location)

    def __str__(self):
        return self.cat.categ_name


@receiver(post_delete, sender=File)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# future scope
class Question(models.Model):
     CAT_CHOICES = (
    ('English', 'English'),
    ('Math', 'Math'),
    ('Reasoning', 'Reasoning'),
    ('Computer', 'Computer')
     )
     category = models.CharField(max_length=25, choices=CAT_CHOICES)
     question = models.TextField(max_length=500)
     option1 = models.CharField(max_length=100)
     option2 = models.CharField(max_length=100)
     option3 = models.CharField(max_length=100)
     option4 = models.CharField(max_length=100)
     choose = (('A', 'option1'), ('B', 'option2'), ('C', 'option3'),('D', 'option4'))
     Answers = models.CharField(max_length=1, choices=choose)

     class Meta:
        ordering = ('-category',)

     def __str__(self):
        return str(self.question)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pic',null=True,default='default.jpg')
    dob = models.DateTimeField(null=True)
    bio = models.CharField(max_length=225)
    city = models.CharField(max_length=225)



class Feedback(models.Model):
    name = models.CharField(max_length=225)
    email = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'feedbacks'

    def __str__(self):
        return 'Feedback from' + ' ' + self.name
