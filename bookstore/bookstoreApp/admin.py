from django.contrib import admin
from .models import CustomUser,Book

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    fields = ('username','email','author_pseudonym')    
    list_display =  ('username','email','author_pseudonym')
    search_fields =  ('username',)
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price')
    search_fields = ('title', 'author__username')