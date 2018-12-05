"""
These are the views to:
    - Register users
    - See a user profile
    - Log in a user
    - Log out a user
    - Add a credit card to the user
    - Delete a credit card from the user
    - Set the default credit card of a user
"""

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
    """
    Creates registration html page
    :param request: The request type
    :return: register page
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            user = auth.authenticate(username=request.POST.get('email'),
                                     password=request.POST.get('password1'))

            try:
                # Need to create a stripe token and save to database
                customer = create_stripe_customer(user)
                save_stripe_customer(customer.id, user.id)
            except:
                print('Could not add user to Stripe.')

            if customer:
                messages.success(request, 'You have successfully registered. ')
                return redirect(reverse('login'))
            else:
                messages.error(request, 'Unable to register you at this time! ')
    else:
        form = UserRegistrationForm()

    args = {'form': form}
    args.update(csrf(request))

    return render(request, 'register.html', args)


@login_required(login_url='/login/')
def profile(request):
    """
    Creates the profile html page
    :param request: The request type
    :return: profile page
    """
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
    """
    Creates the login page
    :param request: The request type
    :return: login page
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=request.POST.get('email'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                messages.success(request, 'You have successfully logged in.')
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect(reverse('index'))
            else:
                messages.error(request, 'Your email or password was not recognized.')

    else:
        form = UserLoginForm()

    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'login.html', args)


def logout(request):
    """
    Processes the logout
    :param request: The request type
    :return: Redirects to index page
    """
    auth.logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect(reverse('index'))


@login_required(login_url='/login/')
def add_card(request):
    """
    Adds credit card to Stripe customer
    :param request: The request type
    :return: Profile page with status message for successful or unsuccessful add.
    """
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
                print('ERROR: Could not save Stripe customer.')
        else:
            try:
                customer = stripe.Customer.retrieve(request.user.stripe_id)
                source = customer.sources.create(source=request.POST.get('stripeToken'))
            except stripe.error.CardError as e:
                message = str(e).split(":", maxsplit=1)[1]
                messages.error(request, message)
                return redirect(reverse('profile'))

            if source:
                messages.success(request, source.brand + ' ending in (' + source.last4 +
                                 ') has been added to your account.')
    else:
        return render(request, 'stripe/card_form.html')

    args = {'stripe_key':settings.STRIPE_PUBLISHABLE}
    args.update(csrf(request))
    return redirect(reverse('profile'))


@login_required(login_url='/login/')
def delete_card(request, card_id):
    """
    Deletes credit card from Stripe customer
    :param request: The request type
    :param card_id: Stripe id for card being deleted
    :return: Profile page with status message for successful or unsuccessful deletion.
    """
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
            messages.success(request, brand + ' ending in (' + last4 + ') has been deleted.')

    return redirect(reverse('profile'))


@login_required(login_url='/login/')
def set_default_card(request, card_id):
    """
    Sets the default credit card for the Stripe customer
    :param request: The request type
    :param card_id: Stripe id for card being set to default
    :return: Profile page with status message for successful or unsuccessful default status.
    """
    if request.method == 'POST':
        customer = stripe.Customer.retrieve(request.user.stripe_id)
        try:
            customer.default_source = card_id
            customer.save()
        except stripe.error.CardError as e:
            message = str(e).split(':', maxsplit=1)[1]
            messages.error(request, message)
            return redirect(reverse('profile'))

        if customer.default_source == card_id:
            card = customer.sources.retrieve(card_id)
            messages.success(request, card.brand + ' ending in (' + card.last4 +
                             ') has been set to default.')

    return redirect(reverse('profile'))


def create_stripe_customer(user):
    """
    Creates a customer in the Stripe database
    :param user: User that needs to be added as a Stripe customer
    :return: Stripe customer object
    """
    customer = stripe.Customer.create(
        description='Customer for ' + str(user.username),
        email=user.email,
    )
    return customer


def save_stripe_customer(customer_id, user_id):
    """
    Saves the stripe customer token id to local database
    :param customer_id: Stripe id of customer
    :param user_id: User id in local database
    :return: None
    """
    user = User.objects.get(id=user_id)
    user.stripe_id = customer_id
    user.save()
