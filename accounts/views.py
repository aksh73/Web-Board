from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
# from django.urls import reverse_lazy
# from django.views import generic
# # we use reverse_lazy to redirect the user to the login page upon successful signup and we are using it instead of reverse because generic class based views the urls are not loaded when the file is imported so we use the lazy form to reverse to load them later when they re availabe.
# #
# class SignUp(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/signup.html'
# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)   # we can import login instead of login and when the form is valid, form.save() will create an instance of the User class(containing  the username and password )from the database, so when user object is passed to the auth_login() it automatically does the login for the first time and then we redirect the page to home.
            return redirect('home')     # in login also the username and password will be verified only in order to grant access.
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html',{'form':form})


def changed_done(request):
    return render(request,'registration/changed_done.html')

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
