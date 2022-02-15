from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


def profile_pic_upload_directory_path(instance, filename):
    """
    file will be uploaded to uploads/profiles/<type>/<username>/<filename>
    """
    return 'uploads/profiles/{0}/{1}/{2}'.format(instance.type, instance.username, filename)


class CustomUserManager(BaseUserManager):
    """ Custom user db model manager """

    # Manually handle user creation so password get's hashed
    def create_user(self, username: str, first_name: str = None, last_name: str = None, password=None):

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    # Create and save a new superuser with given details
    def create_superuser(self, username: str, password):
        user = self.create_user(username=username, password=password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class TeacherManager(CustomUserManager):
    """ Teacher db model manager """

    # Only return users that are type 'teacher'
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.TEACHER)


class StudentManager(CustomUserManager):
    """ Student db model manager """

    # Only return users that are type 'student'
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.STUDENT)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """ Database model for Teachers and Students in the system """

    class Types(models.TextChoices):
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"

    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to=profile_pic_upload_directory_path, blank=True)
    type = models.CharField(
        max_length=50, choices=Types.choices, default=Types.TEACHER)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["first_name", "last_name"]


class Teacher(CustomUser):
    """
    Teacher proxy model is like a reference to 'CustomUser' model
    that wont create a new table for 'Teacher'
    """
    objects = TeacherManager()

    class Meta:
        proxy = True

    # When create a new instance of this model, type field will be set to 'TEACHER'
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = CustomUser.Types.TEACHER
        return super().save(*args, **kwargs)


class Student(CustomUser):
    """
    Student proxy model is like a reference to 'CustomUser' model
    that wont create a new table for 'Student'
    """

    objects = StudentManager()

    class Meta:
        proxy = True

    # When create a new instance of this model, type field will be set to 'STUDENT'
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = CustomUser.Types.STUDENT
        return super().save(*args, **kwargs)


def attachment_upload_path(instance, filename):

    # return f"uploads/attachments/{instance.date_created}/{filename}"
    return f"uploads/attachments/{filename}"


class Assignment(models.Model):
    """ Assignments database model in system """
    title = models.CharField(max_length=50)
    more = models.TextField(max_length=1000, default="")
    attachment = models.FileField(
        upload_to=attachment_upload_path, max_length=100)
    classroom = models.ForeignKey(
        "Classroom", on_delete=models.CASCADE, null=True)
    students_that_completed = models.ManyToManyField(
        Student, blank=True, related_name="completed_assignments")
    owner_teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="assignments")
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class AssignmentCompleted(models.Model):
    """ Submitted Assisgnments by students, database model in system """
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    score = models.IntegerField(max_length=100, null=True, blank=True)
    accepted = models.BooleanField(default=False)
    attachment = models.FileField(
        upload_to=attachment_upload_path, max_length=100, null=True)
    more = models.TextField(max_length=500, blank=True)
    owner_student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.assignment.title


class Classroom(models.Model):
    """ Database model for 'Classroom' in the system """
    class_name = models.CharField(max_length=100)
    owner_teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.class_name)
