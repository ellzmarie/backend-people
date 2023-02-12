from rest_framework.views import APIView    # <- as super to your class
from rest_framework.response import Response  # <- to send data to the frontend
from rest_framework import status # <- to include status codes in your response
from .serializers import PeopleSerializer # <- to format data to and from the database, enforces schema
from .models import Person
from django.shortcuts import render, get_object_or_404


# class (People)

#  GET     /people - index
#  POST    /people - create

# class  (PeopleDetail) - use primary key (pk) as argument to access id

#  GET     /people/:id - show
#  PUT     /people/:id - update
#  DELETE  /people/:id - delete

class People(APIView):

    def get(self, request):
        print(request)
        people = Person.objects.all()
        data = PeopleSerializer(people, many=True).data
        return Response(data)
    
    def post(self, request):
        print(request.data)
        people = PeopleSerializer(data=request.data)
        if people.is_valid():
            people.save()
            return Response(people.data, status=status.HTTP_201_CREATED)
        else:
            return Response(people.errors, status=status.HTTP_400_BAD_REQUEST)

class PeopleDetail(APIView):
    def get(self, request, pk):
        print(request)
        people = get_object_or_404(Person, pk=pk)
        data = PeopleSerializer(people).data
        return Response(data)
    
    def put (self, request, pk):
        print(request)
        people = get_object_or_404(Person, pk=pk)
        updated = PeopleSerializer(people, data=request.data, partial=True)
        if updated.is_valid():
            updated.save()
            return Response(updated.data)
        else:
            return Response(updated.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        print(request)
        people = get_object_or_404(Person, pk=pk)
        people.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)