from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    # указание, что это поле необязательно для заполнения, потому что в методе create мы укажем значение, которое мы получаем из request
    owner = serializers.CharField(required=False)

    class Meta:
        model = Contact
        fields = '__all__'

    def create(self, validated_data):
        # достаем юзера из request (нам доступен request, потому что во view я указала get_serializer_context)
        user = self.context.get('request').user
        # создаем новый объект контакта с указанием юзера, который отправляет request
        contact = Contact.objects.create(owner=user, **validated_data)
        return contact
