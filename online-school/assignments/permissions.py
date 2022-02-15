from .models import CustomUser
from rest_framework import permissions


class UpdateOwnObject(permissions.BasePermission):
    """ Allow user to edit their own profile """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class TeacherUpdateOwnObject(permissions.BasePermission):
    """ Allow 'Teacher' to update instances they own, e.g. (profile,assignment...) """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner_teacher == request.user


class TeacherOrReadOnly(permissions.BasePermission):
    """ if user type is 'Teacher' he can create or update otherwise can only read the content """

    def has_permission(self, request, view):
        is_teacher = request.user.type == CustomUser.Types.TEACHER
        if request.method in permissions.SAFE_METHODS:
            return True
        return is_teacher


class StudentUpdateOwnObject(permissions.BasePermission):
    """ Allow 'Student' to update instances they own, e.g. (profile,submitted assignment...) """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner_student == request.user


class StudentOrReadOnly(permissions.BasePermission):
    """ Allow to 'Student' to update instances they own, e.g. (profile,submitted assignment...) """

    def has_permission(self, request, view):
        is_student = request.user.type == CustomUser.Types.STUDENT
        if request.method in permissions.SAFE_METHODS:
            return True

        return is_student


class AssignmentStudentOrTeacherOwner(permissions.BasePermission):
    """
    Students can edit their submitted assignment/AssignmentCompleted.
    Assignment owner also can edit their submission to set 'Score' field
    """

    def has_permission(self, request, view):
        is_student = request.user.type == CustomUser.Types.STUDENT
        is_teacher = request.user.type == CustomUser.Types.TEACHER

        is_get = request.method == "GET"
        is_patch = request.method == "PATCH"

        # Teachers that own the assignment can view and edit related submitted assignments
        if is_get or is_patch and is_teacher:
            return True

        return is_student

    def has_object_permission(self, request, view, obj):
        is_student = request.user.type == CustomUser.Types.STUDENT
        is_submitted_assignment_owner_student = obj.owner_student == request.user
        is_teacher = request.user.type == CustomUser.Types.TEACHER
        is_assignment_owner_teacher = obj.assignment.owner_teacher == request.user

        is_get = request.method == "GET"
        is_patch = request.method == "PATCH"

        # Students can edit and view their own submitted assignment.
        # Teachers that own the assignment can view specific submitted assignment.
        if is_get or is_patch and is_assignment_owner_teacher:
            return True

        return is_submitted_assignment_owner_student
