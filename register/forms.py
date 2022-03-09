
from django import forms

from .models import profile

class EmployeeForm(forms.ModelForm):
    #to get all fields of profile model
    class Meta:
        model=profile
        fields='__all__'
    
    # its not working but it for use select text instied of "-----" in dropdown 
    def __init__(self,*args,**kwargs):
        super(EmployeeForm,self).__init__(*args,**kwargs)
        self.fields['position'].empty_label="select"