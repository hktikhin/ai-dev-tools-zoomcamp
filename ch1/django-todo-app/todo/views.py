# todo/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
# Optional: we'll add login later — remove LoginRequiredMixin if you don't want auth yet

from .models import Todo


class TodoListView(ListView):
    model = Todo
    template_name = 'todo/todo_list.html'
    context_object_name = 'todos'
    ordering = ['-created_at']


class TodoCreateView(CreateView):
    model = Todo
    template_name = 'todo/todo_form.html'
    fields = ['title', 'description', 'due_date']
    success_url = reverse_lazy('todo:list')

    def form_valid(self, form):
        # Auto-set status to pending on create
        form.instance.status = 'pending'
        return super().form_valid(form)


class TodoUpdateView(UpdateView):
    model = Todo
    template_name = 'todo/todo_form.html'
    fields = ['title', 'description', 'due_date', 'status']
    success_url = reverse_lazy('todo:list')


class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'todo/todo_confirm_delete.html'
    success_url = reverse_lazy('todo:list')


# Quick "Mark as Done" action — one-click from the list
def mark_as_done(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.status = 'done'
    todo.save()
    return redirect('todo:list')


def mark_as_pending(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.status = 'pending'
    todo.save()
    return redirect('todo:list')