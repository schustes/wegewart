from .UserEntity import UserEntity


class UserAggregate:
    def __init__(self, rootEntity: UserEntity):
        self.rootEntity =rootEntity
