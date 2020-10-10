from django.shortcuts import render

# TODO: move into library modules
def home_view(request):
    return render(request, "library/home.html")

# TODO: you can access this page from wherever, whenever
# TODO: Move into library views
def success(request):
    """
    Catch all success page
    """
    return render(request, "library/success.html")
