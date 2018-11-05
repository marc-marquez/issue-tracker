from django.contrib import messages, auth
from django.urls import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from accounts.forms import UserRegistrationForm, UserLoginForm
from .models import User

stripe.api_key = settings.STRIPE_SECRET

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            user = auth.authenticate(username=request.POST.get('email'),
                                     password=request.POST.get('password1'))

            try:
                # Need to create a stripe token and save to database
                customer = create_stripe_customer(user)
                save_stripe_customer(customer.id,user.id)
            except:
                print("Could not add user to Stripe.")

            #if user:
            if customer:
                messages.success(request, "You have successfully registered. ")
                return redirect(reverse('login'))
            else:
                messages.error(request, "Unable to register you at this time! ")
    else:
        form = UserRegistrationForm()

    args = {'form': form}
    args.update(csrf(request))

    return render(request, 'register.html', args)

@login_required(login_url='/login/')
def profile(request):
    try:
        customer = stripe.Customer.retrieve(request.user.stripe_id)
    except:
        #If no customer found on Stripe, create it.
        customer = create_stripe_customer(request.user)
        save_stripe_customer(customer.id, request.user.id)
        return redirect(reverse('profile'))

    try:
        cards = stripe.Customer.retrieve(customer.id).sources.list(object='card')
        default_source = customer.default_source
    except:
        cards = None
        default_source = None

    args = {'cards':cards, 'default_source':default_source}
    return render(request, 'profile.html', args)

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=request.POST.get('email'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)

                #try to recover stripe id from stripe database
                try:
                    existing_stripe_customer = stripe.Customer.list(email=request.user.email,
                                                                    limit=1)
                    customer = stripe.Customer.retrieve(existing_stripe_customer.data[0]['id'])
                except:
                    customer = create_stripe_customer(user)

                if customer:
                    save_stripe_customer(customer.id, user.id)
                    messages.success(request, "You have successfully logged in.")
                else:
                    messages.error(request,"Could not find customer in database.")

                return redirect(reverse('index'))
            else:
                messages.error(request, "Your email or password was not recognized.")

    else:
        form = UserLoginForm()

    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'login.html', args)

def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect(reverse('index'))

@login_required(login_url='/login/')
def add_card(request):
    if request.method == 'POST':
        if not request.user.stripe_id:
            #Check to see if customer exists in database, if not, redirect to profile
            try:
                #try to find customer in stripe database first!
                existing_stripe_customer = stripe.Customer.list(email=request.user.email, limit=1)

                #if existing_stripe_customer:
                customer = stripe.Customer.retrieve(existing_stripe_customer.data[0]['id'])
            except stripe.error.CardError as e:
                message = str(e).split(":", maxsplit=1)[1]
                messages.error(request, message)
                return redirect(reverse('profile'))

            if customer:
                save_stripe_customer(customer.id, request.user.id)
            else:
                print("ERROR: Could not save Stripe customer.")
        else:
            try:
                customer = stripe.Customer.retrieve(request.user.stripe_id)
                source = customer.sources.create(source=request.POST.get('stripeToken'))
            except stripe.error.CardError as e:
                message = str(e).split(":", maxsplit=1)[1]
                messages.error(request, message)
                return redirect(reverse('profile'))

            if source:
                messages.success(request, source.brand + " ending in (" + source.last4 +
                                 ") has been added to your account.")
    else:
        return render(request, 'stripe/card_form.html')

    args = {'stripe_key':settings.STRIPE_PUBLISHABLE}
    args.update(csrf(request))
    return redirect(reverse('profile'))

@login_required(login_url='/login/')
def delete_card(request, card_id):
    if request.method == 'POST':
        customer = stripe.Customer.retrieve(request.user.stripe_id)
        card = customer.sources.retrieve(card_id)
        brand = card.brand
        last4 = card.last4
        try:
            deleted_card = card.delete()
        except stripe.error.CardError as e:
            message = str(e).split(":", maxsplit=1)[1]
            messages.error(request, message)
            return redirect(reverse('profile'))

        if deleted_card.deleted:
            messages.success(request, brand + " ending in (" + last4 + ") has been deleted.")

    return redirect(reverse('profile'))

@login_required(login_url='/login/')
def set_default_card(request, card_id):
    if request.method == 'POST':
        customer = stripe.Customer.retrieve(request.user.stripe_id)
        try:
            customer.default_source = card_id
            customer.save()
        except stripe.error.CardError as e:
            message = str(e).split(":", maxsplit=1)[1]
            messages.error(request, message)
            return redirect(reverse('profile'))

        if customer.default_source == card_id:
            card = customer.sources.retrieve(card_id)
            messages.success(request, card.brand + " ending in (" + card.last4 +
                             ") has been set to default.")

    return redirect(reverse('profile'))

def create_stripe_customer(user):
    customer = stripe.Customer.create(
        description="Customer for " + str(user.username),
        email=user.email,
    )
    return customer

def save_stripe_customer(customer_id,user_id):
    user = User.objects.get(id=user_id)
    user.stripe_id = customer_id
    user.save()
    return





