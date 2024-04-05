from django import forms
from fit.models import Appointment, Schedule, CustomUser, Gym

class AppointmentForm(forms.ModelForm):
    client = forms.ModelChoiceField(label='Клиент',queryset=CustomUser.objects.filter(is_client=True))
    day_of_week = forms.ChoiceField(label='День недели',choices=[('monday', 'Понедельник'), ('tuesday', 'Вторник'), ('wednesday', 'Среда'), ('thursday', 'Четверг'), ('friday', 'Пятница'), ('saturday', 'Суббота'), ('sunday', 'Воскресенье')])
    start_time = forms.TimeField(label='Время начала')
    end_time = forms.TimeField(label='Время окончания')
    gym = forms.ModelChoiceField(label='Спортзал', queryset=Gym.objects.all())
    

    class Meta:
        model = Appointment
        fields = ['client', 'trainer','gym', 'appointment_date', 'appointment_time', 'status', 'day_of_week', 'start_time', 'end_time']


    def save(self, commit=True):
        appointment = super().save(commit=False)
        if commit:
            appointment.save()
        return appointment