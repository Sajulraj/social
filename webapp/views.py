from django.shortcuts import redirect, render
from api.models import *
from .forms import *
from django.views.generic import CreateView, FormView, ListView,TemplateView,UpdateView
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
class IndexView( ListView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followings"] = Friends.objects.filter(follower=self.request.user)
        return context

@method_decorator(decs,name="dispatch")
class PostFormView(CreateView):
    template_name="add-post.html"
    form_class=PostForm
    success_url=reverse_lazy("home")
    model=Posts

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)



@method_decorator(decs,name="dispatch")
class UserIndexView(CreateView, ListView):
    template_name = "userindex.html"
    form_class = PostForm
    success_url = reverse_lazy("userindex")
    queryset = Posts.objects.all()
    context_object_name = 'posts'
    model=Posts

    
            

    def get_queryset(self):
        return Posts.objects.filter(user=self.request.user).order_by("-created_date")

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


@method_decorator(decs,name="dispatch")
class AddProfileView(CreateView):
    template_name="userprofile.html"
    form_class=ProfileForm
    success_url=reverse_lazy("home")

    def post(self,request,*args,**kw):
        form=ProfileForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect("home")
        else:
            return render(request,"userprofile.html",{"form":form})

@method_decorator(decs,name="dispatch")
class ViewmyProfile(TemplateView):
    template_name="userindex.html"
    
@method_decorator(decs,name="dispatch")
class EditProfileView(UpdateView):
    template_name="profile.html"
    form_class=ProfileForm
    model=UserProfile
    pk_url_kwargs="id"
    success_url=reverse_lazy("userindex")


@method_decorator(decs,name="dispatch")
class ListPeopleView(ListView):
    template_name="people/peoples.html"
    model = User
    context_object_name = 'people'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followings"] = Friends.objects.filter(follower=self.request.user)
        context["posts"] = Posts.objects.all().order_by('-created_date')
        return context
    

    def get_queryset(self):
        return User.objects.exclude(username=self.request.user)

decs
def add_follower(request, *args, **kwargs):
    id = kwargs.get('id')
    usr = User.objects.get(id=id)
    if not Friends.objects.filter(user=usr, follower=request.user):
        Friends.objects.create(user=usr, follower=request.user)
    else:
        Friends.objects.get(user=usr, follower=request.user).delete()
    return redirect("people")


decs
def comment_delete(request,*args,**kw):
    id=kw.get("id")
    Comments.objects.get(id=id).delete()
    return redirect("home")

decs
def post_delete(request,*args,**kw):
    id=kw.get("id")
    Posts.objects.get(id=id).delete()
    return redirect("home")


def sign_out_view(request,*args,**kw):
    logout(request)
    return redirect("sign-in")