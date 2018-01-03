from ..models import Brownbag
import datetime


class BrownbagUtility(object):
    """Class handling brownbag utilities"""

    def sanitize_db(self):
        """Sanitizes database by marking a brownbag as done if its date is a past
        date from the day this function is run"""
        brownbags = Brownbag.objects.filter(status="next_in_line")
        for brownbag in brownbags:
            if brownbag.date < datetime.date.today():
                brownbag.status = "done"
                brownbag.save()
