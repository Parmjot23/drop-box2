import re

from django.db import models
from django.core.files.base import ContentFile
from moviepy.editor import VideoFileClip
from PIL import Image
from io import BytesIO
import os


class Document(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.title:  # Only set the title if it's not already set
            self.title = os.path.basename(self.file.name)
        super(Document, self).save(*args, **kwargs)

        # Only generate thumbnails for image/video files
        if self.is_image() or self.is_video():
            if not self.thumbnail:
                if self.is_video():
                    self.generate_video_thumbnail()
                elif self.is_image():  # This checks if it's an image
                    self.generate_image_thumbnail()
                super(Document, self).save(*args, **kwargs) # Save again with the thumbnail

    def is_video(self):
        # Simple check based on file extension
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv']
        file_extension = os.path.splitext(self.file.name)[1].lower()
        return file_extension in video_extensions

    def is_image(self):
        # Simple check based on file extension to determine if the file is an image
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        file_extension = os.path.splitext(self.file.name)[1].lower()
        return file_extension in image_extensions

    def generate_video_thumbnail(self):
        clip = VideoFileClip(self.file.path)
        frame = clip.get_frame(4)  # Get a frame at 1 second

        frame_image = Image.fromarray(frame)
        frame_io = BytesIO()
        frame_image.save(frame_io, 'JPEG', quality=85)
        self.thumbnail.save(f'{os.path.splitext(self.file.name)[0]}_thumbnail.jpg',
                            ContentFile(frame_io.getvalue()), save=False)

    def generate_image_thumbnail(self):
        img = Image.open(self.file.path)

        # Correcting the orientation using EXIF data
        if hasattr(img, '_getexif') and img._getexif() is not None:
            exif_data = img._getexif()
            orientation_tag = 274  # EXIF Tag for orientation
            if orientation_tag in exif_data:
                orientation = exif_data[orientation_tag]
                rotate_values = {3: 180, 6: 270, 8: 90}
                if orientation in rotate_values:
                    img = img.rotate(rotate_values[orientation], expand=True)

        # Continue with thumbnail generation
        img.thumbnail((300, 300), Image.Resampling.LANCZOS)  # Example thumbnail size

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=95)
        self.thumbnail.save(f'{os.path.splitext(self.file.name)[0]}_thumbnail.jpg',
                            ContentFile(thumb_io.getvalue()), save=False)

    def is_photo(self):
        return bool(re.match(r'.*\.(jpg|jpeg|png|gif)$', self.file.name, re.I))

    def is_video(self):
        return bool(re.match(r'.*\.(mp4|mov|avi|mkv)$', self.file.name, re.I))