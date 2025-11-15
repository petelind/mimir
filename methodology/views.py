from django.shortcuts import render


def index(request):
    """
    Home page - methodology explorer placeholder.
    
    :param request: Django request object. Example: HttpRequest(method='GET')
    :return: Rendered HTML response. Example: HttpResponse(status=200, content="<div>...</div>")
    """
    return render(request, 'methodology/index.html')
