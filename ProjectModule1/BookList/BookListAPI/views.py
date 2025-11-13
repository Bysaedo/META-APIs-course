from django.shortcuts import render
#from django.http import HttpResponse
#from django.db import IntegrityError
#from django.http import JsonResponse
from .models import Book
#from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import BookSerializer
from rest_framework import generics

@api_view (['GET', 'POST'])
def books(request):
    return Response('list of the books', status=status.HTTP_200_OK)

"""class BookList(APIView):
    def get(self, request):
        author = request.GET.get('author')
        if(author):
            return Response({"message":"List of books by"}, status.HTTP_200_OK)
        return Response({"message":"List of books"}, status.HTTP_200_OK) 
    def post(self, request):
        return Response({"title":request.data.get('title')}, status.HTTP_201_CREATED)
    
class SingleBook(APIView):
    def get(self, request, pk):
        return Response({"message":"single book with id" + str(pk)}, status.HTTP_200_OK)
    def put(self, request, pk):
        return Response({"title":request.data.get('title')}, status.HTTP_200_OK)"""
    
class BookView(generics.ListCreateAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
class BookDetailView(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    
"""
@csrf_exempt
def books(request):
    if request.method =='GET':
        books = Book.objects.all().values()
        return JsonResponse({'books': list(books)})
    elif request.method == 'POST':
        title =request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')

        book = Book(title=title, author=author, price = price)
        try:
            book.save()
        except IntegrityError:
            return JsonResponse({'error': 'true', 'message': 'required field missing'}, status =400)
        
        return Response('list of the books', status=status.HTTP_200_OK)
    """