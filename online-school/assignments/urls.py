from django.conf.urls import url
from django.urls import path, include
from . import views
from rest_framework.authtoken import views as drf_views
from rest_framework.routers import DefaultRouter
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Setting up drf yasg stuff
schema_view = get_schema_view(
    openapi.Info(
        title="Online School API",
        default_version='v1',
        description="Online school API",
        contact=openapi.Contact(email="mr.amir.rezazadehh@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"teachers", views.TeacherViewSet)
router.register(r"students", views.StudentViewSet)
router.register(r"assignments", views.AssignmentViewSet)
router.register(r"assignments-completed", views.AssignmentCompletedViewSet)
router.register(r"classrooms", views.ClassroomViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.UserLoginApiView.as_view(), name="login-api-view"),

    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger',
                                           cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc',
                                         cache_timeout=0), name='schema-redoc'),
]
