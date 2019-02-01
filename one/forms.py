from django import forms
from .models import UserInfo
class Form1(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['username', 'password' ]
    def save(self, commit=True):
        self.instance.save()
        return self.instance