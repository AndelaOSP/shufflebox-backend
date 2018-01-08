from ..models import Brownbag
from ..models import User


class BrownbagUtility(object):
    """Class handling brownbag utilities"""

    def update_status(self, id, status):
        """Updates brownbag status"""
        brownbag = self.get_brownbag(id)
        brownbag.status = status
        brownbag.save()

    def get_next_in_line(self):
        return Brownbag.objects.filter(status="next_in_line")

    def get_done(self):
        return Brownbag.objects.filter(status="done")

    def get_not_done(self):
        return Brownbag.objects.filter(status="not_done")

    def get_user_email(self, id):
        return User.objects.get(brownbag=id).email

    def get_brownbag(self, id):
        return Brownbag.objects.get(id=id)
