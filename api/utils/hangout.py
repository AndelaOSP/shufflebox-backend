from ..models import Group


class HangoutUtility(object):
    """Class that handles all the transactions for the hangouts"""

    def get_groups(self):
        return Group.objects.all()

    def get_members(self, group):
        return group.members.all()

    def get_member_emails(self, group):
        emails = []
        for member in self.get_members(group):
            emails.append(member.email)
        return emails

