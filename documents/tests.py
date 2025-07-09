import tempfile
from django.urls import reverse
from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from unittest import mock

from .models import Document, Comment


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class SearchViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

        patcher_img = mock.patch('documents.models.Document.generate_image_thumbnail', lambda self: None)
        patcher_vid = mock.patch('documents.models.Document.generate_video_thumbnail', lambda self: None)
        self.addCleanup(patcher_img.stop)
        self.addCleanup(patcher_vid.stop)
        patcher_img.start()
        patcher_vid.start()

        self.img = Document.objects.create(
            title='photo',
            file=SimpleUploadedFile('test.jpg', b'1')
        )
        self.vid = Document.objects.create(
            title='video',
            file=SimpleUploadedFile('video.mp4', b'1')
        )
        self.doc = Document.objects.create(
            title='doc',
            file=SimpleUploadedFile('notes.txt', b'1')
        )

        old_date = timezone.now() - timezone.timedelta(days=2)
        Document.objects.filter(pk=self.doc.pk).update(uploaded_at=old_date)
        self.doc.refresh_from_db()

    def test_search_by_type_image(self):
        response = self.client.get(reverse('search'), {'type': 'image'})
        self.assertContains(response, 'photo')
        self.assertNotContains(response, 'video')

    def test_search_by_date(self):
        today = timezone.now().date().isoformat()
        response = self.client.get(reverse('search'), {'start_date': today})
        self.assertContains(response, 'photo')
        self.assertContains(response, 'video')
        self.assertNotContains(response, 'doc')


class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

        patcher_img = mock.patch('documents.models.Document.generate_image_thumbnail', lambda self: None)
        patcher_vid = mock.patch('documents.models.Document.generate_video_thumbnail', lambda self: None)
        self.addCleanup(patcher_img.stop)
        self.addCleanup(patcher_vid.stop)
        patcher_img.start()
        patcher_vid.start()

        self.doc = Document.objects.create(
            title='doc',
            file=SimpleUploadedFile('notes.txt', b'1')
        )

    def test_add_comment(self):
        url = reverse('document_detail', args=[self.doc.id])
        response = self.client.post(url, {'text': 'Nice file'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(document=self.doc, text='Nice file').exists())
