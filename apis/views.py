from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import api_view , permission_classes 
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer , ProductSerializer , RegistrationSerializer
from store.models import Product , Category
from accounts.models import Account
from django.utils.encoding import force_bytes , force_str
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated



# Store api_view
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def category_api(request , slug = None):
    serializer = CategorySerializer
    if request.method == 'GET':
        if slug:
            qs = get_object_or_404(Category ,slug = slug)
            serializer = CategorySerializer(qs)
            return Response(serializer.data , status=status.HTTP_200_OK)
        else:
            qs = Category.objects.all()
            serializer = CategorySerializer(qs , many = True)
            return Response(serializer.data , status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Object Created Successful'} , status= status.HTTP_201_CREATED)
    
    elif request.method in ['PUT','PATCH']:
        category = get_object_or_404(Category , slug=slug)
        partial = request.method == 'PATCH'
        serializer = CategorySerializer(category , data = request.data , partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Object Updated Successfully.'}, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        category = get_object_or_404(Category , slug=slug)
        category.delete()
        return Response({'message':'Object Deleted Successfully.'} , status=status.HTTP_204_NO_CONTENT)

    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST )

@api_view(['GET','POST','PUT','PATCH','DELETE'])
def product_api(request , slug = None):
    serializer = ProductSerializer
    if request.method == 'GET':
        if slug:    
            qs = get_object_or_404(Product, slug = slug , status = Product.Status.AVAILABLE )
            serializer = ProductSerializer(qs)
            return Response(serializer .data, status = status.HTTP_200_OK)
        else:
            qs = Product.objects.filter(status=Product.Status.AVAILABLE)
            serializer = ProductSerializer(qs , many = True)
            return Response(serializer .data, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
    
    elif request.method in ['PUT','PATCH']:
        product = get_object_or_404(Product , slug = slug , status = Product.Status.AVAILABLE)
        partial = request.method == 'PATCH'
        serializer = ProductSerializer(product , data = request.data , partial = partial)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Object Updated Successfully.'},status = status.HTTP_200_OK)
        
    elif request.method == 'DELETE':
        product = get_object_or_404(Product , status = Product.Status.AVAILABLE , slug = slug)
        product.delete()
        return Response(
            {'message':'Object Deleted Successfully.'},
            status = status.HTTP_204_NO_CONTENT
        )

    return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)


# Accounts api_view
@api_view(['POST'])
def registrationUserView(request):
    data = request.data
    serializer = RegistrationSerializer(data = data)
    if serializer.is_valid():
        user = serializer.save()  
        if isinstance(user, list):
            user = user[0]
        user.is_active = False
        user.save()

        # Send verification Email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = f'localhost:8000/v1/api/activate/{uid}/{token}'
        email = user.email
        send_mail = EmailMessage(
            subject='Email Activation',
            body=f'Click here to activate your account: {activation_link}',
            from_email= settings.DEFAULT_FROM_EMAIL,
            to= [email],
        )
        send_mail.send()
        return Response({'message':'Account Created , Check your email to activate.'},status=status.HTTP_200_OK)
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def activationView(request, uid64 , token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = Account.objects.get(pk = uid)

        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return Response({'message':'Account activated successfully'}, status=status.HTTP_200_OK)
        return Response({'message':'Your activation link is not valid'},status=status.HTTP_400_BAD_REQUEST)
    except Account.DoesNotExist:
        return Response({'error':'User Not Found'},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([IsAuthenticated]) 
@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token :
            return Response({'message':'Refresh token is required'},status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message":'Loged OUt Successfully'} , status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


