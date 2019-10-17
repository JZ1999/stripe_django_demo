import stripe
from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from .serializers import DemoChargeSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):  # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def charge(request):  # new
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        print(charge)
        return render(request, 'charge.html')


class DemoCharge(viewsets.ViewSet):
    serializer_class = DemoChargeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return Response(serializer.save(), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
