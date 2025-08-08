from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Topic
import datetime
from .views import get_review_intervals # Re-using your helper function
from django.contrib.auth.models import User

# ... the rest of your imports and code

@shared_task
def send_daily_review_reminders():
    """
    Finds users with topics due for review today and sends them an email.
    """
    today = timezone.now().date()
    
    # Get all users who have topics
    users_with_topics = Topic.objects.values_list('user', flat=True).distinct()

    for user_id in users_with_topics:
        user = User.objects.get(id=user_id)
        print(f"Processing user ID: {user.id}, Username: {user.username}, Email: {user.email}")
        user_intervals = get_review_intervals(user)
        
        # Find topics due for this user today
        due_topics = []
        for topic in Topic.objects.filter(user=user):
            learned_date = topic.learned_date
            delta = today - learned_date
            if delta.days in user_intervals:
                due_topics.append(topic.name)

        if due_topics:
            subject = f"Your Daily Review Reminder for {today.strftime('%Y-%m-%d')}"
            message = f"Hello {user.username},\n\n" \
                      f"You have the following topics to review today:\n\n" \
                      f"{' - '.join(due_topics)}\n\n" \
                      f"Keep up the great work!\n\n" \
                      f"Your Forgetting Curve Timetable"
            
            # You can also use an HTML template here for a nicer email
            # html_message = render_to_string('email/review_reminder.html', {'user': user, 'topics': due_topics})
            
            send_mail(
                subject,
                message,
                'your_email@gmail.com', # From email
                [user.email], # To email
                fail_silently=False,
            )