from django.core.management.base import BaseCommand
from base.models import User 
from environs import Env 

env = Env()
env.read_env()

class Command(BaseCommand):
    help = "Create a superuser"

    def handle(self, *args, **options):
        if not User.objects.filter(email=env.str("SU_EMAIL")).exists():
            User.objects.create_superuser(
                username="that-dude-jude",
                email=env.str("SU_EMAIL"),
                password=env.str("SU_PASSWORD")                
            )

        print('Superuser has been created!')
