from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError


class MyUserManager(BaseUserManager):
    """ClientManager."""

    def create_user(
        self,
        email: str,
        password: str
    ) -> 'CustomUser':

        if not email:
            raise ValidationError('Email required')

        custom_user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        custom_user.set_password(password)
        custom_user.save(using=self._db)
        return custom_user

    def create_superuser(
        self,
        email: str,
        password: str
    ) -> 'CustomUser':

        custom_user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        custom_user.is_superuser = True
        custom_user.is_active = True
        custom_user.is_staff = True
        custom_user.set_password(password)
        custom_user.save(using=self._db)
        return


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='почта', 
        unique=True
    )
    is_client = models.BooleanField(
        verbose_name = 'клиент',
        default=False
    )
    is_trainer = models.BooleanField(
        verbose_name = 'тренер',
        default=False
    )
    is_admin = models.BooleanField(
        verbose_name = 'админ',
        default=False
    )
    is_active = models.BooleanField(
        verbose_name = 'активный',
        default=True
    )
    is_staff = models.BooleanField(
        verbose_name = 'в штате',
        default=False
    )

    objects = MyUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'{self.email}'


class Gym(models.Model):
    name = models.CharField(
        verbose_name = 'спортзал',
        max_length=50
    )
    address = models.CharField(
        verbose_name='адресс', 
        max_length=100
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'

    def __str__(self) -> str:
        return f'{self.name}'


class FitnessTrainer(models.Model):
    user = models.OneToOneField(
        verbose_name = 'фитнесс-тренер',
        to = CustomUser, 
        on_delete=models.CASCADE, 
        primary_key=True
    )
    full_name = models.CharField(
        verbose_name = 'полное имя',
        max_length=200
    )
    date_of_birth = models.DateField(
        verbose_name = 'дата рождения',
    )
    gender = models.CharField(
        verbose_name = 'пол',
        max_length=10, 
        choices=[('male', 'Мужчина'), ('female', 'Женщина')]
    )
    gyms = models.ManyToManyField(
        verbose_name = 'спортзалы',
        to= Gym, 
        related_name='trainers'
    )
    profile_image = models.ImageField(
        verbose_name='фото профиля', 
        upload_to='profile_images/', 
        null=True, 
        blank=True,
        default= 'default_profile.jpg'
    )

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренера'

    def __str__(self) -> str:
        return f'{self.full_name} | {self.user}'
    

class Schedule(models.Model):
    trainer = models.ForeignKey(
        verbose_name = 'расписание тренеров',
        to = FitnessTrainer, 
        on_delete=models.CASCADE, 
        related_name='schedules'
    )
    gym = models.ForeignKey(
        verbose_name = 'спортзал',
        to = Gym, 
        on_delete=models.CASCADE
    )
    day_of_week = models.CharField(
        verbose_name = 'день недели',
        max_length=20, 
        choices=[('monday', 'Понедельник'), ('tuesday', 'Вторник'), ('wednesday', 'Среда'), ('thursday', 'Четверг'), ('friday', 'Пятница'), ('saturday', 'Суббота'), ('sunday', 'Воскресенье')]
    )
    start_time = models.TimeField(
        verbose_name = 'начало',
    )
    end_time = models.TimeField(
        verbose_name = 'конец',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписании'

    def __str__(self) -> str:
        return f'{self.trainer} | {self.gym} | {self.day_of_week}'


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('confirmed', 'Принято'),
        ('cancelled', 'Отменено'),
    ]

    client = models.ForeignKey(
        verbose_name = 'клиент',
        to = CustomUser, 
        on_delete=models.CASCADE, 
        related_name='appointments'
    )
    trainer = models.ForeignKey(
        verbose_name = 'тренер',
        to=FitnessTrainer, 
        on_delete=models.CASCADE
    )
    schedule = models.ForeignKey(
        verbose_name = 'расписание',
        to = Schedule, 
        on_delete=models.CASCADE
    )
    appointment_date = models.DateField(
        verbose_name = 'дата тренировки',
    )
    appointment_time = models.TimeField(
        verbose_name = 'время тренировки',
    )
    status = models.CharField(
        verbose_name='статус', 
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Встреча'
        verbose_name_plural = 'Встречи'

    def __str__(self) -> str:
        return f'{self.client} | {self.trainer} | {self.appointment_date} | {self.status}'

    
