
from django.db import models
from django.contrib.auth.models import User
from django.db import models



class abstractclass(models.Model):
    #use abstract class if u have common field in any of instance
    #in my case incharge is common for some employees
    #use related_name if refer same field more than one times 
    incharge=models.ForeignKey(User,on_delete=models.CASCADE,related_name='+',null=True,blank=True)
    #use related name if u use two foreignkey for same field in my case {User } in incharge & user in profile
    class Meta:
        abstract=True

    
    
#mention it is extent abstract class
class profile(abstractclass):
    # for drop down selection
    POSITION_TYPE=(
    ('manager','manager'),
    ('admin','admin'),
    ('employee','employee'),
    )
    #models feilds
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name= models.CharField(max_length=100,null=True,blank=True)
    empCode= models.CharField(max_length=10,null=True,blank=True)
    phoneNo= models.CharField(max_length=15,null=True,blank=True)
    position= models.CharField(max_length=20, choices=POSITION_TYPE,null=True,blank=True)
    # to get name field of respective object instead of pointer to it
    def __str__(self):
        return self.name
