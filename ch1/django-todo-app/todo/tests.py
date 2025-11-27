# todo/tests/test_todo_app.py

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from todo.models import Todo


class TodoAppTestCase(TestCase):
    def setUp(self):
        """Create reusable test data"""
        self.todo1 = Todo.objects.create(
            title="Buy groceries",
            description="Milk, eggs, bread",
            due_date=timezone.now() + timedelta(days=1),
            status='pending'
        )
        self.todo2 = Todo.objects.create(
            title="Finish Django project",
            due_date=timezone.now(),
            status='done'
        )

    # 1. Test the list page
    def test_todo_list_page_loads_and_shows_todos(self):
        response = self.client.get(reverse('home'))  # or reverse('todo:list') if you prefer /todo/
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Buy groceries")
        self.assertContains(response, "Finish Django project")
        self.assertContains(response, "My Todos")

    # 2. Test creating a new todo
    def test_create_todo_successfully(self):
        response = self.client.post(reverse('todo:create'), {
            'title': 'Learn testing',
            'description': 'Write comprehensive tests',
            'due_date': '2025-12-31'
        })
        self.assertEqual(response.status_code, 302)  # redirect after success
        self.assertTrue(Todo.objects.filter(title="Learn testing").exists())
        new_todo = Todo.objects.get(title="Learn testing")
        self.assertEqual(new_todo.status, 'pending')

    def test_create_todo_requires_title(self):
        response = self.client.post(reverse('todo:create'), {
            'title': '',
            'description': 'This should fail'
        })
        self.assertEqual(response.status_code, 200)  # form re-rendered
        self.assertContains(response, "This field is required")
        self.assertFalse(Todo.objects.filter(description="This should fail").exists())

    # 3. Test editing a todo
    def test_edit_todo_changes_data(self):
        response = self.client.post(reverse('todo:update', kwargs={'pk': self.todo1.pk}), {
            'title': 'Buy MORE groceries',
            'status': 'done',
            'due_date': '2025-12-25'
        })
        self.assertEqual(response.status_code, 302)
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.title, "Buy MORE groceries")
        self.assertEqual(self.todo1.status, 'done')

    # 4. Test delete todo
    def test_delete_todo_removes_it(self):
        todo_count_before = Todo.objects.count()
        response = self.client.post(reverse('todo:delete', kwargs={'pk': self.todo1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), todo_count_before - 1)
        self.assertFalse(Todo.objects.filter(pk=self.todo1.pk).exists())

    # 5. Test "Mark as Done" one-click action
    def test_mark_as_done_changes_status(self):
        self.assertEqual(self.todo1.status, 'pending')
        response = self.client.get(reverse('todo:mark_done', kwargs={'pk': self.todo1.pk}))
        self.assertEqual(response.status_code, 302)
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.status, 'done')

    def test_mark_as_pending_works(self):
        self.todo2.status = 'done'
        self.todo2.save()
        response = self.client.get(reverse('todo:mark_pending', kwargs={'pk': self.todo2.pk}))
        self.assertEqual(response.status_code, 302)
        self.todo2.refresh_from_db()
        self.assertEqual(self.todo2.status, 'pending')

    # 6. Test template shows correct visual indicators
    def test_pending_todo_shows_clock_icon_and_warning_styles(self):
        self.todo1.status = 'pending'
        self.todo1.save()

        response = self.client.get(reverse('home'))
        html = response.content.decode()

        # The clock icon + warning color + warning border must appear near this todo
        title = self.todo1.title
        self.assertIn(title, html)
        self.assertIn('bi-clock', html)
        self.assertIn('text-warning', html)
        self.assertIn('border-warning', html)

    def test_done_todo_shows_check_icon_and_success_styles(self):
        self.todo2.status = 'done'
        self.todo2.save()

        response = self.client.get(reverse('home'))
        html = response.content.decode()

        title = self.todo2.title
        self.assertIn(title, html)
        self.assertIn('bi-check2-circle', html)
        self.assertIn('text-success', html)
        self.assertIn('border-success', html)

    def test_no_todos_shows_empty_state(self):
        Todo.objects.all().delete()
        response = self.client.get(reverse('home'))
        self.assertContains(response, "No todos yet!")
        self.assertContains(response, "Create your first todo")

    # 7. Test empty state message
    def test_empty_list_shows_no_todos_message(self):
        Todo.objects.all().delete()
        response = self.client.get(reverse('home'))
        self.assertContains(response, "No todos yet!")
        self.assertContains(response, "Create your first todo")