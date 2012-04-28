import datetime

from djutils import constants
from djutils.test import TestCase
from djutils.tests.models import (
    Simple, Complex, UnderscoresNumerals, StatusModel
)


class SmartSlugFieldTestCase(TestCase):
    def test_simple(self):
        s1 = Simple(slug='simple')
        s1.save()
        self.assertEqual(s1.slug, 'simpl')

        s2 = Simple(slug='simple')
        s2.save()
        self.assertEqual(s2.slug, 'simp_')

        s3 = Simple(slug='simple')
        s3.save()
        self.assertEqual(s3.slug, 'sim__')

    def test_date_handling(self):
        dt = datetime.datetime(2010, 1, 1, 1, 1, 1)
        c1 = Complex(
            title='complex example',
            pub_date=dt)
        c1.save()

        self.assertEqual(c1.slug, 'complex')

        dt = datetime.datetime(2010, 1, 2, 1, 1, 1)
        c2 = Complex(
            title='complex example',
            pub_date=dt)
        c2.save()

        self.assertEqual(c2.slug, 'complex')

        c3 = Complex(
            title='complex example',
            pub_date=dt)
        c3.save()
        
        self.assertEqual(c3.slug, 'complex_')

    def test_split_words_generation(self):
        dt = datetime.datetime(2010, 1, 1, 1, 1, 1)
        c1 = Complex(title='complex example', pub_date=dt)
        c1.save()
        self.assertEqual(c1.slug, 'complex')

        c2 = Complex(title='complex example', pub_date=dt)
        c2.save()
        self.assertEqual(c2.slug, 'complex_')

        c3 = Complex(title='complex example', pub_date=dt)
        c3.save()
        self.assertEqual(c3.slug, 'complex__')
        
        c4 = Complex(title='complex example', pub_date=dt)
        c4.save()
        self.assertEqual(c4.slug, 'complex___')
        
        c5 = Complex(title='complex example', pub_date=dt)
        c5.save()
        self.assertEqual(c5.slug, 'comple____')

    def test_complex_splitting(self):
        dt = datetime.datetime(2010, 1, 1, 1, 1, 1)
        c1 = Complex(title='complex example test', pub_date=dt)
        c1.save()

        self.assertEqual(c1.slug, 'complex')

        c1.title = "complex as hell"
        c1.save()
        self.assertEqual(c1.slug, 'complex-as')

        c2 = Complex(title='complex as hell', pub_date=dt)
        c2.save()
        self.assertEqual(c2.slug, 'complex-a_')

        c3 = Complex(title='complex as hell', pub_date=dt)
        c3.save()
        self.assertEqual(c3.slug, 'complex-__')

    def test_numeral_handling(self):
        un1 = UnderscoresNumerals(slug_underscores='test', slug_numerals='test')
        un1.save()

        self.assertEqual(un1.slug_underscores, 'test')
        self.assertEqual(un1.slug_numerals, 'test')

        un2 = UnderscoresNumerals(slug_underscores='test', slug_numerals='test')
        un2.save()

        self.assertEqual(un2.slug_underscores, 'test_')
        self.assertEqual(un2.slug_numerals, 'test-1')

        un3 = UnderscoresNumerals(slug_underscores='test', slug_numerals='test')
        un3.save()

        self.assertEqual(un3.slug_underscores, 'test__')
        self.assertEqual(un3.slug_numerals, 'test-2')

    def test_numeral_overflow(self):
        un_long = UnderscoresNumerals(slug_underscores='long-example', slug_numerals='long-example')
        un_long.save()
        self.assertEqual(un_long.slug_underscores, 'long-examp')
        self.assertEqual(un_long.slug_numerals, 'long-examp')

        un_long2 = UnderscoresNumerals(slug_underscores='long-example', slug_numerals='long-example')
        un_long2.save()
        self.assertEqual(un_long2.slug_underscores, 'long-exam_')
        self.assertEqual(un_long2.slug_numerals, 'long-exa-1')

        un_long3 = UnderscoresNumerals(slug_underscores='long-example', slug_numerals='long-example')
        un_long3.save()
        self.assertEqual(un_long3.slug_underscores, 'long-exa__')
        self.assertEqual(un_long3.slug_numerals, 'long-exa-2')


class StatusFieldTestCase(TestCase):
    def test_defaults(self):
        instance = StatusModel()
        self.assertEqual(instance.status, constants.LIVE_STATUS)
        instance.save()
        
        saved = StatusModel.objects.get(pk=instance.pk)
        self.assertEqual(saved.status, constants.LIVE_STATUS)


class PublishedManagerTestCase(TestCase):
    def test_published_mgr(self):
        live_obj = StatusModel.objects.create(status=constants.LIVE_STATUS)
        draft_obj = StatusModel.objects.create(status=constants.DRAFT_STATUS)
        deleted_obj = StatusModel.objects.create(status=constants.DELETED_STATUS)
        
        self.assertQuerysetEqual(StatusModel.objects.published(), [live_obj])
