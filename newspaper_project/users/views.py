from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.views import LogoutView, LoginView
from .forms import CustomUserCreationForm
from .models import EmailVerification

class CustomLogoutView(LogoutView):
	next_page = 'login'
	
	def dispatch(self, request, *args, **kwargs):
		messages.success(request, "您已成功登出。")
		return super().dispatch(request, *args, **kwargs)

class CustomLoginView(LoginView):
	def form_valid(self, form):
		user = form.get_user()
		if not user.is_active:
			messages.error(self.request, '請先驗證您的電子郵件地址。')
			return self.form_invalid(form)
		messages.success(self.request, f'歡迎回來，{user.username}！')
		return super().form_valid(form)
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            verification = EmailVerification.objects.create(user=user)
            verification.generate_token()
            
            verify_url = request.build_absolute_uri(
                reverse('verify_email', args=[verification.token])
            )
            
            try:
                html_message = render_to_string('registration/verification_email.html', {
                    'user': user,
                    'verify_url': verify_url,
                })
                plain_message = strip_tags(html_message)
                
                send_mail(
                    '請驗證您的電子郵件',
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                return render(request, 'registration/verification_sent.html', {
                    'email': user.email
                })
            except Exception as e:
                user.delete()
                messages.error(request, '發送驗證郵件時出現錯誤，請稍後再試。')
                return redirect('signup')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def verify_email(request, token):
    try:
        verification = EmailVerification.objects.get(token=token)
        if not verification.is_verified:
            user = verification.user
            user.is_active = True
            user.save()
            verification.is_verified = True
            verification.save()
            return render(request, 'registration/verification_success.html')
        else:
            messages.info(request, '此連結已經被使用過了。')
    except EmailVerification.DoesNotExist:
        messages.error(request, '無效的驗證連結。')
    
    return redirect('login')