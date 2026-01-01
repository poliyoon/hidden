
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'core/index.html')

@login_required
def profile(request):
    # Pass user data to template
    return render(request, 'core/profile.html')

@login_required
def profiling(request):
    return render(request, 'core/profiling.html')

@login_required
def black_book(request):
    return render(request, 'core/black_book.html')
