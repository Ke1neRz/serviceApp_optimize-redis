import datetime
from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction
from django.db.models import F
from django.core.cache import cache
from django.conf import settings


# Во внутрь транзакций ложим только работу с базой, и после .save() выходим с неё
# В 1 функции может быть несколько транзакций

@shared_task(base=Singleton)
def set_price(subscription_id):
    from services.models import Subscription

    with transaction.atomic(): # Атомарное выполнение (Не может выполнится частично, то есть база накапливает все изменения внутри транхации и только если всё выполниломь сохраняет)
        subscription = Subscription.objects.select_for_update().filter(id=subscription_id).annotate(
            annotated_price=F('service__full_price') - 
                            F('service__full_price') * F('plan__discount_percent') / 100.00).first()

        subscription.price = subscription.annotated_price
        subscription.save()
    
    cache.delete(settings.PRICE_CACHE_NAME) # Инвалидация. (Чтобы при измениение данных cache пересоздавался)

        # new_price = (subscription.service.full_price -
        #              subscription.service.full_price * subscription.plan.discount_percent / 100)
        # subscription.price = new_price


@shared_task(base=Singleton)
def set_comment(subscription_id):
    from services.models import Subscription

    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().get(id=subscription_id)
        subscription.comment = str(datetime.datetime.now())
        subscription.save()

    cache.delete(settings.PRICE_CACHE_NAME)
