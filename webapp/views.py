from django.shortcuts import redirect, render
from api.models import *
from .forms import *
from django.views.generic import CreateView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Create your views here.
def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"You must login first")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper

decs=[signin_required,never_cache]

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
                login(request,user)
                return redirect("home")
            else:
                messages.error(request, "Your credentials not matching, try again")
                return render(request, "login.html", {'form':form})

@method_decorator(decs,name="dispatch")
class IndexView(CreateView, ListView):
    template_name = "index.html"
    form_class = PostForm
    success_url = reverse_lazy("home")
    queryset = Posts.objects.all()
    context_object_name = 'posts'
    model=Posts


    def form_valid(self, form):
        if form.is_valid():
            form.instance.user=self.request.user
            messages.success(self.request, "New post has been uploaded")
            return super().form_valid(form)
        else:
            messages.error(self.request, "uploading failed")
            return render(self.request, "index.html", {"form":form})

    def get_queryset(self):
        return Posts.objects.exclude(user=self.request.user).order_by("-created_date")
decs   
def add_comment(request, *args, **kwargs):
        id = kwargs.get('id')
        cmt = request.POST.get('comment')
        qs = Posts.objects.get(id=id)
        qs.comments_set.create(user=request.user, comment=cmt)
        messages.success(request, "Comment added succesfully")
        return redirect("home")

decs
def like_post(request, *args, **kwargs):
        id = kwargs.get('id')
        ps = Posts.objects.get(id=id)
        if ps.like.contains(request.user):
            ps.like.remove(request.user)
        else:
            ps.like.add(request.user)
        return redirect("home")


def sign_out_view(request,*args,**kw):
    logout(request)
    return redirect("sign-in")