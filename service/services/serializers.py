from rest_framework import serializers

from services.models import Plan, Subscription
from services.models import Plan

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('__all__')

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')
    price = serializers.SerializerMethodField() # сериализатор ищет функцию price с приставкой get_

    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'client_name', 'price', 'email', 'plan')
    
    def get_price(self, instance):
        return instance.price
    # def get_price(self, instance):
    #     return (instance.service.full_price - 
    #             instance.service.full_price * (instance.plan.discount_percent / 100))
