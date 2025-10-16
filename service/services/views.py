from django.shortcuts import render
from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet

from services.serializers import SubscriptionSerializer
from services.models import Subscription
from clients.models import Client

class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name',
                                                              'user__email'))
    ) # prefetch_related('client') - Возьмём всех клиентов разом сразу для всех подписок. (Тоесть теперь не будем брать для каждой подписки всех клиетов, а вытащим сразу)
    serializer_class = SubscriptionSerializer
