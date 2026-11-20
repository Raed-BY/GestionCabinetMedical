from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

    doctor = models.ForeignKey('AccountApp.Doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey('AccountApp.Patient', on_delete=models.CASCADE)
    
    reason = models.TextField()
    prescription = models.FileField(
        upload_to='prescriptions/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    duration_minutes = models.PositiveIntegerField(default=30)
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['appointment_date']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'], 
                name='unique_doctor_appointment'
            )
        ]
    def clean(self):
        super().clean()
        if self.appointment_date and self.appointment_date <= timezone.now():
            raise ValidationError({'appointment_date': "La date du rendez-vous doit être dans le futur."})

    def __str__(self):
        return f"RDV: {self.patient} avec {self.doctor} le {self.appointment_date}"