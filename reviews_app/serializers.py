from rest_framework import serializers
from reviews_app.models import Review, Company
from django.contrib.auth.models import User


class ReviewSerializer(serializers.ModelSerializer):

    reviewer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all())
    reviewer_username = serializers.CharField(
        source='reviewer.username', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
