from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import JobApplySerializer, JobSerializer, ProductSerializer, OrderItemsSerializer
from .models import Apply, Product, OrderItem, Order, User, Job
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
import json
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.pagination import PageNumberPagination


# Create your views here.
def Home(request):
    return HttpResponse("<h1>This is the home age</h1>")

class CreateJobView(generics.ListCreateAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):

        job = Job.objects.all()

        return job

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')
        user = User.objects.get(id = user_id)
        serializer.save(user = user)

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'

class ProductView(generics.ListCreateAPIView):
    # permission_classes = [AllowAny, IsAuthenticated]
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        # product = Product.objects.all()
        product = Product.objects.all().order_by("-created_at")
        return product
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)
    



class order_item(APIView):

    def post(self, request):

        serializer = JobApplySerializer( data = request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED )

        user_id = serializer.validated_data['user_id']
        job_id = serializer.validated_data['job_id']

        list_apply = Apply.objects.all()

        for applications in list_apply:
            if applications.job.id == job_id and applications.user.id == user_id:
                response = {
                    "msg" : "This user already applied for this job"
                }  

                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id = user_id)
        job = Job.objects.get(id = job_id)

        new_application = Apply(user = user, job = job)
        new_application.save()

        response = {
            "msg" : "Application Successful"
        }

        return Response(response, status=status.HTTP_201_CREATED)


    def get(self, request):
        user_id = request.query_params.get('id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        list_jobs = Job.objects.filter(user=user)
        apply_list = Apply.objects.all()

        serializer = JobSerializer(list_jobs, many=True)

        send_list = []

        for job in list_jobs:
            for app in apply_list:
                if job.id == app.job.id:
                    new_data = {
                        "id" : app.user.id, 
                        "profile_id" : "2", 
                        "job_title" : job.job_title, 
                        "experience" : "3",
                        "hourly_rate" : 12500.00,
                        "languages": "English", 
                        "bio" : "Hello",
                        "skills" : "Hello", 
                        "education" : "Hello",
                        "website_link": "https://emilyrodriguez.analytics",
                        "linkedin_link": "https://linkedin.com/in/emily-rodriguez-data",
                        "name": f"{app.user.first_name} {app.user.last_name}",
                        "email": app.user.email,
                        "phone": app.user.phone_number,
                        "location": app.user.address_default,
                        "jobId": app.job.id,
                        "appliedDate": "2024-06-23",
                        "expectedSalary": 520000,
                        "status": "pending",
                        "rating": 4.2,
                        "avatar": "ER"
                    }

                    send_list.append(new_data)



    
        return Response({"data" : serializer.data, "app" : send_list}, status=status.HTTP_200_OK)