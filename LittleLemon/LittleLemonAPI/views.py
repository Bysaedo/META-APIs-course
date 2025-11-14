from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage

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