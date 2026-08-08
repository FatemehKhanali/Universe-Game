from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import authenticate, login as django_login, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache  # ✅ این درستشه
from django.core.mail import send_mail

from .forms import LoginForm, RegisterForm, ProfileForm
from .models import city, User, Profile


from django.http import JsonResponse

def edit_profile(request):
    user_profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                messages.success(request, 'Profile updated successfully')
                return redirect('accounts:edit_profile')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'The form is invalid'}, status=400)
    else:
        form = ProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'form': form})

from django.http import JsonResponse
from .models import city

def load_cities(request):
    province_id = request.GET.get('province_id')
    cities = city.objects.filter(province_id=province_id).values('id', 'title')
    return JsonResponse(list(cities), safe=False)


def get_cities(request):
    province_id = request.GET.get('province_id')
    if not province_id:
        return JsonResponse({'error':'Province ID is required'}, status=400)
    cities = city.objects.filter(province_id=province_id).values('id', 'title')
    return JsonResponse(list(cities), safe=False)

def login_view(request):
    next_page = request.GET.get('next')

    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            django_login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials or inactive account.')

    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, 'register.html', {'form': form})

        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'This email is already registered.')
            return render(request, 'register.html', {'form': form})

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        token = default_token_generator.make_token(user)
        encoded_user_id = urlsafe_base64_encode(force_bytes(user.id))
        activation_path = reverse('accounts:active_email', args=[encoded_user_id, token])
        activation_url = f"http://{current_site.domain}{activation_path}"

        send_activation_code(activation_url, user.email)

        messages.info(request, 'An activation email has been sent to your email address.')
        return redirect('accounts:login')

    form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def send_activation_code(activation_url, email_address):
    send_mail(
        subject='Activate your Gamer Zone account',
        message=f'Please click the link below to activate your account:\n\n{activation_url}',
        from_email='admin@admin.com',
        recipient_list=[email_address],
        fail_silently=False,
    )

def active_email(request, encoded_user_id, token):
    try:
        user_id = force_str(urlsafe_base64_decode(encoded_user_id))
        user = User.objects.get(id=user_id, is_active=False)
    except (User.DoesNotExist, ValueError, TypeError):
        return HttpResponse('<h1>Error: Invalid activation link.</h1>')

    if not default_token_generator.check_token(user, token):
        return HttpResponse('<h1>Error: Invalid or expired token.</h1>')

    user.is_active = True
    user.save()
    return render(request, 'accounts/activation_success.html')

def mobile_login(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        if mobile:
            send_otp(mobile)
            request.session['mobile'] = mobile
            return redirect(reverse('accounts:varify_otp'))
    return render(request, 'mobile_login.html')

def send_otp(mobile):
    import random
    otp = random.randint(100000, 999999)
    cache.set(mobile, otp, 300)
    print(f"OTP for {mobile}: {otp}")

def varify_otp(request):
    mobile = request.session.get('mobile')
    if not mobile:
        return redirect(reverse('accounts:mobile_login'))

    if request.method == "POST":
        otp = request.POST.get('otp')
        cached_otp = cache.get(mobile)

        if cached_otp and str(cached_otp) == otp:
            try:
                user = User.objects.get(mobile=mobile)

                if not user.is_active:
                    return render(request, 'varify_otp.html', {'error': 'User is not active'})

                login(request, user)
                print(f"✅ Logged in as: {request.user}")
                return redirect(reverse('index'))

            except User.DoesNotExist:
                return render(request, 'varify_otp.html', {'error': 'User not found'})
        else:
            return render(request, 'varify_otp.html', {'error': 'OTP is invalid'})

    return render(request, 'varify_otp.html')

