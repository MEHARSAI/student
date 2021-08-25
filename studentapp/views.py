from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView


# Create your views here.
from .serializers import studentSerializer

SUBJECT_LIST = ["english","maths","science"] #List for subjects in the Marksheet model

# Error Messages
INVALID_STUDENT_MESSAGE = "Students in invalid_student_list DoesNotExist!!!"
MARKS_ALREADY_EXISTS_MESSAGE = "Marks have already been entered for students in failure_list"
UNAUTHORIZED_MESSAGE = "You're not authorized!!!"
INVALID_SUBJECT_MESSAGE = "Subject Not Available"

@api_view(['GET'])
def showstudent(request):
    results=Student.objects.all()
    searalize=studentSerializer(results,many=True)
    return Response(searalize.data)

@api_view(['GET', 'POST'])
def list_student(request):
    if request.method == "GET":
        courses = Student.objects.all()
        serializer = studentSerializer(courses, many=True)
        return Response(serializer.data)
    else:  # Post
        serializer = studentSerializer(data=request.data)
        if serializer.is_valid():
            #print(serializer.marks)
            serializer.save()
            return Response(serializer.data, status=201)  # Successful post

        return Response(serializer.errors, status=400)  # Invalid data


class addMarks(APIView):

    def post(self, request, filename, format=None):
        id = request.META['HTTP_TOKEN']
        try:
            course = Student.objects.get()

            f = request.data['file']
            with open('input.pdf', 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            data = {}

            success_list = []
            failure_list = []
            invalid_student_list = []
            messages = []
            for row in range(row_count):
                student_id = data.iloc[row]['student_id']
                try:
                    # print("Student\t\t:{0}".format(student_id))
                    user = User.objects.get(email=student_id, is_teacher=False)
                    grade = data.iloc[row]['grade']
                    english = data.iloc[row]['english']
                    maths = data.iloc[row]['maths']
                    science = data.iloc[row]['science']
                    Student.objects.create(user=user, grade=grade, english=english, maths=maths, science=science)
                except User.DoesNotExist:
                    invalid_student_list.append(student_id)
                    if INVALID_STUDENT_MESSAGE not in messages:
                        messages.append(INVALID_STUDENT_MESSAGE)
                    continue
                except:
                    failure_list.append(student_id)
                    if MARKS_ALREADY_EXISTS_MESSAGE not in messages:
                        messages.append(MARKS_ALREADY_EXISTS_MESSAGE)
                    continue
                success_list.append(student_id)
            data = {}
            data['messages'] = messages
            data['student_list'] = success_list
            data['invalid_student_list'] = invalid_student_list
            data['failure_list'] = failure_list
            if success_list:
                data['success'] = True
                data['marks_entered_by'] = u.email
                return Response(data)
            else:
                data['success'] = False
                return Response(data, status=422)
        except Exception as e:
            print(e)
            data = {}
            data['success'] = False
            data['message'] = UNAUTHORIZED_MESSAGE
            return Response(data, status=403)


class getMarksByGrade(APIView):
    def get(self, request, grade, format=None, studentMarksJSON=None):
        id = request.META['HTTP_TOKEN']
        data = {}
        try:
            u = User.objects.get(id=id, is_teacher=False)
            marks = Student.objects.filter(user=u, grade=grade)
            return studentMarksJSON(marks, u)
        except Exception:
            data['success'] = False
            data['message'] = UNAUTHORIZED_MESSAGE
            return Response(data, status=403)
