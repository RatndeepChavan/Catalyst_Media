from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import MyUser, Status, Tran


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control rounded-pill text-center', 'placeholder':'Enter Password'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class':'form-control rounded-pill text-center', 'placeholder':'Re-enter Password'}))
    class Meta:
        model = MyUser
        fields = ['email']

        widgets = {'email' : forms.EmailInput(attrs={'class':'form-control rounded-pill text-center', 'placeholder':'Enter Email'})}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id','email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ("User data : ", {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('id','email','is_admin')
    filter_horizontal = ()

@admin.register(Status)
class Adstatus(admin.ModelAdmin):
    model= Status
    list_display = ['id', 'em', 'st', 'bl']

@admin.register(Tran)
class Adtran(admin.ModelAdmin):
    model= Tran
    list_display = ['id', 'us', 'am', 'dt']

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
