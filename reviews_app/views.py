from rest_framework import viewsets
from reviews_app.models import Review
from reviews_app.serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)
