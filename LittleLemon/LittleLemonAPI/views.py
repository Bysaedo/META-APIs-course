from rest_framework import generics,viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import User, Group
from .throttles import TenCallsPerMinute
from .models import MenuItem, Category,Rating
from .serializers import MenuItemSerializer, CategorySerializer,RatingSerializer

# Create your views here.
@api_view(['GET','POST'])
def menu_items(request):
  if request.method=='GET':
    items = MenuItem.objects.select_related('category').all()
    category_name = request.query_params.get('category')
    to_price=request.query_params.get('to_price')
    search = request.query_params.get('search')
    ordering=request.query_params.get('ordering')
    perpage = request.query_params.get('perpage', default=2)
    page=request.query_params.get('page', default=1)
    if category_name:
        items=items.filter(category__slug=category_name)
    if to_price:
        items=items.filter(price=to_price)
    if search:
        items=items.filter(title__icontains=search)
    if ordering:
        ordering_fields=ordering.split(",")
        items=items.order_by(*ordering_fields)
    paginator = Paginator(items, per_page=perpage)
    try:
        items=paginator.page(number=page)
    except EmptyPage:
        items=[]
    serialized_item=MenuItemSerializer(items, many=True)
    return Response(serialized_item.data)
  elif request.method=='POST':
      serialized_item=MenuItemSerializer(data=request.data)
      serialized_item.is_valid(raise_exception=True)
      serialized_item.save()
      return Response(serialized_item.data, status.HTTP_201_CREATED)

@api_view()
def single_item(request, id):
  item=get_object_or_404(MenuItem, pk=id)
  serialized_item=MenuItemSerializer(item)
  return Response(serialized_item.data)

@api_view()
@renderer_classes([TemplateHTMLRenderer])
def menu(request):
    items=MenuItem.objects.select_related('category').all()
    serialized_item=MenuItemSerializer(items, many=True)
    return Response({'data':serialized_item.data}, template_name='menu-items.html')

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"Some secret message"})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"Only Manager should see this"})
    else:
        return Response({"message":"You are not authorized"}, 403)
    #USERS HERE????? MANAGERS CAN UPDATE ALL DATA ON THE MENU AND UPDATE USERS TO DELIVERY PERSON
    #IF USER DOESN'T BELONG TO ANY CATEGORY THEN IS A CUSTOMER, BE ABLE TO BROWSE MENU ITEMS, THE HAVE TO HAVE API TO ADD ITEMS TO THEIR CART AND BE ABLE TO PLACE AN ORDER, CUSTOMER CAN HAVE ONLY ONE CART WITH MULTIPLES MENU ITEMS IN IT 
    #DELIVERY, MANAGERS MUST BE ABLE TO BROWSE, ASSIGN AND FILTER ORDERS FOR THE DELIVERY CREW, ALSO BE ABLE TO SEE THE STATUS OF THE ORDER, AFTER AUTHENTICATION DELIVERY PEOPLE SHOULD BE ABLE TO BROWSE THE ORDER ASSIGNED TO THEM, CUSTOMERS SHOULD BE ABLE TO SEE THEIR ORDERS AND STATUS
    #THROTTLING LIMITING 5 CALLS PER MINUTE PER API
@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username=request.data['username']
    if username:
        user=get_object_or_404(User, username=username)
        managers=Group.objects.get(name="Manager")
        if request.method=='POST':
            managers.user_set.add(user)
        elif request.method=='DELETE':
            managers.user_ser.remove(user)
        return Response({"message": "ok"})
    
    return Response({"message": "error"}, status.HTTP_400_BAD_REQUEST)
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "successful"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({"message":"message for the logged in users only"})
class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields=['title']
class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset=MenuItem.objects.all()
    serializer_class = MenuItemSerializer 

class CategoriesView(generics.ListCreateAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer
    ordering_fields=['price', 'inventory']
    filterset_fields=['price', 'inventory']
    search_fields=['category']

class RatingsView(generics.ListCreateAPIView):
    queryset=Rating.objects.all()
    serializer_class=RatingSerializer

    def get_permissions(self):
        if(self.request.method=='GET'):
            return[]
        return[IsAuthenticated()]