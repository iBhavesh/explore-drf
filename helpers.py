from time import strftime
import os
import mimetypes
import sys
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def upload_to(instance, filename):  # pylint:disable=unused-argument
    print(instance)
    filenames = os.path.splitext(filename)
    return "posts/" + strftime('%Y%m%d%H%M%S') + filenames[-1]


def compress_image(uploaded_image):
    mime_type = mimetypes.guess_type(uploaded_image.name)
    if mime_type[0] is not None:
        return uploaded_image
    elif not mime_type[0].startswith('image'):
        return uploaded_image
    elif uploaded_image.size is not None and uploaded_image.size / 1024 < 200:
        return uploaded_image
    image_temporary = Image.open(uploaded_image)
    output_io_stream = BytesIO()
    # imageTemproaryResized = imageTemproary.resize((1020, 573))
    image_temporary.save(output_io_stream, format='JPEG', quality=50)
    output_io_stream.seek(0)
    uploaded_image = InMemoryUploadedFile(
        output_io_stream, 'ImageField', "%s.jpg" % uploaded_image.name.split('.')[
            0], 'image/jpeg', sys.getsizeof(output_io_stream), None)
    return uploaded_image
