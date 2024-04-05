from rest_framework import serializers
from fit.models import CustomUser, Gym, FitnessTrainer, Schedule, Appointment


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'is_client', 'is_trainer', 'is_admin']


class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ['id', 'name', 'address']


class FitnessTrainerSerializer(serializers.ModelSerializer):
    profile_image: str = serializers.ImageField(read_only=True)
    
    class Meta:
        model = FitnessTrainer
        fields = ['user', 'full_name', 'date_of_birth', 'gender', 'gyms', 'profile_image']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'trainer', 'gym', 'day_of_week', 'start_time', 'end_time']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'client', 'trainer', 'schedule', 'appointment_date', 'appointment_time', 'status']
