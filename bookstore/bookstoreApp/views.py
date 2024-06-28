from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView  
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import MyTokenObtainPairSerializer,RegisterSerializer,BookSerializer
from .models import CustomUser,Book
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
from rest_framework import status
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework.negotiation import DefaultContentNegotiation


# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

#Register User
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
class BookView(APIView):    
    #http://example.com/api/purchases?title=Der%20Turm
     authentication_classes = []
     permission_classes = []
     renderer_classes = [XMLRenderer,JSONRenderer] #,
   
     
     def get_queryset(self):       
        queryset = Book.objects.all()
        title = self.request.query_params.get('title')
        if title is not None:
            queryset = queryset.filter(title=title)
        return queryset
    
     def get(self,request):                
            queryset = self.get_queryset()
            serializer = BookSerializer(queryset, many=True)     
            content_type = request.META.get('CONTENT_TYPE')
           
            if content_type == 'application/xml':
             print("XMLRenderer")
             renderer = XMLRenderer()
            else:
             print("JSONRenderer")
             renderer = JSONRenderer()          
            response = Response(serializer.data)
            response.accepted_renderer = renderer
            response.accepted_media_type = 'application/json'#renderer.media_type
            response.renderer_context = self.get_renderer_context()
        
            return response
                           
             

class BookCRUDView(APIView): 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]       
    renderer_classes = [XMLRenderer,JSONRenderer] 
    
    def post(self,request):
        data = json.loads(request.body)         
        # Erstelle ein neues Book-Objekt
        try:
            if data['title']=="":
                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                book = Book.objects.create(
                    title=data['title'],
                    description=data['description'],
                    author_id=data['author_id'],
                    cover_image=data['cover_image'],
                    price=data['price']
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)        
      
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 
    def get(self,request):          
          queryset = Book.objects.all()
          serializer = BookSerializer(queryset, many=True)
          return Response(serializer.data)
    def put(self,request):        
        data = json.loads(request.body)
        print(data)    
        book = Book.objects.filter(id = data['id'])[0] 
        user = CustomUser.objects.filter(id =data['author_id'])[0]       
        try:            
            book.title=data['title']
            book.description=data['description']          
            book.price=data['price']
            book.save()
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)      
        serializer = BookSerializer(book,many=False)    
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def delete(self,request):
         data = json.loads(request.body) 
         user = request.user
         book = Book.objects.filter(author=user,title=data['title'])
         if len(book)>0:
          book[0].delete()
          return Response("Book DELETED", status=status.HTTP_201_CREATED)
         return Response("Book does not exist.", status=status.HTTP_201_CREATED)
         


