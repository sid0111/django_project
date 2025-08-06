from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Topic, UserSettings
import json
import datetime
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms

# Helper function to get intervals for a user
def get_review_intervals(user):
    try:
        settings = UserSettings.objects.get(user=user)
        intervals = [int(i.strip()) for i in settings.review_intervals.split(',')]
        return intervals
    except (UserSettings.DoesNotExist, ValueError):
        # Fallback to default if no settings exist or they are invalid
        return [0, 1, 3, 7, 30]

def is_due_today(learned_date, intervals):
    """
    Checks if a topic is due for review based on a spaced repetition schedule.
    """
    today = datetime.date.today()
    delta = today - learned_date
    
    return delta.days in intervals

@login_required(login_url='user_login')
def index(request):
    """
    Renders the main page. This is a regular HTML page load.
    The page will then use JavaScript to fetch the topics for the logged-in user.
    """
    return render(request, 'index.html')

@csrf_exempt
@require_http_methods(["GET"])
@login_required(login_url='user_login')
def get_topics(request):
    """
    API endpoint to retrieve all topics for the logged-in user.
    """
    user_intervals = get_review_intervals(request.user)
    topics = Topic.objects.filter(user=request.user).order_by('-learned_date')
    topics_list = []
    for topic in topics:
        topic_dict = model_to_dict(topic)
        topic_dict['id'] = str(topic.id)
        topic_dict['learned_date'] = topic.learned_date.strftime('%Y-%m-%d')
        topic_dict['is_due_today'] = is_due_today(topic.learned_date, user_intervals)
        topics_list.append(topic_dict)
    
    return JsonResponse({'topics': topics_list, 'review_intervals': user_intervals})


@csrf_exempt
@require_http_methods(["POST"])
@login_required(login_url='user_login')
def add_topic(request):
    """
    API endpoint to add a new topic for the logged-in user.
    """
    try:
        data = json.loads(request.body)
        topic_name = data.get('name')
        if not topic_name:
            return JsonResponse({'status': 'error', 'message': 'Topic name is required'}, status=400)
        
        new_topic = Topic.objects.create(name=topic_name, user=request.user)
        new_topic_dict = model_to_dict(new_topic)
        new_topic_dict['id'] = str(new_topic.id)
        new_topic_dict['learned_date'] = new_topic.learned_date.strftime('%Y-%m-%d')
        user_intervals = get_review_intervals(request.user)
        new_topic_dict['is_due_today'] = is_due_today(new_topic.learned_date, user_intervals)
        
        return JsonResponse({
            'status': 'success',
            'topic': new_topic_dict
        })
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
@login_required(login_url='user_login')
def delete_topic(request, topic_id):
    """
    API endpoint to delete a topic. Ensures the user can only delete their own topics.
    """
    try:
        topic_to_delete = Topic.objects.get(pk=topic_id, user=request.user)
        topic_to_delete.delete()
        return JsonResponse({'status': 'success'})
    except Topic.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Topic not found or you do not have permission to delete it'}, status=404)

# --- Authentication Views ---

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserSettings.objects.create(user=user)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
def profile_and_password_change(request):
    # This is a custom form to edit a user's name and email
    class UserProfileForm(UserChangeForm):
        class Meta:
            model = User
            fields = ['username', 'email']
            widgets = {
                'username': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 shadow-sm text-gray-700'}),
                'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 shadow-sm text-gray-700'}),
            }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Remove the password field from the form
            self.fields.pop('password')


    if request.method == 'POST':
        # Check which form was submitted using a hidden input or form name
        if 'profile_form_submit' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=request.user)
            password_form = PasswordChangeForm(request.user) # Keep the password form for rendering
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('profile_and_password_change')
            else:
                messages.error(request, 'Please correct the error in the profile form.')
        elif 'password_form_submit' in request.POST:
            profile_form = UserProfileForm(instance=request.user) # Keep the profile form for rendering
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile_and_password_change')
            else:
                messages.error(request, 'Please correct the error in the password form.')
        else:
            profile_form = UserProfileForm(instance=request.user)
            password_form = PasswordChangeForm(request.user)
            messages.error(request, 'Invalid form submission.')
    else:
        profile_form = UserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })

class UserSettingsForm(forms.ModelForm):
    review_intervals = forms.CharField(
        label="Review Intervals (comma-separated days)",
        help_text="e.g., 0,1,3,7,30",
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 shadow-sm text-gray-700'}),
        required=False
    )
    class Meta:
        model = UserSettings
        fields = ['review_intervals']
        
@login_required
def settings_view(request):
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings were successfully updated!')
            return redirect('settings')
    else:
        form = UserSettingsForm(instance=user_settings)
    return render(request, 'settings.html', {'form': form})