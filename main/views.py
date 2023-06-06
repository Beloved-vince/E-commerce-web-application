from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from .forms import SignUpForm


# Create your views here.
# @api_view(['GET'])
def signup(request):
    """
    Get user account data
    """
    if request.method == 'POST':
        try:
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse("success")
        except Exception as e:
            return HttpResponse(f"The error message is {e}")
    else:
        form = SignUpForm()
    return render(request, 'register.html')