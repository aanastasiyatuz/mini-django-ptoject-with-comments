from rest_framework import generics
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer

# view только для регистрации потому что login происходит при получении токена по адрессу /api/token/
class RegisterApi(generics.GenericAPIView):
    # указываем сериализацию
    serializer_class = RegisterSerializer
    # переопределяем метод post
    def post(self, request, *args,  **kwargs):
        # передаем в сериализатор введенную информацию, которая хранится в request
        serializer = self.get_serializer(data=request.data)
        # если json невалидный выйдет соответствующая ошибка, которую мы указали в сериализаторе
        serializer.is_valid(raise_exception=True)
        # сохраняем json данные
        user = serializer.save()
        # возвращаем на фронт данные
        return Response({
            # модель, которая проходит UserSerializer
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # сообщение об успешном создании юзера
            "message": "User Created Successfully.  Now perform Login to get your token",
        })
