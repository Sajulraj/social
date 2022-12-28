from django.shortcuts import redirect, render
from api.models import *
from .forms import *
from django.views.generic import CreateView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate

# Create your views here.

class UserReigtrationView(CreateView):
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('sign-in')

    def form_invalid(self, form):
        if form.is_valid():
            messages.success(self.request, 'Account has been created')
        else:
            messages.error(self.request, 'An error occured try again')
        return super().form_invalid(form)


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                return redirect("home")
            else:
                messages.error(request, "Your credentials not matching, try again")
                return render(request, "login.html", {'form':form})

class IndexView(CreateView, ListView):
    template_name = "index.html"
    form_class = PostForm
    success_url = reverse_lazy("home")
    queryset = Posts.objects.all()
    context_object_name = 'posts'
    model=Posts


    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"your post added successfully")
        return super().form_valid(form)







    # def get_queryset(self):

    #     return Posts.objects.exclude(user=self.request.user).order_by("-created_date")



def add_comment(request,*args,**kw):
    id=kw.get("id")
    pos=Posts.objects.get(id=id)
    com=request.POST.get("comment")
    Comments.objects.create(posts=pos,comments=com,user=request.user)
    return redirect("home")