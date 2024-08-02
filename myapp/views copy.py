from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
import json
from .models import *


class DeleteUserForm(forms.Form):
    user_email = forms.EmailField()

class SearchUserForm(forms.Form):
    user_email = forms.EmailField()
from django.shortcuts import render, redirect
from django import forms
import json

# Define your dynamic form creation function
def create_dynamic_form(fields):
    class DynamicForm(forms.Form):
        pass

    for field_name, field in fields.items():
        DynamicForm.base_fields[field_name] = field

    return DynamicForm

def user_profile_form(request):
    if request.method == 'POST':
        # Define static fields
        static_fields = {
            'user_name': forms.CharField(),
            'user_email': forms.EmailField(),
            'user_region': forms.CharField(),
            'user_country_code': forms.CharField(),
            'user_country': forms.CharField(),
            'user_cadre': forms.CharField(),
            'access_permission': forms.CharField(),
            'added_by': forms.CharField(),
        }

        # Process dynamic fields
        dynamic_fields = {}
        dynamic_data = {}

        temp_dict = dict(request.POST.items())
        start_key = 'added_by'
        if start_key in temp_dict:
            start_index = list(temp_dict.keys()).index(start_key)
            result_dict = {key: temp_dict[key] for key in list(temp_dict.keys())[start_index + 1:]}
        else:
            result_dict = {}

        for key, value in request.POST.items():
            if key.startswith('dynamic_field_value_'):
                index = key.split('_')[-1]  # Extract index from key
                field_name = request.POST.get(f'dynamic_field_name_{index}')  # Get the field name corresponding to the index

                if field_name:
                    dynamic_fields[field_name] = forms.CharField()  # Create form field for each dynamic field
                    dynamic_data[field_name] = value  # Save the value associated with the field name

        fields = {**static_fields, **dynamic_fields}
        DynamicForm = create_dynamic_form(fields)
        form = DynamicForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_profile_data = {field: data[field] for field in static_fields.keys()}

            # Save user profile
            user_profile = UserProfile(**user_profile_data)
            user_profile.save()

            # Save dynamic data
            dynamic_data_instance = DynamicData(user_profile=user_profile, data=json.dumps(result_dict))
            dynamic_data_instance.save()

            return redirect('success_url')  # Replace 'success_url' with the name of the URL you want to redirect to

    else:
        # Define static fields for GET request
        static_fields = {
            'user_name': forms.CharField(),
            'user_email': forms.EmailField(),
            'user_region': forms.CharField(),
            'user_country_code': forms.CharField(),
            'user_country': forms.CharField(),
            'user_cadre': forms.CharField(),
            'access_permission': forms.CharField(),
            'added_by': forms.CharField(),
        }
        DynamicForm = create_dynamic_form(static_fields)
        form = DynamicForm()

    return render(request, 'user_profile_form.html', {'form': form})


def user_profile_not_found(request):
    return render(request, 'user_profile_not_found.html')

def delete_user(request):
    if request.method == 'POST':
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['user_email']
            try:
                user_profile = UserProfile.objects.get(user_email=email)
                DynamicData.objects.filter(user_profile=user_profile).delete()
                user_profile.delete()
                messages.success(request, "User deleted successfully!")  
                return redirect('delete_user')
            except UserProfile.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('user_profile_not_found')
        else:
            messages.error(request, "Invalid form data.")
            return redirect('delete_user')
    else:
        form = DeleteUserForm()

    return render(request, 'delete_user.html', {'form': form})


class DeleteUserForm(forms.Form):
    user_email = forms.EmailField()

class SearchUserForm(forms.Form):
    user_email = forms.EmailField()

def create_dynamic_form(fields):
    class DynamicForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field_instance in fields.items():
                self.fields[field_name] = field_instance
    return DynamicForm


def user_profile_not_found(request):
    return render(request, 'user_profile_not_found.html')

def delete_user(request):
    if request.method == 'POST':
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['user_email']
            try:
                user_profile = UserProfile.objects.get(user_email=email)
                DynamicData.objects.filter(user_profile=user_profile).delete()
                user_profile.delete()
                messages.success(request, "User deleted successfully!")  
                return redirect('delete_user')
            except UserProfile.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('user_profile_not_found')
        else:
            messages.error(request, "Invalid form data.")
            return redirect('delete_user')
    else:
        form = DeleteUserForm()

    return render(request, 'delete_user.html', {'form': form})

