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
                messages.success(request, "You have successfully registered. ")
                return redirect(reverse('profile'))
            else:
                messages.error(request, "Unable register you at this time! ")
    else:
        form = UserRegistrationForm()

    args = {'form': form}
    args.update(csrf(request))

    return render(request, 'register.html', args)

@login_required(login_url='/login/')
def profile(request):
    try:
        customer = stripe.Customer.retrieve(request.user.stripe_id)
        cards = stripe.Customer.retrieve(customer.id).sources.list(object='card')
        default_source = customer.default_source
    except:
        messages.error(request,"No customer on file.")
        return redirect(reverse('profile'))

    args = {'cards':cards,'default_source':default_source}
    return render(request, 'profile.html',args)

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=request.POST.get('email'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                messages.success(request, "You have successfully logged in.")
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

@login_required
def add_card(request):
    if request.method == 'POST':
        if not request.user.stripe_id:
            #Check to see if customer exists in database, if not, create Stripe.customer and save token to stripe_id
            try:
                customer = stripe.Customer.create(
                    description="Customer for " + str(request.user.username),
                    source=request.POST.get('stripeToken')
                )
            except stripe.error.CardError as e:
                message = str(e).split(":",maxsplit=1)[1]
                messages.error(request,message)
                return redirect(reverse('profile'))

            if (customer):
                messages.success(request,"Stripe customer has been created.")

                #Add customer token to database
                user = User.objects.get(id=request.user.id)
                user.stripe_id = customer.id
                user.save()
            else:
                messages.error(request, "Stripe customer was NOT created.")
        else:
            try:
                customer = stripe.Customer.retrieve(request.user.stripe_id)
                source = customer.sources.create(source=request.POST.get('stripeToken'))
            except stripe.error.CardError as e:
                message = str(e).split(":", maxsplit=1)[1]
                messages.error(request, message)
                return redirect(reverse('profile'))

            if (source):
                messages.success(request,"Card has been added to your account.")
    else:
        return render(request, 'stripe/card_form.html')

    args = {'stripe_key':settings.STRIPE_PUBLISHABLE}
    args.update(csrf(request))
    return redirect(reverse('profile'))

'''
def get_cards(request):
    try:
        customer = stripe.Customer.retrieve(request.user.stripe_id)
        cards = stripe.Customer.retrieve(customer.id).sources.list(object='card')
    except:
        messages.error(request,"No customer on file.")
        return render(request, 'stripe/cards.html')
    #if request.method == 'POST':
    #    pass

    args = {'cards':cards}
    return render(request,'stripe/cards.html',args)
'''

@login_required
def delete_card(request,card_id):
    if request.method == 'POST':
        print("Made it to POST in delete_card")
        customer = stripe.Customer.retrieve(request.user.stripe_id)
        try:
            deleted_card = customer.sources.retrieve(card_id).delete()
        except stripe.error.CardError as e:
            message = str(e).split(":", maxsplit=1)[1]
            messages.error(request, message)
            return redirect(reverse('profile'))

        if deleted_card.deleted:
            messages.success(request,"Card has been deleted.")

    return redirect(reverse('profile'))

def edit_card(request):
    pass
