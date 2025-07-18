from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# for api filtering
from .filters import ServiceItemFilter

from django.shortcuts import get_object_or_404

from .models import ServiceItem, ServiceSignUp

from .serializers import (
    ServiceItemSerializer,
    ServiceSignupSerializer,
    ServiceItemDetailSerializer,
)

"""For all service items & creation of new service items"""


class ServiceItemListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.query_params.get("user_services"):
            # Handle `/api/services/?user_services=true`
            services = ServiceItem.objects.filter(
                servicesignup__user_id=request.user.user_id
            )
            serializer = ServiceItemSerializer(services, many=True)
            return Response(serializer.data)

        # Default filtered list
        filtered = ServiceItemFilter(request.GET, queryset=ServiceItem.objects.all())
        serializer = ServiceItemSerializer(filtered.qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data["service_provider"] = str(request.user.user_id)  # auto-assign creator

        serializer = ServiceItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""For a service item"""


class ServiceItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, service_id):
        try:
            service = get_object_or_404(
                ServiceItem, service_id=service_id
            )  # ServiceItem.objects.get(service_id=service_id)
        except ServiceItem.DoesNotExist:
            return Response(
                {"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ServiceItemDetailSerializer(service)
        return Response(serializer.data)

    def patch(self, request, service_id):
        service = get_object_or_404(ServiceItem, service_id=service_id)
        serializer = ServiceItemDetailSerializer(
            service, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_id):
        service = get_object_or_404(ServiceItem, service_id=service_id)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""For creating a new signup item"""


class ServiceItemSignUpView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, service_id):
        try:
            service = ServiceItem.objects.get(pk=service_id)
        except ServiceItem.DoesNotExist:
            return Response({"error": "Service not found."}, status=404)

        signup = ServiceSignUp.objects.create(
            user_id=str(request.user.user_id),
            service=service,
            start_date=request.data.get("start_date"),
            end_date=request.data.get("end_date"),
            messages=request.data.get("messages", ""),
        )

        serializer = ServiceSignupSerializer(signup)
        return Response(serializer.data, status=201)


"""For getting all signups for a specific service"""


class ServiceSignUpDetailView(APIView):
    permission_classes = [IsAuthenticated]

    # To get specific signup details
    def get(self, request, signup_id):
        signup = get_object_or_404(ServiceSignUp, signup_id=signup_id)
        serializer = ServiceSignupSerializer(signup)
        return Response(serializer.data)

    # To update specific signup details
    def patch(self, request, signup_id):
        new_status = request.data.get("status")  # expected: "accepted" or "rejected"

        if new_status not in ["accepted", "rejected"]:
            return Response(
                {"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST
            )

        signup = get_object_or_404(ServiceSignUp, pk=signup_id)
        service = signup.service

        # Enforce only the service provider can approve/reject
        if service.service_provider != str(request.user.user_id):
            print("broke here?")
            return Response(
                {"error": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN
            )

        # Just update status — do not modify unavailable dates
        signup.status = new_status
        signup.save()
        print(signup)

        return Response(
            {"message": f"Signup status updated to '{new_status}'."},
            status=status.HTTP_200_OK,
        )

    # To delete specific signup details
    def delete(self, request, signup_id):
        signup = get_object_or_404(ServiceSignUp, signup_id=signup_id)
        signup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_services_by_user(request, user_id):
    services = ServiceItem.objects.filter(service_provider=user_id)
    serialized = ServiceItemSerializer(services, many=True)
    return Response({"services": serialized.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_services_exculde_user(request):
    services = ServiceItem.objects.exclude(service_provider=request.user.user_id)
    serialized = ServiceItemSerializer(services, many=True)
    return Response(serialized.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_visibility(request):
    service = get_object_or_404(ServiceItem, service_id=request.data.get("service_id"))
    serializer = ServiceItemDetailSerializer(
        service, data={"visibility": request.data.get("visibility")}, partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
