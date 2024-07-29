from django.shortcuts import render


def handler400(request, exception):
    """
    Renders the custom error 400 page.
    """
    return render(request, 'error_page/error_400.html', status=400)


def handler404(request, exception):
    """
    Renders the custom error 404 page.
    """
    return render(request, 'error_page/error_404.html', status=404)


def handler500(request):
    """
    Renders the custom error 500 page.
    """
    return render(request, 'error_page/error_500.html', status=500)
