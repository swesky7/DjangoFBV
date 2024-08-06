from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from first_app.models import Student
from first_app.serializers import StudentSerializer
from rest_framework.response import Response


# Create your views here.

@api_view(['GET', 'POST'])
def student_list(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        # We create a StudentSerializer instance with the queryset and specify many=True
        # to indicate that we're serializing multiple objects.
        return Response(serializer.data)
        # returning the serialized data as a response to an API request.

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)  # deserializing incoming
        # JSON data into a
        # Django model instance
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def student_detail(request, pk):
    try:
        student = Student.objects.get(pk=pk)  # retreieving single studnet object
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    elif request.method == 'PUT':  # update
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()  # overwrite the data
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
