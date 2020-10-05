from django.shortcuts import render

def home_view(request):
    return render(request, "bibliotech/home.html")

# TODO: you can access this page from wherever, whenever
def success(request):
    """
    Catch all success page
    """
    return render(request, "bibliotech/success.html")
