from django import forms
from .models import *




def create_dynamic_form(fields):
    class DynamicForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field_instance in fields.items():
                self.fields[field_name] = field_instance
    return DynamicForm
# --------------------------------ok


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'position']


from django import forms

class DynamicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Extract dynamic fields from kwargs
        dynamic_fields = kwargs.pop('dynamic_fields', {})
        print(dynamic_fields,"dynamic_fields")
        instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        # Add dynamic fields to the form
        for field_name, field_options in dynamic_fields.items():
            field_type = field_options.get('type', forms.CharField)
            self.fields[field_name] = field_type(**field_options)

        # Pre-fill the form with instance data if provided
        if instance:
            for field_name in dynamic_fields.keys():
                if hasattr(instance, field_name):
                    self.fields[field_name].initial = getattr(instance, field_name)




def get_dynamic_form(user_profile):
    dynamic_data = user_profile.dynamic_data.data if user_profile.dynamic_data else {}
    fields = {}
    for key, value in dynamic_data.items():
        field_type = value.get('input_type', 'text')
        print(field_type)
        if field_type == 'text':
            fields[key] = forms.CharField(required=False, initial=value.get('additional_value', ''))
        elif field_type == 'dropdown':
            choices = [(opt.strip(), opt.strip()) for opt in value.get('additional_value', '').split(',')]
            fields[key] = forms.ChoiceField(choices=choices, required=False, initial=value.get('additional_value', ''))
        elif field_type == 'checkbox':
            fields[key] = forms.BooleanField(required=False, initial=value.get('additional_value', ''))
        elif field_type == 'numerical':
            fields[key] = forms.DecimalField(required=False, initial=value.get('additional_value', ''))
        elif field_type == 'date':
            fields[key] = forms.DateField(required=False, initial=value.get('additional_value', ''))
    print("dynamic_data",dynamic_data)
    return DynamicForm
