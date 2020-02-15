from django import forms
from django.contrib.auth.models import User
from .models import profile


class user_form(forms.ModelForm):
    username=forms.CharField(label=False,max_length=40,min_length=4,widget=forms.TextInput(attrs={
        'placeholder':'username',
        'required':True,
        'class':'form-control',
    }))
    first_name=forms.CharField(label=False,widget=forms.TextInput(attrs={
        'placeholder':'first name',
        'class':'form-control',

    }))
    last_name=forms.CharField(label=False,widget=forms.TextInput(attrs={
        'placeholder':'last name',
        'class':'form-control',
    }))
    password=forms.CharField(label=False,min_length=5,max_length=30,widget=forms.PasswordInput(attrs={
        'placeholder':'password',
        'class':'form-control',
    }))
    confirm_password=forms.CharField(label=False,min_length=5,max_length=30,widget=forms.PasswordInput(attrs={
        'placeholder':'confirm password',
        'class':'form-control',
    }))

    email=forms.EmailField(label=False,widget=forms.EmailInput(attrs={
        'placeholder':'email',
        'class':'form-control',
    }))

    class Meta:
        model=User
        fields=['username','first_name','last_name','password','email']

    
    def clean_username(self):
        username=self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            raise forms.ValidationError("user name already exists")
        except User.DoesNotExist:
            return username

    def clean_email(self):
        email=self.cleaned_data.get('email')
        user=User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError("email taken")
        return email

    def clean_confirm_password(self):
        password=self.cleaned_data.get('password')
        confirm_password=self.cleaned_data.get('confirm_password')
        if confirm_password != password:
            raise forms.ValidationError('password mismatch')
        return confirm_password

    


class profile_form(forms.ModelForm):
    image=forms.FileField(label=False,required=False)
    class Meta:
        model=profile
        fields=['image']


class login_form(forms.Form):
    username=forms.CharField(label=False,widget=forms.TextInput(attrs={
        'placeholder':'username',
        'class':'form-control',
    }))
    password=forms.CharField(label=False,widget=forms.PasswordInput(attrs={
        'placeholder':'password',
        'class':'form-control',
    }))




class edituserform(forms.ModelForm):
    username=forms.CharField(label=False,max_length=40,min_length=4,widget=forms.TextInput(attrs={
    'placeholder':'username',
    'required':True,
    'class':'form-control',
    }))
    first_name=forms.CharField(label=False,widget=forms.TextInput(attrs={
        'placeholder':'first name',
        'class':'form-control',

    }))
    last_name=forms.CharField(label=False,widget=forms.TextInput(attrs={
        'placeholder':'last name',
        'class':'form-control',
    }))
    password=forms.CharField(label=False,min_length=5,max_length=30,widget=forms.PasswordInput(attrs={
        'placeholder':'password',
        'class':'form-control',
    }))
    confirm_password=forms.CharField(label=False,min_length=5,max_length=30,widget=forms.PasswordInput(attrs={
        'placeholder':'confirm password',
        'class':'form-control',
    }))

    email=forms.EmailField(label=False,widget=forms.EmailInput(attrs={
        'placeholder':'email',
        'class':'form-control',
    }))

    class Meta:
        model=User
        fields=['username','first_name','last_name','password','email']

    
    def clean_username(self):
        username=self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            raise forms.ValidationError("user name already exists")
        except User.DoesNotExist:
            return username

    def clean_email(self):
        email=self.cleaned_data.get('email')
        user=User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError("email taken")
        return email

    def clean_confirm_password(self):
        password=self.cleaned_data.get('password')
        confirm_password=self.cleaned_data.get('confirm_password')
        if confirm_password != password:
            raise forms.ValidationError('password mismatch')
        return confirm_password


    
    

class editprofileform(forms.ModelForm):
    image=forms.FileField(label=False,required=False)
    class Meta:
        model=profile
        fields=['image']


# class edituserform(forms.ModelForm):
#     confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
#         'class':'form-control',
#         'placeholder':'confirmPassword',
#         'name':'confirm_password'
#     }))
#     password=forms.CharField(widget=forms.PasswordInput(attrs={
#     'class':'form-control',
#     'placeholder':'password',
#     }))

#     class Meta:
#         model=User
#         fields=['username','email','password']
#         widgets={
#             'username':forms.TextInput(attrs={
#                 'class':'form-control',
#                 'placeholder':'username'
                
#             }),
#             'email':forms.EmailInput(attrs={
#             'class':'form-control',
#             'placeholder':'email'
#             }),
#         }
#     def clean_username(self):
#         username=self.cleaned_data['username']
#         try:
#             User.objects.get(username=username)
#         except User.DoesNotExist:
#             raise forms.ValidationError("user name must be unique")
#         return username


# class editprofileform(forms.ModelForm):
#     class Meta:
#         model=profile
#         fields=['image']
#         widgets={
#             'image':forms.FileInput(attrs={
#             'class':'form-control'
#             })
#         }
