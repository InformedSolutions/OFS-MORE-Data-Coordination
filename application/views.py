from django.shortcuts import render
from application import automatic_deletion
# Create your views here.


def test_view(request):

    print(automatic_deletion.automatic_deletion())

