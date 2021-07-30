from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--user", required=True)
        parser.add_argument("--group", required=True)

    def handle(self, *args, **options):
        username = options["user"]
        group = options["group"]

        if not Group.objects.filter(name=group).count() >= 1:
            group = Group.objects.create(name=group)
            group.save() 

        if not User.objects.filter(username=username).count() >= 1:
            user = User.objects.create_user(username=username,
                                 email='email@email.com',
                                 password='password')
            user.save()
            user.groups.add(group) 



