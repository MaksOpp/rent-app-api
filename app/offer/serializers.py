from rest_framework import serializers

from core.models import Tag, Offer


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_Fields = ('id',)


class OfferSerializer(serializers.ModelSerializer):
    """Serialize a offer"""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Offer
        fields = (
            'id', 'title', 'description', 'tags', 'min_players', 'max_players',
            'price_per_day', 'is_highlighted'
        )
        read_only_fields = ('id',)
