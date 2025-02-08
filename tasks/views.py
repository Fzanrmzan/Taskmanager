from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


# 🌟 API Views for Task Management (Django REST Framework)
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require login

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

# 🌟 User Authentication Views
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

# 🌟 Dashboard View
@login_required
def dashboard(request):
    """Render the Task Manager Dashboard."""
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        Task.objects.create(user=request.user, title=title, description=description, status='todo')
        return redirect('dashboard')

    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/dashboard.html', {'tasks': tasks})

# 🌟 Update Task Status via Drag & Drop (AJAX)
@csrf_exempt
@login_required
def update_task_status(request, task_id):
    """Update task status via Drag & Drop."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_status = data.get("status")

            if new_status in ["todo", "in_progress", "done"]:
                task = Task.objects.get(id=task_id, user=request.user)
                task.status = new_status
                task.save()
                return JsonResponse({"message": "Task status updated successfully!"})
            else:
                return JsonResponse({"error": "Invalid status"}, status=400)

        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

# 🌟 Update Task Details
@login_required
def update_task(request, task_id):
    """Update task details."""
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        task.title = title
        task.description = description
        task.save()
        return redirect('dashboard')

    return render(request, 'tasks/edit_task.html', {'task': task})

# 🌟 Delete Task
@csrf_exempt
@login_required
def delete_task(request, task_id):
    if request.method == 'POST':
        try:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            task.delete()
            return JsonResponse({'message': 'Task deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)