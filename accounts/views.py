from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from django.http import HttpResponse # type: ignore
from django.contrib import messages, auth # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from carts.models import Cart, CartItem
from carts.views import _cart_id

# verification email 
from django.contrib.sites.shortcuts import get_current_site # type: ignore
from django.template.loader import render_to_string # type: ignore
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode # type: ignore
from django.utils.encoding import force_bytes # type: ignore
from django.contrib.auth.tokens import default_token_generator # type: ignore
from django.core.mail import EmailMessage # type: ignore
import requests
# Create your views here.

def register(request): 
    if request.method == "POST": 
        form = RegistrationForm(request.POST)
        if form.is_valid(): 
            email = form.cleaned_data['email']
            user = Account.objects.create_user(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                username = form.cleaned_data['email'].split("@")[0],
                email = email,
                password = form.cleaned_data['password'],
            )
            user.phone = form.cleaned_data['phone']
            user.save()
            
            # create user profile 
            profile = UserProfile()
            profile.user_id = user.id 

            profile.profile_picture = 'default/default-user.png'
            profile.save()

            # User Activation email system 
            current_site = get_current_site(request)
            mail_subject = 'Please Activate your account'
            message = render_to_string('BestStore/accounts/account_verification_email.html', {
                 'user': user, 
                 'domain': current_site,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            #messages.success(request, 'We have sent you a verification email please verify ')
            return redirect('accounts/login/?command=verification&email=' + email)
           
    else: 
          form = RegistrationForm()
         


    context = {
        'form': form ,
        
    }

    return render(request, 'BestStore/accounts/register.html', context)

def login(request): 
    if request.method == "POST": 
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user: 
                try: 
                     cart = Cart.objects.get(cart_id=_cart_id(request))
                     is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()   
                     if is_cart_item_exist: 
                          cart_item = CartItem.objects.filter(cart=cart)
                          # Getting the product variation by cart ID
                          product_variation = []
                          for item in cart_item:
                               variation = item.variations.all() 
                               product_variation.append(list(variation))
                         
                         # get cart item from the user to access the product variation 
                          cart_item = CartItem.objects.filter(user=user)
        
                          ex_var_list = []
                          id = []
                          for item in cart_item: 
                              existing_variation = item.variations.all()
                              ex_var_list.append(list(existing_variation))
                              id.append(item.id)

                          # getting common product  variations
                          for pr in product_variation: 
                               if pr in ex_var_list: 
                                    index = ex_var_list.index(pr)
                                    item_id = id[index]
                                    item = CartItem.objects.get(id=item_id)
                                    item.quantity +=1
                                    item.user = user
                                    item.save()
                               else: 
                                   cart_item = CartItem.objects.filter(cart=cart)
                                   for item in cart_item: 
                                        item.user = user
                                        item.save()
                              
                except: 
                     pass
                auth.login(request, user) 
                messages.success(request, 'successfully logged in ')
                url = request.META.get('HTTP_REFERER')
                try: 
                     query = requests.utils.urlparse(url).query
                     params = dict(x.split('=') for x in query.split('&'))
                     if 'next' in params: 
                          nextPage = params['next']
                          return redirect(nextPage)

                except: 
                     return redirect('dashboard')
        else: 
            messages.error(request, 'invalid login cridentials')
            return redirect('login')
  
    
    return render(request, 'BestStore/accounts/login.html')


@login_required(login_url = 'login')
def logout(request): 
    auth.logout(request)
    messages.success(request, 'you are logged out')
    
    return redirect('login')

def activate(request, uidb64, token):
     try: 
          uid = urlsafe_base64_decode(uidb64).decode()
          user = Account._default_manager.get(pk=uid)
     except(TypeError, ValueError, OverflowError, Account.DoesNotExist): 
          user = None
     if user is not None and default_token_generator.check_token(user, token): 
          user.is_active = True
          user.save()
          messages.success(request, 'Congratulations your account is activated')
          return redirect('login')
     else: 
          messages.error(request, 'Invalid activation link')
          return redirect('register')

@login_required(login_url = 'login')
def dashboard(request): 
     
     return render(request, 'BestStore/accounts/dashboard.html')

def forgotPassword(request): 
     if request.method == "POST": 
          email = request.POST['email']
          check_email = Account.objects.filter(email=email)
          if check_email.exists(): 
               user = Account.objects.get(email__iexact=email)

               # Reset password Email..................................................
               current_site = get_current_site(request)
               mail_subject = 'Please reset your password'
               message = render_to_string('BestStore/accounts/reset_password_email.html', {
                    'user': user, 
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                })
               to_email = email
               send_email = EmailMessage(mail_subject, message, to=[to_email])
               send_email.send()
               messages.success(request, 'Password reset email has been sent to your email address')
               return redirect('login')

          
          else: 
               messages.error(request, 'account does not exist')

               return redirect('forgotpassword')
               
     
     return render(request, 'BestStore/accounts/forgotpassword.html')

def reset_password_validate(request, uidb64, token): 
     try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
     except(TypeError, ValueError, OverflowError, Account.DoesNotExist): 
          user=None
     if user is not None and default_token_generator.check_token(user, token): 
          request.session['uid'] = uid
          messages.success(request, 'please reset your password')
          return redirect('reset_password')
     else: 
          messages.error(request, 'This link has expired')
          return redirect('login')
     

def reset_password(request): 
     if request.method == "POST": 
          password = request.POST['password']
          confirm_password = request.POST['confirm_password']
          if password == confirm_password:
               uid = request.session.get('uid') 
               user = Account.objects.get(pk=uid)
               user.set_password(password)
               user.save()
               messages.success(request, 'Password reset successful')
               return redirect('login')     
          else: 
               messages.error(request, 'password do not match')
               return redirect('reset_password')
     else:          
      return render(request, 'BestStore/accounts/reset_password.html')
     

def my_orders(request): 

     return render(request, 'BestStore/accounts/my_orders.html')


@login_required(login_url='login')
def edit_profile(request): 
     userprofile = get_object_or_404(UserProfile, user=request.user)
     if request.method == "POST": 
          user_form = UserForm(request.POST, instance=request.user)
          profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
          if user_form.is_valid() and profile_form.is_valid(): 
               user_form.save()
               profile_form.save()
               messages.success(request, 'Your profile has been update')
               return redirect('edit_profile')
     else: 
          user_form = UserForm(instance=request.user) 
          profile_form = UserProfileForm(instance=userprofile) 
     context = {
          'user_form': user_form,
          'profile_form': profile_form,
          'user_profile':  userprofile,

     }  

     return render(request, 'BestStore/accounts/edit_profile.html', context)

@login_required(login_url='login')
def change_password(request):
     if request.method == "POST": 
          current_password = request.POST['current_password']
          new_password = request.POST['new_password']
          confirm_new_password = request.POST['confirm_new_password']

          user = Account.objects.get(username__exact=request.user.username)

          if new_password == confirm_new_password: 
               success = user.check_password(current_password)
               if success: 
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password updated successfully')
                    return redirect('change_password')
               else: 
                    messages.error(request, 'Please enter valid current password')
                    return redirect('change_password')
          else: 
               messages.error(request, 'password do not match')
               return redirect('change_password')
     return render(request, 'BestStore/accounts/change_password.html')