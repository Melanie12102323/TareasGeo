from django.db import models


class Team(models.Model):
  name = models.CharField(max_length=100, verbose_name='Nombre del Equipo')
  description = models.TextField(
      blank=True, null=True, verbose_name='Descripción'
  )
  created_at = models.DateTimeField(
      auto_now_add=True, verbose_name='Fecha de Creación'
  )

  class Meta:
    verbose_name = 'Equipo'
    verbose_name_plural = 'Equipos'

  def __str__(self):
    return self.name


class User(models.Model):
  ROLE_CHOICES = [
      ('admin', 'Administrador'),
      ('member', 'Miembro'),
      ('client', 'Cliente'),
  ]

  name = models.CharField(max_length=100, verbose_name='Nombre Completo')
  email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
  password_hash = models.CharField(
      max_length=255, verbose_name='Hash de Contraseña'
  )
  role = models.CharField(
      max_length=20,
      choices=ROLE_CHOICES,
      default='member',
      verbose_name='Rol',
  )
  avatar_url = models.CharField(
      max_length=255, blank=True, null=True, verbose_name='URL de Avatar'
  )
  created_at = models.DateTimeField(
      auto_now_add=True, verbose_name='Fecha de Creación'
  )
  teams = models.ManyToManyField(
      Team,
      through='TeamMember',
      related_name='members',
      verbose_name='Equipos',
  )

  class Meta:
    verbose_name = 'Usuario'
    verbose_name_plural = 'Usuarios'

  def __str__(self):
    return f'{self.name} ({self.email})'


class TeamMember(models.Model):
  team = models.ForeignKey(
      Team, on_delete=models.CASCADE, verbose_name='Equipo'
  )
  user = models.ForeignKey(
      User, on_delete=models.CASCADE, verbose_name='Usuario'
  )
  joined_at = models.DateTimeField(
      auto_now_add=True, verbose_name='Fecha de Unión'
  )

  class Meta:
    verbose_name = 'Miembro de Equipo'
    verbose_name_plural = 'Miembros de Equipos'
    unique_together = ('team', 'user')

  def __str__(self):
    return f'{self.user.name} en {self.team.name}'


class Project(models.Model):
  name = models.CharField(max_length=150, verbose_name='Nombre del Proyecto')
  description = models.TextField(
      blank=True, null=True, verbose_name='Descripción'
  )
  budget = models.DecimalField(
      max_digits=12, decimal_places=2, verbose_name='Presupuesto'
  )
  deadline = models.DateField(verbose_name='Fecha Límite')
  team = models.ForeignKey(
      Team,
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
      related_name='projects',
      verbose_name='Equipo Asignado',
  )
  created_at = models.DateTimeField(
      auto_now_add=True, verbose_name='Fecha de Creación'
  )

  class Meta:
    verbose_name = 'Proyecto'
    verbose_name_plural = 'Proyectos'

  def __str__(self):
    return self.name


class Tag(models.Model):
  name = models.CharField(max_length=50, unique=True, verbose_name='Etiqueta')
  color = models.CharField(
      max_length=7, default='#000000', verbose_name='Color (HEX)'
  )

  class Meta:
    verbose_name = 'Etiqueta'
    verbose_name_plural = 'Etiquetas'

  def __str__(self):
    return self.name


class Task(models.Model):
  PRIORITY_CHOICES = [
      ('Alta', 'Alta'),
      ('Media', 'Media'),
      ('Baja', 'Baja'),
  ]
  STATUS_CHOICES = [
      ('To-Do', 'Por Hacer'),
      ('Doing', 'En Progreso'),
      ('Done', 'Completado'),
  ]

  project = models.ForeignKey(
      Project,
      on_delete=models.CASCADE,
      related_name='tasks',
      verbose_name='Proyecto',
  )
  title = models.CharField(max_length=200, verbose_name='Título de Tarea')
  description = models.TextField(
      blank=True, null=True, verbose_name='Descripción'
  )
  priority = models.CharField(
      max_length=20,
      choices=PRIORITY_CHOICES,
      default='Media',
      verbose_name='Prioridad',
  )
  status = models.CharField(
      max_length=20,
      choices=STATUS_CHOICES,
      default='To-Do',
      verbose_name='Estado',
  )
  due_date = models.DateField(verbose_name='Fecha Vencimiento')
  assigned_user = models.ForeignKey(
      User,
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
      related_name='assigned_tasks',
      verbose_name='Usuario Asignado',
  )
  assigned_team = models.ForeignKey(
      Team,
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
      related_name='assigned_tasks',
      verbose_name='Equipo Asignado',
  )
  tags = models.ManyToManyField(
      Tag,
      related_name='tasks',
      blank=True,
      verbose_name='Etiquetas',
  )
  created_at = models.DateTimeField(
      auto_now_add=True, verbose_name='Fecha de Creación'
  )
  updated_at = models.DateTimeField(
      auto_now=True, verbose_name='Última Actualización'
  )

  class Meta:
    verbose_name = 'Tarea'
    verbose_name_plural = 'Tareas'

  def __str__(self):
    return self.title


