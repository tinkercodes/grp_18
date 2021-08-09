from django import forms
from . import choices

class check_post_form(forms.Form):
	state = forms.ChoiceField(choices=choices.states)
	district = forms.ChoiceField(choices=choices.district_26)
	place = forms.CharField(max_length=30,min_length=10,strip=True)
	pincode = forms.CharField(max_length=6,min_length=6)

	state.widget.attrs.update({'class': 'form-control-sm form-control form-select form-select-sm text-center'})
	district.widget.attrs.update({'class': 'form-control-sm form-control form-select form-select-sm text-center'})
	place.widget.attrs.update({'class': 'form-control-sm form-control'})
	pincode.widget.attrs.update({'class': 'form-control-sm form-control'})


class check_post_login_form(forms.Form):
	state = forms.ChoiceField(choices=choices.states)
	district = forms.ChoiceField(choices=choices.district_26)
	pincode = forms.CharField(max_length=6,min_length=6)
	check_post_id = forms.CharField(max_length=10,min_length=10)

	state.widget.attrs.update({'class': 'form-control-sm form-control form-select form-select-sm text-center'})
	district.widget.attrs.update({'class': 'form-control-sm form-control form-select form-select-sm text-center'})
	pincode.widget.attrs.update({'class': 'form-control-sm form-control'})
	check_post_id.widget.attrs.update({'class': 'form-control-sm form-control'})

class user_registration_form(forms.Form):
	first_name = forms.CharField(max_length=10,min_length=10)
	last_name = forms.CharField(max_length=10,min_length=10)
	check_post_id = forms.CharField(max_length=10,min_length=10)
	email = forms.EmailField()
	password = forms.CharField(max_length=12,min_length=4)

	first_name.widget.attrs.update({'class': 'form-control-sm form-control'})
	last_name.widget.attrs.update({'class': 'form-control-sm form-control'})
	check_post_id.widget.attrs.update({'class': 'form-control-sm form-control'})
	email.widget.attrs.update({'class': 'form-control-sm form-control'})
	password.widget.attrs.update({'class':'form-control-sm form-control', 'type':'password'})

class user_login_form(forms.Form):

	email = forms.EmailField()
	password = forms.CharField(max_length=12,min_length=4)

	email.widget.attrs.update({'class': 'form-control-sm form-control'})
	password.widget.attrs.update({'class':'form-control-sm form-control', 'type':'password'})