def user_details(request):
    dynamic_data = {}
    user_profile = None
    form = SearchUserForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['user_email']
            user_profile = get_object_or_404(UserProfile, user_email=email)
            dynamic_instance = DynamicData.objects.filter(user_profile_id=user_profile.id).first()

            if dynamic_instance:
                if 'delete_columns' in request.POST:
                    columns_to_delete = request.POST.getlist('columns')
                    data = dynamic_instance.data

                    try:
                        dynamic_data = json.loads(data)
                    except json.JSONDecodeError:
                        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

                    for column in columns_to_delete:
                        if column in dynamic_data:
                            del dynamic_data[column]

                    dynamic_instance.data = json.dumps(dynamic_data)
                    dynamic_instance.save()

                    return JsonResponse({'status': 'success', 'message': 'Selected columns deleted successfully.'})
                else:
                    try:
                        dynamic_data = json.loads(dynamic_instance.data)
                    except json.JSONDecodeError:
                        dynamic_data = {"error": "Invalid JSON data"}

    return render(request, 'user_details.html', {
        'form': form,
        'user_profile': user_profile,
        'dynamic_data': dynamic_data
    })





# Function to dynamically create a form class
def create_dynamic_form(fields):
    class DynamicForm(forms.Form):
        pass
    
    for field_name, field in fields.items():
        DynamicForm.base_fields[field_name] = field
    
    return DynamicForm

def user_profile_form(request):
    if request.method == 'POST':
        # Define static fields
        static_fields = {
            'user_name': forms.CharField(required=True),
            'user_email': forms.EmailField(required=True),
            'user_region': forms.CharField(required=True),
            'user_country_code': forms.CharField(required=True),
            'user_country': forms.CharField(required=True),
            'user_cadre': forms.CharField(required=True),
            'access_permission': forms.CharField(required=True),
            'added_by': forms.CharField(required=True),
        }
        
        # Extract dynamic fields from POST data
        dynamic_fields = {}
        dynamic_data = {}
        result_dict = {}
        temp_dict = dict(request.POST.items())
        start_key = 'added_by'
        if start_key in temp_dict:
            start_index = list(temp_dict.keys()).index(start_key)
            result_dict = {key: temp_dict[key] for key in list(temp_dict.keys())[start_index+1:]}
        else:
            result_dict = {}
        new_dict={}
        # Iterate through the dictionary
        for key, value in result_dict.items():
            col_name = key.split('_')[2]
            print(col_name)
            if col_name!="name":
                print("key",key)
                # Extract the index from the key
                index = key.split('_')[-1]
                name_key = f'dynamic_field_name_{index}'
                if name_key in result_dict:
                    field_value = value
                    field_name = result_dict[name_key]
                    if field_value not in new_dict:
                        new_dict[field_value] = field_name
        print(new_dict)

        temp_dict = dict(request.POST.items())
        start_key = 'added_by'
        if start_key in temp_dict:
            start_index = list(temp_dict.keys()).index(start_key)
            result_dict = {key: temp_dict[key] for key in list(temp_dict.keys())[start_index + 1:]}

        # Process dynamic fields
        for key, value in result_dict.items():
            if key.startswith('dynamic_field_value_'):
                index = key.split('_')[-1]
                field_name = request.POST.get(f'dynamic_field_name_{index}')
                if field_name:
                    dynamic_fields[field_name] = forms.CharField(required=True)
                    dynamic_data[field_name] = value
        
        # Combine static and dynamic fields
        fields = {**static_fields, **dynamic_fields}
        DynamicForm = create_dynamic_form(fields)
        form = DynamicForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            user_profile_data = {field: data[field] for field in static_fields.keys()}
            user_profile = UserProfile(**user_profile_data)
            user_profile.save()

            # Save dynamic field data
            dynamic_data_instance = DynamicData(user_profile=user_profile, data=json.dumps(new_dict))
            dynamic_data_instance.save()

            return redirect('user_profile_form')
    else:
        static_fields = {
            'user_name': forms.CharField(required=True),
            'user_email': forms.EmailField(required=True),
            'user_region': forms.CharField(required=True),
            'user_country_code': forms.CharField(required=True),
            'user_country': forms.CharField(required=True),
            'user_cadre': forms.CharField(required=True),
            'access_permission': forms.CharField(required=True),
            'added_by': forms.CharField(required=True),
        }
        DynamicForm = create_dynamic_form(static_fields)
        form = DynamicForm()
    
    return render(request, 'user_profile_form.html', {'form': form})


def sample(request):
    print(request.POST)
    return render(request,'drop.html')