from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.fit import views

from rest_framework.routers import DefaultRouter
from apps.fit.views import (CustomUserViewSet, GymViewSet, FitnessTrainerViewSet, 
                            ScheduleViewSet, AppointmentViewSet)


router = DefaultRouter()


router.register(r'users', CustomUserViewSet)
router.register(r'gyms', GymViewSet)
router.register(r'trainers', FitnessTrainerViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'appointments', AppointmentViewSet)
# router.register(r'registration', RegistrationViewSet, basename='registration')
# router.register(r'login', LoginViewSet, basename='login')
# router.register(r'index', IndexViewSet, basename='index')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('main/', views.index, name='index'),
    path('trainers/', FitnessTrainerViewSet.as_view({'get': 'list'}), name='trainer_list'),
    path('trainer/<int:pk>/', FitnessTrainerViewSet.as_view({'get': 'retrieve'}), name='trainer_detail'),
    path('make_appointment/', FitnessTrainerViewSet.as_view({'post': 'make_appointment'}), name='make_appointment'),
    path('trainer/<int:pk>/make_appointment/', FitnessTrainerViewSet.as_view({'post': 'make_appointment'}), name='make_appointment'),
    path('schedule/<int:pk>/', ScheduleViewSet.as_view({'get': 'retrieve'}), name='schedule_detail'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
