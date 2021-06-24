from django.apps import AppConfig


class UserManageConfig(AppConfig):
    name = 'user_manage'

    def ready(self):
        print('at ready')
        import user_manage.signals
