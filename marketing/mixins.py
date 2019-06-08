from django.views.decorators.csrf import csrf_exempt

class CsrfExemptMixin(object):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(request, *args, **kwargs)