class Subtask(models.Model):
  task = models.ForeignKey(
      Task,
      on_delete=models.CASCADE,
      related_name='subtasks',
      verbose_name='Tarea Principal',
  )
  title = models.CharField(max_length=200, verbose_name='Título Subtarea')
  is_completed = models.BooleanField(
      default=False, verbose_name='Completada'
  )
  position = models.IntegerField(default=0, verbose_name='Posición')

  class Meta:
    verbose_name = 'Subtarea'
    verbose_name_plural = 'Subtareas'

  def __str__(self):
    return self.title


class Comment(models.Model):
  task = models.ForeignKey(
      Task,
      on_delete=models.CASCADE,
      related_name='comments',
      verbose_name='Tarea',
  )
  user = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      related_name='comments',
      verbose_name='Usuario',
  )
  content = models.TextField(verbose_name='Contenido del Comentario')
  created_at = models.DateTimeField(
      auto_now_add=True, verbose_name='Fecha de Creación'
  )

  class Meta:
    verbose_name = 'Comentario'
    verbose_name_plural = 'Comentarios'

  def __str__(self):
    return f'Comentario de {self.user.name} en {self.task.title}'


class TimeLog(models.Model):
  task = models.ForeignKey(
      Task,
      on_delete=models.CASCADE,
      related_name='time_logs',
      verbose_name='Tarea',
  )
  user = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      related_name='time_logs',
      verbose_name='Usuario',
  )
  hours = models.DecimalField(
      max_digits=5, decimal_places=2, verbose_name='Horas Invertidas'
  )
  log_date = models.DateField(verbose_name='Fecha de Registro')
  notes = models.CharField(
      max_length=255, blank=True, null=True, verbose_name='Notas'
  )

  class Meta:
    verbose_name = 'Registro de Tiempo'
    verbose_name_plural = 'Registros de Tiempo'

  def __str__(self):
    return f'{self.hours} hrs - {self.user.name} ({self.log_date})'


class Attachment(models.Model):
  task = models.ForeignKey(
      Task,
      on_delete=models.CASCADE,
      related_name='attachments',
      verbose_name='Tarea',
  )
  uploaded_by = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      related_name='attachments',
      verbose_name='Subido por',
  )
  file_name = models.CharField(max_length=200, verbose_name='Nombre de Archivo')
  file_url = models.CharField(max_length=255, verbose_name='URL del Archivo')
  file_type = models.CharField(max_length=50, verbose_name='Tipo de Archivo')
  created_at = models.DateTimeField(
      auto_now_add=True, verbose_name='Fecha de Subida'
  )

  class Meta:
    verbose_name = 'Adjunto'
    verbose_name_plural = 'Adjuntos'

  def __str__(self):
    return self.file_name


class Notification(models.Model):
  TYPE_CHOICES = [
      ('assigned', 'Asignación'),
      ('due_soon', 'Próximo a vencer'),
      ('comment', 'Comentario'),
  ]

  user = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      related_name='notifications',
      verbose_name='Usuario Destino',
  )
  task = models.ForeignKey(
      Task,
      on_delete=models.CASCADE,
      related_name='notifications',
      verbose_name='Tarea Relacionada',
  )
  type = models.CharField(
      max_length=50, choices=TYPE_CHOICES, verbose_name='Tipo de Notificación'
  )
  message = models.CharField(max_length=255, verbose_name='Mensaje')
  is_read = models.BooleanField(default=False, verbose_name='Leída')
  created_at = models.DateTimeField(
      auto_now_add=True, verbose_name='Fecha de Creación'
  )

  class Meta:
    verbose_name = 'Notificación'
    verbose_name_plural = 'Notificaciones'

  def __str__(self):
    return f'Notificación para {self.user.name} [{self.type}]'