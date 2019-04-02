from rest_framework import serializers
from .models import Meeting
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    meetings = serializers.PrimaryKeyRelatedField(many=True, queryset=Meeting.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'meetings',)


class MeetingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Meeting
        fields = ('id', 'created', 'sinceWhen', 'tilWhen', 'user',)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Meeting.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.sinceWhen = validated_data.get('sinceWhen', instance.sinceWhen)
        instance.tilWhen = validated_data.get('tilWhen', instance.tilWhen)
        instance.save()
        return instance

    def validate(self, attrs):
        if attrs['sinceWhen'] >= attrs['tilWhen']:
            raise serializers.ValidationError("sinceWhen must precede tilWhen")

        before = Meeting.objects.filter(sinceWhen__lt=attrs['tilWhen'])
        after = Meeting.objects.filter(tilWhen__gt=attrs['sinceWhen'])

        for i in before:
            if i.tilWhen > attrs['sinceWhen']:
                raise serializers.ValidationError("invalid reservation time 1")

        for j in after:
            if j.sinceWhen < attrs['tilWhen']:
                raise serializers.ValidationError("invalid reservation time 2")

        return attrs

class MeetingSerializer_detail(MeetingSerializer):

    def validate(self, attrs):
        if attrs['sinceWhen'] >= attrs['tilWhen']:
            raise serializers.ValidationError("sinceWhen must precede tilWhen")

        before = Meeting.objects.filter(sinceWhen__lt=attrs['tilWhen']).exclude(pk=self.instance.pk)
        after = Meeting.objects.filter(tilWhen__gt=attrs['sinceWhen']).exclude(pk=self.instance.pk)

        for i in before:
            if i.tilWhen > attrs['sinceWhen']:
                raise serializers.ValidationError("invalid reservation time 1")

        for j in after:
            if j.sinceWhen < attrs['tilWhen']:
                raise serializers.ValidationError("invalid reservation time 2")

        return attrs