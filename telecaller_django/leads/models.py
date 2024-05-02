from django.db import models

# Create your models here.
class LogRegister_Details(models.Model):
    log_username = models.CharField(max_length=255,default='',null=True,blank=True)
    log_password = models.CharField(max_length=255,default='',null=True,blank=True)
    log_date = models.DateField(auto_now_add=True,null=True)
    log_time = models.TimeField(auto_now_add=True,null=True)
    position = models.CharField(max_length=255,default='',null=True,blank=True)
    is_staff = models.IntegerField(default=0)
    active_status = models.IntegerField(default=0)   

    def __str__(self):
        return self.log_username


class EmployeeRegister_Details(models.Model):
    logreg_id = models.ForeignKey(LogRegister_Details, on_delete=models.CASCADE, null=True,default='')
    emp_name = models.CharField(max_length=255,default='',null=True,blank=True)
    emp_contact_no = models.CharField(max_length=255,default='',null=True,blank=True)
    emp_email =  models.EmailField(max_length=255,default='email@gmail.com')
   
    def __str__(self):
        return self.emp_name

class Leads(models.Model):
  
    lead_name = models.CharField(max_length=255,default='',null=True,blank=True)
    lead_email = models.EmailField(default='',null=True,blank=True)
    lead_contact = models.CharField(max_length=255,default='',null=True,blank=True)

    def __str__(self):
        return self.lead_name

   

class Leads_assignto_tc(models.Model):
    leadId = models.ForeignKey(Leads, on_delete=models.CASCADE, null=True,default='')
    # dataBank_ID = models.ForeignKey(DataBank, on_delete=models.CASCADE, null=True,default='')
    TC_Id =  models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
    Response = models.CharField(max_length=255,default='',null=True,blank=True)
    Reason = models.CharField(max_length=255,default='',null=True,blank=True)
    Assign_Date = models.DateField(auto_now_add=True,null=True)
    Allocate_time = models.TimeField(default='00:00:00')
    Update_Date = models.DateField(auto_now_add=False,null=True,)
    Next_update_date = models.DateField(auto_now_add=False,null=True)
    Update_Action = models.IntegerField(default=0)
    Status = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.TC_Id

    # client_id = models.ForeignKey(ClientRegister, on_delete=models.CASCADE, null=True,default='')  



# class Waste_Leads(models.Model):
#     leadId = models.ForeignKey(Leads, on_delete=models.CASCADE, null=True,default='')
#     assignto_tc_id = models.ForeignKey(Leads_assignto_tc, on_delete=models.CASCADE, null=True,default='')
#     dbId = models.ForeignKey(DataBank, on_delete=models.CASCADE, null=True,default='')
#     client_id = models.ForeignKey(ClientRegister, on_delete=models.CASCADE, null=True,default='') 
#     TC_Id =  models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
#     waste_marked_Date = models.DateField(auto_now_add=True,null=True)
#     reason = models.TextField(default='')
#     Status = models.IntegerField(default=0)
#     head_reason = models.TextField(default='')
#     confirmation = models.IntegerField(default=0)





# class FollowupStatus(models.Model):
#     status_name = models.CharField(max_length=150,default='')
#     company_Id = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True,default='')


# class FollowupDetails(models.Model):
#     lead_Id = models.ForeignKey(Leads, on_delete=models.CASCADE, null=True,default='')
#     comp_Id = models.ForeignKey(BusinessRegister_Details, on_delete=models.CASCADE, null=True,default='')
#     hr_telecaller_Id = models.ForeignKey(EmployeeRegister_Details, on_delete=models.CASCADE, null=True,default='')
#     response_date = models.DateField(auto_now_add=True,null=True)
#     response = models.TextField(default='',null=True,blank=True)
#     nextfollowup_date = models.DateField(auto_now_add=False,null=True)
#     response_status = models.CharField(max_length=150,default='')    
