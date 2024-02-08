
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import UserTaskAccount, UserAddress


class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))

    city = forms.CharField(max_length=100)

    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name',
                  'last_name', 'email', 'birth_date', 'city', 'country']

        # form.save()
    def save(self, commit=True):
        our_user = super().save(commit=False)  # ami database e data save korbo na ekhn
        if commit == True:
            our_user.save()  # user model e data save korlam

            country = self.cleaned_data.get('country')
            birth_date = self.cleaned_data.get('birth_date')
            city = self.cleaned_data.get('city')

            UserAddress.objects.create(
                user=our_user,
                country=country,
                city=city,

            )
            UserTaskAccount.objects.create(
                user=our_user,
                birth_date=birth_date,
                account_no=100000 + our_user.id
            )
        return our_user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))

    city = forms.CharField(max_length=100)

    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except UserTaskAccount.DoesNotExist:
                user_account = None
                user_address = None

            if user_account:

                self.fields['birth_date'].initial = user_account.birth_date

                self.fields['city'].initial = user_address.city

                self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_account, created = UserTaskAccount.objects.get_or_create(
                user=user)
            user_address, created = UserAddress.objects.get_or_create(
                user=user)
            #UserTaskAccount er data save
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()
            #userAddress er data save
            user_address.city = self.cleaned_data['city']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user

class ChangeUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']