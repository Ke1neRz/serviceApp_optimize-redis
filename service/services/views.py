from django.db.models import Prefetch, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet

from services.serializers import SubscriptionSerializer
from services.models import Subscription
from clients.models import Client

# Аннотация - Информация к определённой записи. (для каждой записи индивидуальное значение)
# Агрегация - Суммарная информация по всем записям.

class SubscriptionView(ReadOnlyModelViewSet):
    # prefetch_related('client') - Возьмём всех клиентов разом сразу для всех подписок. (Тоесть теперь не будем брать для каждой подписки всех клиетов, а вытащим сразу)
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name',
                                                              'user__email'))
    )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()) # наш queryset который определяется выше
        response = super().list(request, *args, **kwargs)
        response_data = {'result': response.data}
        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total') # get вернёт нам просто число
        response.data = response_data
        return response
    # Переопределение
    # Так ничего не изменится, но сдесь можно что-то подменть или изменить
    # def list(self, request, *args, **kwargs): 
    #     response = super().list(request, *args, **kwargs)
    #     return response
