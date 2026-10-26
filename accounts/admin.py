from django.contrib import admin
from django.contrib.auth.hashers import identify_hasher, make_password
from .models import Student, PasswordResetOTP, SignupOTP

class StudentAdmin(admin.ModelAdmin):
    list_display = ('registration_id', 'full_name', 'email', 'department')
    search_fields = ('registration_id', 'full_name', 'email')

    def save_model(self, request, obj, form, change):
        if obj.password:
            try:
                identify_hasher(obj.password)
            except ValueError:
                obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(Student, StudentAdmin)
admin.site.register(PasswordResetOTP)
admin.site.register(SignupOTP)
