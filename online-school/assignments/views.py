from django.shortcuts import get_object_or_404

from .models import Classroom, Teacher, Student, AssignmentCompleted, Assignment
from .permissions import AssignmentStudentOrTeacherOwner, TeacherOrReadOnly, TeacherUpdateOwnObject, UpdateOwnObject

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.settings import api_settings

from .serializers import ClassroomSerializer, TeacherSerializer,  StudentSerializer, AssignmentCompletedSerializer, AssignmentSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    """
    CRUD Operation for 'Teacher' instances
    """

    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [UpdateOwnObject]
    filter_backends = [SearchFilter]
    search_fields = ["username"]

    @action(methods=["get"], detail=True, url_path="profile-pic", url_name="profile-pic")
    def get_profile(self, request, pk=None):
        queryset = Teacher.objects.all()
        teacher = get_object_or_404(queryset, pk=pk)
        serializer = TeacherSerializer(teacher, context={"request": request})
        content = {
            "profile_pic": serializer.data["profile_pic"],

        }
        return Response(content)


class StudentViewSet(viewsets.ModelViewSet):
    """     
    CRUD Operation for 'Student' instances
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [UpdateOwnObject]
    filter_backends = [SearchFilter]
    search_fields = ["username", "first_name", "last_name"]

    @action(methods=["get"], detail=True, url_path="profile-pic", url_name="profile-pic")
    def get_profile(self, request, pk=None):
        queryset = Student.objects.all()
        teacher = get_object_or_404(queryset, pk=pk)
        serializer = TeacherSerializer(teacher, context={"request": request})
        content = {
            "profile_pic": serializer.data["profile_pic"],

        }
        return Response(content)


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    CRUD Operation for 'Assignment' instances
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        TeacherOrReadOnly,
        TeacherUpdateOwnObject,
    ]
    filter_backends = [SearchFilter]
    search_fields = ["id", "owner_teacher"]

    def perform_create(self, serializer):
        """ Sets the Assignment owner_teacher to the logged in teacher/user """
        serializer.save(owner_teacher=self.request.user)


class AssignmentCompletedViewSet(viewsets.ModelViewSet):
    """
    CRUD Operation for 'AssignmentCompleted' instances
    """

    queryset = AssignmentCompleted.objects.all()
    serializer_class = AssignmentCompletedSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,
                          AssignmentStudentOrTeacherOwner]

    def perform_create(self, serializer):

        serializer.save(score=None, owner_student=self.request.user)


class ClassroomViewSet(viewsets.ModelViewSet):
    """
    CRUD Operation for 'Classroom' instances
    """
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, TeacherOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner_teacher=self.request.user)


class UserLoginApiView(ObtainAuthToken):
    """ Handle creating user authentication tokens """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
