from django.test import TestCase
from .models import Carousel


class CarouselModelTests(TestCase):
    def test_carousel_model(self):
        model_instance = Carousel.objects.create(
            field1="value1",
            field2="value2",
        )
        self.assertEqual(str(model_instance), "value1")


