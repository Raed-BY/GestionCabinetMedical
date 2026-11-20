from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor, Patient, Specialty

admin.site.register(User, UserAdmin)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'license_number')
    search_fields = ('username', 'license_number')
    
    def get_readonly_fields(self, request, obj=None):
        if obj: 
            return ('license_number',)
        return ()

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'national_id', 'phone')
    search_fields = ('username', 'national_id', 'phone')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('national_id',)
        return ()

# 4. Specialty
@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)