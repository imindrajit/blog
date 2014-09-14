from blogengine.models import UserProfile, Post
from django.contrib.auth.models import User
from django import forms
from django.template.defaultfilters import slugify


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username']:
            self.fields[fieldname].help_text = None
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('website',)

class AddPostForm(forms.ModelForm):
	
	class Meta:
		model = Post
    	
    	def __init__(self, *args, **kwargs):
        	from django.forms.widgets import HiddenInput
        	hide_condition = kwargs.pop('hide_condition',None)
        	super(AddPostForm, self).__init__(*args, **kwargs)
        	#self.fields['author'].required = False
        	if hide_condition:
				self.fields['author'].widget = HiddenInput()
				#self.fields['url'].widget = HiddenInput()
				self.fields['pub_date'].widget = HiddenInput()
				self.fields['views'].widget = HiddenInput()

		