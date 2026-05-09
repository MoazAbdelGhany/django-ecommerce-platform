from rest_framework import serializers  
from store.models import Product , Category
from accounts.models import Account

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = ['name', 'slug', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','category','slug','price','description','created_at','updated_at','image','status']
        depth = 1


class RegistrationSerializer(serializers.ModelSerializer): 
    class Meta:  
        model = Account 
        fields = ['first_name','last_name','email','username','phone_number','country','password',]
        extra_kwargs = {'password':{'write_only':True}}

    def create(self , validated_data):
        user = Account.objects.create_user(     # type: ignore
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username'],
            phone_number = validated_data['phone_number'],
            country = validated_data['country'],
            password = validated_data('password')
        )
        return user   