from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from accounts.models import User, Profile
from blog.models import Post, Category

category_list = [
    "IT",
    "Design",
    "Fun"
]

class Command(BaseCommand):
    help = "inserting dummy data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create(email = self.fake.email(), password = "Test@12345678")
        profile = Profile.objects.get(user = user)

        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.bio = self.fake.paragraph(nb_sentences=5)
        profile.save()

        for name in category_list:
            Category.objects.get_or_create(name = name)
        
        for _ in range(10):
            Post.objects.create(
                author = profile,
                category = Category.objects.get(name = random.choice(category_list)),
                title = self.fake.paragraph(nb_sentences=1),
                content  = self.fake.paragraph(nb_sentences=10),
                status = random.choice([True, False]),
                published_date = timezone.now()
            )