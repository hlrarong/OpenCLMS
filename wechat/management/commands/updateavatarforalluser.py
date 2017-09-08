# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from user.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        counter = 0
        users = User.objects.exclude(openid=None).all()
        for u in users:
            try:
                u.updateavatarfromwechat()
            except:
                pass
            counter += 1
        self.stdout.write("update %d users" % counter)
