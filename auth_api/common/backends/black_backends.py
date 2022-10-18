from common.enum.tenant import AccountStatusChoice


def BlackBackEnds(user):
    # return user.status == AccountStatusChoice.NORMAL
    return user.is_active