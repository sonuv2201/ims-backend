from django.shortcuts import render
from rest_framework import viewsets

from generic.views import GenericModelViewSet

from homerun.models import Book
from homerun.serializer import (
    BookSerializer,
)
from homerun.models import Book
from homerun.serializer import BookSerializer

# Create your views here.


class BookViewSet(GenericModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
