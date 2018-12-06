from django.db.models import Avg
from rest_framework import serializers

from . import models


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'email': {'write_only': True}
        }
        fields = (
            'id',
            'course',
            'name',
            'email',
            'comment',
            'rating',
            'created_at'
        )
        model = models.Review

    def validate_rating(self, value):
        if value in range(1, 6):
            return value
        raise serializers.ValidationError(
            'Rating must be an integer between 1 and 5')


class CourseSerializer(serializers.ModelSerializer):
    href = serializers.HyperlinkedIdentityField(
        view_name='apiv2:course-detail')
    # reviews = ReviewSerializer(many=True, read_only=True)
    # reviews = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     read_only=True
    # )
    reviews = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='apiv2:review-detail'  # ViewSetによる自動
    )
    average_rating = serializers.SerializerMethodField()  # get_average_rating()

    class Meta:
        fields = (
            'id',
            'href',
            'title',
            'url',  # hyperlinked identity field ではない
            'reviews',
            'average_rating',
        )
        model = models.Course

    def get_average_rating(self, obj):
        average = obj.reviews.aggregate(Avg('rating')).get('rating__avg')
        if average is None:
            return 0

        return round(average * 2) / 2  # 0.5刻み
