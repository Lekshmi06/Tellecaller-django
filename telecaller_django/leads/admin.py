from django.contrib import admin
from .models import Leads_assignto_tc, Leads, CustomUser, EmployeeRegister_Details

# Register your models here.
admin.site.register(Leads)
admin.site.register(Leads_assignto_tc)
admin.site.register(CustomUser)
admin.site.register(EmployeeRegister_Details)