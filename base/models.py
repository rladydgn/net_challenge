from django.db import models


class UserData(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    limit_speed = models.IntegerField()
    road_name = models.CharField(max_length=50)
    longitude = models.FloatField()
    latitude = models.FloatField()
    do_limit = models.IntegerField()