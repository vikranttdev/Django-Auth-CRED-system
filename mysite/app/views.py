from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SetPasswordForm
from .forms import PasswordResetForm ,send_forget_password_mail


# Create your views here.
def home(request):
    return render(request, 'lms/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')

    else:
        form = SignupForm()

    context = {'form': form}
    return render(request, 'lms/signup.html', context)

@login_required
def cred(request):
    emp = Employees.objects.all()
    print(emp)
    context = {
        'emp': emp,
    }
    return render(request,'lms/cred.html',context)


def add(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        address=request.POST.get("address")
        phone = request.POST.get("phone")
        emp=Employees(name=name,email=email,address=address,phone=phone)
        emp.save()
        return redirect('cred')
    return render(request, 'cred.html')


def edit(request):
    emp=Employees.objects.all()
    context={
        'emp':emp,
    }
    return render(request,'cred.html',context)


def update(request,id):
    if request.method=="POST":
        id=id
        name=request.POST.get("name")
        email=request.POST.get("email")
        address=request.POST.get("address")
        phone = request.POST.get("phone")
        emp=Employees(id=id,name=name,email=email,address=address,phone=phone)
        emp.save()
        return redirect('cred')
    return render(request, 'cred.html')


def delete(request,id):
    emp=Employees.objects.filter(id=id)
    emp.delete()
    context={
        'emp':emp,
    }
    return redirect('cred')


@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'lms/change_password.html', {'form': form})


def password_reset_request(request):
    form = PasswordResetForm()
    return render(request=request,template_name="lms/password_reset.html",context={"form": form})


import uuid
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget-password/')

            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')



    except Exception as e:
        print(e)
    return render(request , 'lms/forget-password.html')


def ChangePassword(request, token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('login')

    except Exception as e:
        print(e)
    return render(request, 'lms/change-password.html', context)






















