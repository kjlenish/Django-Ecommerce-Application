from django.contrib import admin
from .models import CustomerProfile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(CustomerProfile)

class ProfileInline(admin.StackedInline):
    model = CustomerProfile
    fields = ['gender', 'dob', 'email', 'country_code', 'phone', 'primary_address']
    
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name']
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
