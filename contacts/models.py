from django.db import models
from account.models import MyUser

class Contact(models.Model):
    # поля в бд
    # ForeignKey связь OneToMany (у одного юзера несколько контактов), при удалении юзера удаляются все его контакты
    owner = models.ForeignKey(MyUser, related_name='contacts', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.name + f' ({self.phone})'