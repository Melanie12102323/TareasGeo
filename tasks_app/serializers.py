import re

from rest_framework import serializers

from .models import (
    Attachment, Comment, Notification, Project, Subtask, Tag,
    Task, Team, TeamMember, TimeLog, User,
)

from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password_hash": {"write_only": True}}

    def create(self, validated_data):
        # Se guarda hasheada, nunca en texto plano
        validated_data["password_hash"] = make_password(validated_data["password_hash"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password_hash" in validated_data:
            validated_data["password_hash"] = make_password(validated_data["password_hash"])
        return super().update(instance, validated_data)


class TeamSerializer(serializers.ModelSerializer):
    # La relación pasa por TeamMember, por eso es solo lectura aquí.
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["id", "name", "description", "members", "created_at"]


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ["id", "team", "user", "joined_at"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "budget", "deadline", "team", "created_at"]

    def validate_budget(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("El presupuesto no puede ser negativo.")
        return value


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "color"]

    def validate_color(self, value):
        if value and not re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
            raise serializers.ValidationError("Usa formato hexadecimal, por ejemplo #FF5733.")
        return value


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ["id", "task", "title", "is_completed", "position"]


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Task
        fields = ["id", "project", "title", "description", "priority", "status",
                  "due_date", "assigned_user", "assigned_team", "tags",
                  "subtasks", "created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "task", "user", "content", "created_at"]


class TimeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLog
        fields = ["id", "task", "user", "hours", "log_date", "notes"]

    def validate_hours(self, value):
        if value <= 0 or value > 24:
            raise serializers.ValidationError("Las horas deben estar entre 0 y 24.")
        return value


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ["id", "task", "uploaded_by", "file_name", "file_url", "file_type", "created_at"]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "user", "task", "type", "message", "is_read", "created_at"]