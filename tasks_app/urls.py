from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("users", views.UserViewSet)
router.register("teams", views.TeamViewSet)
router.register("team-members", views.TeamMemberViewSet)
router.register("projects", views.ProjectViewSet)
router.register("tags", views.TagViewSet)
router.register("tasks", views.TaskViewSet, basename="task")
router.register("subtasks", views.SubtaskViewSet)
router.register("comments", views.CommentViewSet)
router.register("time-logs", views.TimeLogViewSet)
router.register("attachments", views.AttachmentViewSet)
router.register("notifications", views.NotificationViewSet)

urlpatterns = [path("", include(router.urls))]