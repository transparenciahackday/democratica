try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
try:
    import Image
except ImportError:
    from PIL import Image
import os
from urllib2 import urlparse

from django.conf import settings
from django.core.files import storage
from django.core.files.base import ContentFile

from djutils.test import TestCase
from djutils.utils.images import resize
from djutils.utils.strings import split_words_at


class DummyMemoryStorage(storage.Storage):
    """
    A simple in-memory storage backend for testing image storage
    """
    _files = {} # bampf
    
    def delete(self, name):
        if name in self._files:
            del(self._files[name])
    
    def exists(self, name):
        return name in self._files
    
    def listdir(self, path):
        files = []
        if not path.endswith('/'):
            path += '/' # make sure ends in slash for string comp below
        for k in self._files:
            if k.startswith(path) and '/' not in k.replace(path, ''):
                files.append(k.replace(path, ''))
    
    def size(self, name):
        return len(self._files[name])
    
    def url(self, name):
        return urlparse.urljoin(settings.MEDIA_URL, name)
    
    def _open(self, name, mode):
        return StringIO(self._files.get(name, ''))
    
    def _save(self, name, content):
        content.seek(0)
        self._files[name] = content.read()
        return name
    
    def get_valid_name(self, name):
        return name
    
    def get_available_name(self, name):
        if name not in self._files:
            return name
        
        base_path, ext = os.path.splitext(name)
        counter = 1
        
        while 1:
            test = '%s_%s%s' % (base_path, counter, ext)
            if test not in self._files:
                return test
            counter += 1


class StringUtilsTestCase(TestCase):
    def test_split_words_at(self):
        s = 'aa bb cc dd'

        self.assertEqual(split_words_at(s, 1), 'aa')
        self.assertEqual(split_words_at(s, 1, False), 'a')
        self.assertEqual(split_words_at(s, 2), 'aa')
        self.assertEqual(split_words_at(s, 2, False), 'aa')
        self.assertEqual(split_words_at(s, 3), 'aa bb')
        self.assertEqual(split_words_at(s, 3, False), 'aa')

        self.assertEqual(split_words_at(s, 100), 'aa bb cc dd')
        self.assertEqual(split_words_at(s, 100, False), 'aa bb cc dd')


class ImageUtilsTestCase(TestCase):
    def setUp(self):
        self.storage = DummyMemoryStorage()
        
        # monkeypatch default_storage
        self.orig_default_storage = storage.default_storage
        storage.default_storage = self.storage
        
        # swap settings
        self.orig_storage = settings.DEFAULT_FILE_STORAGE
        settings.DEFAULT_FILE_STORAGE = 'djutils.tests.utils.DummyMemoryStorage'
        
        test_image = Image.new('CMYK', (800, 600), (255, 255, 255, 255))
        self.img_buffer = StringIO()
        test_image.save(self.img_buffer, 'JPEG')
        
        self.img_file = ContentFile(self.img_buffer.getvalue())
        self.img_location = 'images/test_image.jpg'
        storage.default_storage.save(self.img_location, self.img_file)
    
    def tearDown(self):
        storage.default_storage = self.orig_default_storage
        settings.DEFAULT_FILE_STORAGE = self.orig_storage
    
    def test_resize(self):
        name, width, height = resize(self.img_location, 'images/test_image_small.jpg', 400)
        self.assertEqual(name, 'images/test_image_small.jpg')
        self.assertEqual(width, 400)
        self.assertEqual(height, 300)
        
        # preserves aspect ratio and creates new files as needed, returning correct name
        name, width, height = resize(self.img_location, 'images/test_image_small.jpg', 200, 200)
        self.assertEqual(name, 'images/test_image_small_1.jpg')
        self.assertEqual(width, 200)
        self.assertEqual(height, 150)
        
        # just double check to be sure it got saved here
        self.assertTrue('images/test_image_small_1.jpg' in self.storage._files)
        img_buf = StringIO(self.storage._files['images/test_image_small_1.jpg'])
        img = Image.open(img_buf)
        self.assertEqual((200, 150), img.size)
    
    def test_resize_to_same(self):
        # a special case that ensures resizing an image to the same destination
        # does not result in multiple files being created
        name, width, height = resize(self.img_location, self.img_location, 400)
        
        # check that it was resized and saved here
        img_buf = StringIO(self.storage._files[self.img_location])
        img = Image.open(img_buf)
        self.assertEqual((400, 300), img.size)
