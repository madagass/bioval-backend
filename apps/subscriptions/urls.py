from django.urls import path
from .views import (
    SubscriptionListView,
    SubscriptionDetailView,
    CreateCheckoutSessionView,
    StripeWebhookView,
)

urlpatterns = [
    path("", SubscriptionListView.as_view(), name="subscription-list"),
    path("checkout/", CreateCheckoutSessionView.as_view(), name="checkout-session"),
    path("webhook/", StripeWebhookView.as_view(), name="stripe-webhook"),
    path("<uuid:pk>/", SubscriptionDetailView.as_view(), name="subscription-detail"),
]