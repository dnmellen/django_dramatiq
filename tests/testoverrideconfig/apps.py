from django_dramatiq.apps import DjangoDramatiqConfig


class GroupsCallbacksDjangoDramatiqConfig(DjangoDramatiqConfig):

    def middleware_groupcallbacks_kwargs(self):
        return {"rate_limiter_backend": self.rate_limiter_backend}
