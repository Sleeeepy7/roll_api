import datetime
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Poll, Question, Choice, Answer, Vote
from .fields import ObjectIDField


class ChoiceSerializer(serializers.ModelSerializer):
    """
    Choice serializer.
    """
    class Meta:
        model = Choice
        fields = ('id', 'text')
        read_only_fields = ('id', )


class QuestionSerializer(serializers.ModelSerializer):
    """
    Question serializer.
    """
    type = serializers.ChoiceField(
        choices=Question.Type.choices, default=Question.Type.TEXT
    )
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id', 'poll', 'text', 'type', 'choices')
        read_only_fields = ('id', )
        extra_kwargs = {
            'poll': {'write_only': True}
        }

    def create_choices(self, question, choices):
        Choice.objects.bulk_create([
            Choice(question=question, **d) for d in choices
        ])

    def create(self, validated_data):
        choices = validated_data.pop('choices', [])
        question = Question.objects.create(**validated_data)
        self.create_choices(question, choices)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop('choices', [])
        instance.choices.all().delete()
        self.create_choices(instance, choices)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class PollSerializer(serializers.ModelSerializer):
    """
    Poll serializer.
    """
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'start_date', 'end_date', 'description', 'questions')
        read_only_fields = ('id', )

    def validate_start_date(self, value):
        """
        Raise error if try to change start_date after poll started.
        """
        if self.instance and self.instance.start_date < value:
            raise serializers.ValidationError(
                "Not allow change start_date poll is started"
            )

        return value


class AnswerSerializer(serializers.ModelSerializer):
    """
    Answer in Vote read/write serializer.
    """
    choice = ChoiceSerializer(read_only=True)
    choice_id = ObjectIDField(queryset=Choice.objects.all(), write_only=True)

    question = QuestionSerializer(read_only=True)
    question_id = ObjectIDField(queryset=Question.objects.all(), write_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'question_id', 'question', 'choice_id', 'choice', 'value')
        read_only_fields = ('id', )


class VoteSerializer(serializers.ModelSerializer):

    """
    Vote on Poll read/write serializer.
    """
    answers = AnswerSerializer(many=True)
    poll = PollSerializer(read_only=True)
    poll_id = ObjectIDField(
        queryset=Poll.objects.filter(end_date__gte=datetime.date.today()),
        write_only=True
    )

    class Meta:
        model = Vote
        fields = ('id', 'poll_id', 'poll', 'user', 'date', 'answers')
        read_only_fields = ('id', 'user', 'date')

    def create(self, validated_data):
        answers = validated_data.pop('answers', [])
        instance = Vote.objects.create(**validated_data)
        Answer.objects.bulk_create([
            Answer(vote=instance, **a) for a in answers
        ])
        return instance
