from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.views import View
from .models import *
from .forms import *
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods


def user_profile_form(request):
    if request.method == 'POST':
        
        # Define static fields with correct names
        static_fields = {
            'name': forms.CharField(),
            'email': forms.EmailField(),
            'id': forms.CharField(),  # This might not be necessary if using Django's primary key
            'position': forms.CharField(),
        }

        # Extract static data
        static_data = {field: request.POST.get(field) for field in static_fields}
        
        # Extract dynamic fields
        dynamic_fields = {}
        
        # Get all dynamic columns
        column_names = request.POST.getlist('dynamic_column_name_')
        column_types = request.POST.getlist('dynamic_column_type_')
        column_additional_values = request.POST.getlist('dynamic_column_additional_value_')
        
        # Iterate over each column index
        for index, column_name in enumerate(column_names):
            if column_name:  # Ensure column_name is not empty
                dynamic_fields[column_name] = {
                    'column_type': column_types[index] if index < len(column_types) else '',
                    'data': column_additional_values[index] if index < len(column_additional_values) else ''
                }

        
        # Create and validate form
        DynamicForm = create_dynamic_form(static_fields)
        form = DynamicForm(request.POST)


        user_profile = UserProfile(
            name=static_data['name'],
            email=static_data['email'],
            position=static_data['position'],

            )
        user_profile.save()

        dynamic_data_instance = DynamicData(user_profile=user_profile, data=dynamic_fields)
        dynamic_data_instance.save()
        
    return render(request, 'user_profile_form.html', {'form': "create_dynamic_form({})()"})

def user_profile_list(request):
    profiles = UserProfile.objects.all()
    
    return render(request, 'user_profile_list.html', {'profiles': profiles    })

def user_profile_delete(request, user_id):
    profile = get_object_or_404(UserProfile, id=user_id)
    profile.delete()
    return redirect('user_profile_list')


@require_http_methods(["POST"])
def delete_user_profile(request):
    user_id = request.POST.get('user_id')
    profile = get_object_or_404(UserProfile, pk=user_id)
    profile.delete()
    return redirect('user_profile_list')

# --------------------------------ok

#     if request.method == 'POST':
#         # Extract data from POST request
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         position = request.POST.get('position')
#         data = request.POST.get('data')
#         try:
#             # Preprocess JSON data to ensure correct format
#             data = data.replace("'", '"')
#             dynamic_data_dict = json.loads(data)
#         except json.JSONDecodeError as e:
#             return render(request, 'user_profile_manage.html', {
#                 'profile': profile,
#                 'dynamic_data': dynamic_data,
#                 'error': 'Invalid JSON data: {}'.format(e),
#             })

#         if user_id:
#             # Update existing profile and dynamic data
#             profile.name = name
#             profile.email = email
#             profile.position = position
#             profile.save()

#             dynamic_data.data = dynamic_data_dict
#             dynamic_data.save()
#         else:
#             # Create new profile
#             profile = UserProfile(name=name, email=email, position=position)
#             profile.save()
#             dynamic_data = DynamicData(user_profile=profile, data=dynamic_data_dict)
#             dynamic_data.save()

#         return redirect('user_profile_list')
    
#     print(dynamic_data_json)  # This will print the actual JSON data
#     return render(request, 'user_profile_manage.html', {
#         'profile': profile,
#         'dynamic_data_json': dynamic_data_json,
#     })

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
from .models import UserProfile, DynamicData

@require_http_methods(["GET", "POST"])
def user_profile_manage(request, user_id=None):
    if user_id:
        profile = get_object_or_404(UserProfile, pk=user_id)
        dynamic_data = get_object_or_404(DynamicData, user_profile=profile)
        dynamic_data_json = json.dumps(dynamic_data.data)
    else:
        profile = None
        dynamic_data_json = '{}'

    if request.method == 'POST':
        print(request.POST)

        # Extract data from POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        position = request.POST.get('position')
        data = request.POST.get('data')
        print("dynamic_data",data)


        
        try:
            # Preprocess JSON data to ensure correct format
            data = data.replace("'", '"')
            dynamic_data_dict = json.loads(data)
        except json.JSONDecodeError as e:
            return render(request, 'user_profile_manage.html', {
                'profile': profile,
                'dynamic_data_json': dynamic_data_json,
                'error': 'Invalid JSON data: {}'.format(e),
            })

        if user_id:
            # Update existing profile and dynamic data
            profile.name = name
            profile.email = email
            profile.position = position
            profile.save()

            dynamic_data.data = dynamic_data_dict
            dynamic_data.save()
        else:
            # Create new profile
            profile = UserProfile(name=name, email=email, position=position)
            profile.save()
            dynamic_data = DynamicData(user_profile=profile, data=dynamic_data_dict)
            dynamic_data.save()

        return redirect('user_profile_list')
    
    # Ensure dynamic_data_json is a JSON-encoded string
    return render(request, 'user_profile_manage.html', {
        'profile': profile,
        'dynamic_data_json': dynamic_data_json,
    })
