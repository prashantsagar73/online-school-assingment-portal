from enum import unique

from django.db import transaction
from .models import Teacher, Student, Assignment, AssignmentCompleted, Classroom
from rest_framework import serializers


class TeacherSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedRelatedField(
        view_name="teacher-detail", read_only=True)

    class Meta:
        model = Teacher
        fields = ["id", "username", "password",
                  "profile_pic", "first_name", "last_name", "type"]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"}
            },
            "type": {"read_only": True}
        }

    def create(self, validated_data):
        """ Create and return a new user """
        user = Teacher.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"]
        )

        return user


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["id", "username", "password",
                  "first_name", "last_name", "profile_pic", "type"]

        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
            "type": {"read_only": True}
        }

    def create(self, validated_data):
        """ Create and return a new user """
        user = Student.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"]
        )

        return user


class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = "__all__"
        extra_kwargs = {"owner_teacher": {"read_only": True}}


class AssignmentCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentCompleted
        fields = "__all__"
        extra_kwargs = {
            "owner_student": {"read_only": True}
        }


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = "__all__"
        extra_kwargs = {
            "owner_teacher": {"read_only": True}
        }
