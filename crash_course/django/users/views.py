from django.shortcuts import render
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

    if form.is_valid():
        new_user = form.save()
        authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
        login(request, authenticated_user)
        return HttpResponseRedirect(reverse('learning_logs:index'))
    
    context = {'form': form}
    return render(request, 'users/register.html', context)


# def login_view(request):
#     """Log the user in."""
#     if request.method != 'POST':
#         # Display blank login form
#         return render(request, 'users/login.html')
#     else:
#         # Process completed form
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         
#         if user is not None:
#             login(request, user)
#             return HttpResponseRedirect(reverse('learning_logs:index'))
#         else:
#             return render(request, 'users/login.html', {'error': True})
