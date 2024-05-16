from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    calories = serializers.CharField()
    fats = serializers.CharField()
    carbs = serializers.CharField()
    proteins = serializers.CharField()
    additional_fats = serializers.CharField()
    sugar = serializers.CharField()
    salt = serializers.CharField()
    portion = serializers.CharField()
