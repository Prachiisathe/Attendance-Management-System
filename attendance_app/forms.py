from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

    def clean_student_name(self):
        name = self.cleaned_data.get("student_name")
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Name cannot contain numbers")
        return name

    def clean_roll_no(self):
        roll = self.cleaned_data.get("roll_no")
        if not roll:
            raise forms.ValidationError("Roll number required")
        return roll

    def clean_phone_no(self):
        phone = self.cleaned_data.get("phone_no")
        if not phone.isdigit():
            raise forms.ValidationError("Only digits allowed")

        if len(phone) != 10:
            raise forms.ValidationError("Phone must be exactly 10 digits")

        return phone
def clean_address(self):
    roll = self.cleaned_data.get("address")
    if not address:
        raise forms.ValidationError("Address required")
    return address
