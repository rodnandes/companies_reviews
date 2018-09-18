from rest_framework import serializers
from reviews_app.models import Review
from django.contrib.auth.models import User


class ReviewSerializer(serializers.ModelSerializer):

    company = serializers.SlugRelatedField(slug_field='name', read_only=True)
    reviewer = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('title', 'company', 'reviewer', 'rating',
                  'summary', 'ip_address', 'submission_date')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
