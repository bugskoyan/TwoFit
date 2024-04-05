from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from fit.models import CustomUser, Gym, FitnessTrainer, Schedule, Appointment
from fit.serializers import CustomUserSerializer, GymSerializer, FitnessTrainerSerializer, ScheduleSerializer, AppointmentSerializer

from .forms import AppointmentForm


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class GymViewSet(viewsets.ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer


class FitnessTrainerViewSet(viewsets.ModelViewSet):
    queryset = FitnessTrainer.objects.all()
    serializer_class = FitnessTrainerSerializer

    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        trainer = self.get_object()
        schedules = Schedule.objects.filter(trainer=trainer)
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])  
    def make_appointment(self, request, pk=None):
        trainer = self.get_object()
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            trainer_pk = self.kwargs.get('pk') 
            trainer = get_object_or_404(FitnessTrainer, pk=trainer_pk)
            appointment.trainer = trainer
            gym = form.cleaned_data['gym']
            schedule = Schedule.objects.create(
                trainer=trainer,
                gym=gym,  
                day_of_week=form.cleaned_data['day_of_week'],
                start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time']
            )
            appointment.schedule = schedule
            appointment.save()
            return redirect('index')  
        return render(request, 'make_appointment.html', {'form': form, 'trainer': trainer})

    def list(self, request):
        trainers = self.get_queryset()
        return render(request, 'trainer_list.html', {'trainers': trainers})

    def retrieve(self, request, pk=None):
        trainer = self.get_object()
        return render(request, 'trainer_detail.html', {'trainer': trainer})


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def retrieve(self, request, pk=None):
        trainer_schedules = Schedule.objects.filter(trainer=pk)
        trainer = FitnessTrainer.objects.get(pk=pk) 
        return render(request, 'schedule_detail.html', {'schedules': trainer_schedules, 'trainer': trainer})


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


def index(request):
    return render(request, 'index.html')


