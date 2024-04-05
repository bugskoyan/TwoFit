from django.contrib import admin

from fit.models import CustomUser, Gym, FitnessTrainer, Schedule, Appointment


admin.site.register(CustomUser)
admin.site.register(Gym)
admin.site.register(FitnessTrainer)
admin.site.register(Schedule)
admin.site.register(Appointment)