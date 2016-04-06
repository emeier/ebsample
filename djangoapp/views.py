from django.http import HttpResponse


def index(request):
    return HttpResponse('Hi there. I am a Django app')


def healthcheck(request):
    return HttpResponse('OK!')
