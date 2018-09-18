from django.contrib import messages, auth
from django.urls import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from accounts.forms import UserRegistrationForm, UserLoginForm, CreditCardForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import User
import stripe

stripe.api_key = settings.STRIPE_SECRET

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            user = auth.authenticate(username=request.POST.get('email'),
                                     password=request.POST.get('password1'))

            if user:
                messages.success(request, "You have successfully registered")
                return redirect(reverse('profile'))

            else:
                messages.error(request, "unable to log you in at this time!")

    else:
        form = UserRegistrationForm()

    args = {'form': form}
    args.update(csrf(request))

    return render(request, 'register.html', args)

@login_required(login_url='/login/')
def profile(request):
    return render(request, 'profile.html')

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=request.POST.get('email'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                messages.error(request, "You have successfully logged in")
                return redirect(reverse('profile'))
            else:
                form.add_error(None, "Your email or password was not recognized")

    else:
        form = UserLoginForm()

    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'login.html', args)

def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect(reverse('index'))

def add_card(request):
    if request.method == 'POST':
        if not request.user.stripe_id:
            #Check to see if customer exists in database, if not, create Stripe.customer and save token to stripe_id
            try:
                customer = stripe.Customer.create(
                    description="Customer for " + str(request.user.username),
                    source=request.POST.get('stripeToken')
                )
            except stripe.error.StripeError as e:
                messages.error(request,"Could not create a customer with Stripe.")
            messages.success(request,"Stripe customer has been created.")
            #Add customer token to database
            user = User.objects.get(id=request.user.id)
            user.stripe_id = customer.id
            user.save()
        else:
            try:
                customer = stripe.Customer.retrieve(request.user.stripe_id)
                customer.sources.create(source=request.POST.get('stripeToken'))
            except stripe.error.StripeError as e:
                messages.error(request, "Could not add card to customer with Stripe.")
            messages.success(request,"Card has been added to your account.")
    else:
        return render(request, 'stripe/card_form.html')
    args = {'stripe_key':settings.STRIPE_PUBLISHABLE}
    args.update(csrf(request))
    return render(request, 'stripe/card_form.html', args)