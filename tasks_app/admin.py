from django.contrib import admin
from .models import (
    Attachment,
    Comment,
    Notification,
    Project,
    Subtask,
    Tag,
    Task,
    Team,
    TeamMember,
    TimeLog,
    User,
)


class TeamMemberInline(admin.TabularInline):
  model = TeamMember
  extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
  list_display = ('name', 'created_at')
  search_fields = ('name',)
  inlines = [TeamMemberInline]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ('name', 'email', 'role', 'created_at')
  list_filter = ('role',)
  search_fields = ('name', 'email')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
  list_display = ('name', 'budget', 'deadline', 'team', 'created_at')
  list_filter = ('deadline', 'team')
  search_fields = ('name', 'description')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
  list_display = ('name', 'color')
  search_fields = ('name',)


class SubtaskInline(admin.TabularInline):
  model = Subtask
  extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
  list_display = (
      'title',
      'project',
      'priority',
      'status',
      'due_date',
      'assigned_user',
  )
  list_filter = ('priority', 'status', 'project')
  search_fields = ('title', 'description')
  inlines = [SubtaskInline]


@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
  list_display = ('title', 'task', 'is_completed', 'position')
  list_filter = ('is_completed',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = ('task', 'user', 'created_at')
  search_fields = ('content',)


@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
  list_display = ('task', 'user', 'hours', 'log_date')
  list_filter = ('log_date',)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
  list_display = ('file_name', 'task', 'uploaded_by', 'file_type', 'created_at')
  search_fields = ('file_name',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
  list_display = ('user', 'task', 'type', 'is_read', 'created_at')
  list_filter = ('is_read', 'type')