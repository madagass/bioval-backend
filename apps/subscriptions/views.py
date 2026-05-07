import stripe
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Subscription
from .serializers import (
    SubscriptionSerializer,
    SubscriptionStatusSerializer,
    CheckoutSessionSerializer,
)
from apps.users.permissions import IsAdminGlobal, IsAdminMetier, IsAdminGlobalOrExterne
from apps.groups.models import Group

stripe.api_key = settings.STRIPE_SECRET_KEY


class SubscriptionListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        group_id = self.request.query_params.get("group_id")

        if user.role == "admin_global":
            qs = Subscription.objects.all()
        elif user.role == "admin_externe":
            qs = Subscription.objects.filter(group__membres=user)
        else:
            return Subscription.objects.none()

        if group_id:
            qs = qs.filter(group__id=group_id)

        return qs


class SubscriptionDetailView(generics.RetrieveUpdateAPIView):
    queryset = Subscription.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return SubscriptionStatusSerializer
        return SubscriptionSerializer

    def get_permissions(self):
        if self.request.method in ["PATCH", "PUT"]:
            return [IsAdminGlobalOrExterne()]
        return super().get_permissions()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        new_statut = serializer.validated_data.get("statut")

        # cancel on Stripe if cancelling
        if new_statut == "inactive" and instance.stripe_subscription_id:
            try:
                stripe.Subscription.cancel(instance.stripe_subscription_id)
            except stripe.error.StripeError:
                pass

        instance.statut = new_statut
        instance.save()
        return Response(SubscriptionSerializer(instance).data)


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAdminGlobalOrExterne]

    def post(self, request):
        serializer = CheckoutSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group_id = serializer.validated_data["group_id"]

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"detail": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="subscription",
                line_items=[{
                    "price": settings.STRIPE_PRICE_ID,
                    "quantity": 1,
                }],
                metadata={"group_id": str(group_id)},
                success_url=settings.FRONTEND_URL + "/subscriptions?success=true",
                cancel_url=settings.FRONTEND_URL + "/subscriptions?cancelled=true",
            )
            return Response({"url": session.url})
        except stripe.error.StripeError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StripeWebhookView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            group_id = session["metadata"].get("group_id")
            stripe_sub_id = session.get("subscription")

            if group_id:
                try:
                    group = Group.objects.get(id=group_id)
                    Subscription.objects.update_or_create(
                        group=group,
                        defaults={
                            "statut": "active",
                            "stripe_subscription_id": stripe_sub_id or "",
                            "date_debut": timezone.now(),
                            "date_fin": timezone.now() + timedelta(days=30),
                        },
                    )
                except Group.DoesNotExist:
                    pass

        elif event["type"] == "customer.subscription.deleted":
            stripe_sub_id = event["data"]["object"]["id"]
            Subscription.objects.filter(
                stripe_subscription_id=stripe_sub_id
            ).update(statut="inactive")

        return Response({"status": "ok"})