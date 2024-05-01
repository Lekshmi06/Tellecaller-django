from django.contrib import admin
from .models import Leads_assignto_tc, Leads, LogRegister_Details, EmployeeRegister_Details

# Register your models here.
admin.site.register(Leads)
admin.site.register(Leads_assignto_tc)
admin.site.register(LogRegister_Details)
admin.site.register(EmployeeRegister_Details)