import os

from django.conf import settings


def delete_previous_image(self, commit, model, file_name):
    db_profile = model.objects.get(pk=self.instance.pk)
    new_image = self.files.get('image')
    old_image = str(db_profile.image)
    old_image_path = os.path.join(settings.MEDIA_ROOT, old_image)
    if commit and new_image and old_image and not old_image == file_name:
        os.remove(old_image_path)
