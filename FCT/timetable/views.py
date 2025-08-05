# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Topic
import json
import datetime
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# Helper function to check if a topic is due for review today
def is_due_today(learned_date):
    """
    Checks if a topic is due for review based on a spaced repetition schedule.
    The schedule is:
    - Day 0 (the day it was learned)
    - Day 1
    - Day 3
    - Day 7
    - Day 30
    """
    today = datetime.date.today()
    delta = today - learned_date
    
    # Calculate review days based on the forgetting curve model
    # Note: Day 0 is the day the topic was learned.
    review_days = [0, 1, 3, 7, 30]
    
    # Check if any review date matches today
    if delta.days in review_days:
        return True
    return False

def index(request):
    """
    Renders the main page. This is a regular HTML page load.
    The page will then use JavaScript to fetch the topics.
    """
    # The CSRF token is automatically added to the context by Django
    # when using render, as long as the template has {% csrf_token %}
    return render(request, 'index.html')

@csrf_exempt
@require_http_methods(["GET"])
def get_topics(request):
    """
    API endpoint to retrieve all topics. Returns a JSON response
    with an added 'is_due_today' flag for each topic.
    """
    topics = Topic.objects.all().order_by('-learned_date')
    topics_list = []
    for topic in topics:
        topic_dict = model_to_dict(topic)
        topic_dict['learned_date'] = topic.learned_date.strftime('%Y-%m-%d')
        topic_dict['is_due_today'] = is_due_today(topic.learned_date)
        topics_list.append(topic_dict)
    
    return JsonResponse({'topics': topics_list})

@csrf_exempt
@require_http_methods(["POST"])
def add_topic(request):
    """
    API endpoint to add a new topic.
    Expects a POST request with a 'name' field in the body.
    """
    try:
        data = json.loads(request.body)
        topic_name = data.get('name')
        if not topic_name:
            return JsonResponse({'status': 'error', 'message': 'Topic name is required'}, status=400)
        
        new_topic = Topic.objects.create(name=topic_name)
        new_topic_dict = model_to_dict(new_topic)
        new_topic_dict['learned_date'] = new_topic.learned_date.strftime('%Y-%m-%d')
        new_topic_dict['is_due_today'] = is_due_today(new_topic.learned_date)
        
        return JsonResponse({
            'status': 'success',
            'topic': new_topic_dict
        })
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def delete_topic(request, topic_id):
    """
    API endpoint to delete a topic by ID.
    Expects a POST request.
    """
    try:
        topic_to_delete = Topic.objects.get(pk=topic_id)
        topic_to_delete.delete()
        return JsonResponse({'status': 'success'})
    except Topic.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Topic not found'}, status=404)