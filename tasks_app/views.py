from rest_framework import viewsets

from .models import (
    Attachment, Comment, Notification, Project, Subtask, Tag,
    Task, Team, TeamMember, TimeLog, User,
)
from .serializers import (
    AttachmentSerializer, CommentSerializer, NotificationSerializer,
    ProjectSerializer, SubtaskSerializer, TagSerializer, TaskSerializer,
    TeamMemberSerializer, TeamSerializer, TimeLogSerializer, UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.select_related("team", "user")
    serializer_class = TeamMemberSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related("team")
    serializer_class = ProjectSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        qs = Task.objects.select_related("project").prefetch_related("tags", "subtasks")
        status = self.request.query_params.get("status")
        project = self.request.query_params.get("project")
        if status:
            qs = qs.filter(status=status)
        if project:
            qs = qs.filter(project_id=project)
        return qs


class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("task", "user")
    serializer_class = CommentSerializer


class TimeLogViewSet(viewsets.ModelViewSet):
    queryset = TimeLog.objects.select_related("task", "user")
    serializer_class = TimeLogSerializer


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.select_related("task", "uploaded_by")
    serializer_class = AttachmentSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.select_related("task", "user")
    serializer_class = NotificationSerializer