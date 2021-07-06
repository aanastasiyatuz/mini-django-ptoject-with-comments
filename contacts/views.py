from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Contact
from .serializers import ContactSerializer

class ContactViewSet(viewsets.ModelViewSet):
    # достаем из бд все обьекты модели контакт
    queryset = Contact.objects.all()
    # указываем сериализатор
    serializer_class = ContactSerializer
    # я поставила запред на доступ, если юзера нет
    permission_classes = [IsAuthenticated, ]

    # поиск при методе get, detail=false позволяет нерассматривать дополнительные параметры, которые идут в запросе
    @action(methods=['GET'], detail=False)
    # даем название запроса /search?q=example
    def search(self, request):
        # вытаскивает только нужный параметр (q)
        query = request.query_params.get('q')
        # фильтруем queryset по имени
        queryset = self.get_queryset().filter(name__icontains=query)
        # сериализуем queryset
        serializer = self.get_serializer(queryset, many=True)
        # возвращаем сериализованные данные, со статусом 200
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    # /sort?filter=A-Z
    def sort(self, request):
        filter = request.query_params.get('filter')
        if filter == 'A-Z':
            queryset = self.get_queryset().order_by('name')
        elif filter == 'Z-A':
            queryset = self.get_queryset().order_by('-name')    
        else:
            queryset = self.get_queryset().order_by('phone')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

    # переопределение метода, чтобы доставать данные, связанные только с юзером, который отправляет запрос
    def get_queryset(self):
        # достаем юзера из запроса
        user = self.request.user
        # фильтруем queryset по юзеру
        queryset = super().get_queryset().filter(owner__exact=user)
        return queryset

    # если нужно передаем контекст в сериализатор
    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}
