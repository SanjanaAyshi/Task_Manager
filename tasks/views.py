from django.shortcuts import render, redirect,get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives,EmailMessage
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_mail_to_user(user, subject, template, **kwargs):
    html_content = render_to_string(template, kwargs)
    text_content = strip_tags(html_content)

    # Send the email
    email = EmailMultiAlternatives(subject, text_content, to=[user.email])
    email.attach_alternative(html_content, "text/html")
    email.send()
    
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  
            task.save()
            messages.success(
                request, "You Task is added.")
            send_mail_to_user(request.user, "Successfully Added Task",
                          "addTaskEmail.html")
            return redirect('home')
    else:
        form = TaskForm()
    return render(request, 'addTask.html', {'form': form})

@login_required
def ProfileData(request):
    user = request.user
    incomplete_tasks = Task.objects.filter(user=user, is_complete=False)
    complete_tasks = Task.objects.filter(user=user, is_complete=True)
    
    return render(request, 'profile.html', {'incomplete_tasks': incomplete_tasks, 'complete_tasks': complete_tasks})


def cancel_task(request, task_id):
    # Retrieve the task object from the database
    task = get_object_or_404(Task, id=task_id)
    task.delete()  
    return redirect('profile')
