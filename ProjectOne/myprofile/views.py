import json
from datetime import datetime

# import pdfkit
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from myprofile.models import MyProfile

from .process import html_to_pdf

# import requests
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.authtoken.models import Token
# from django.db.models import Q
# from .serializers import MyProfileSerializer

# Create your views here.


@api_view(["GET"])
def profiles(request):
    profiles_data = MyProfile.objects.all().order_by("-id")
    response = []
    for data in profiles_data:
        response.append(
            {
                "id": data.id,
                "first_name": data.user.first_name,
                "last_name": data.user.last_name,
                "username": data.user.username,
                "email": data.user.email,
                "phone": data.phone,
                "address": data.address,
            }
        )

    return Response(response)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@permission_required("myprofile.delete_myprofile")
def profile_delete(request):
    id = request.POST["profile_id"]
    MyProfile.objects.filter(id=id).delete()
    return HttpResponse(json.dumps({"code": 1, "msg": "Profile Deleted!"}), content_type="json")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def profile_edit_details(request):
    id = int(request.POST["profile_id"])
    profile_data = MyProfile.objects.filter(id=id).values("id", "phone", "address", "user", "user__first_name", "user__last_name", "user__email")
    response = []
    for data in profile_data:
        response.append(
            {
                "id": data["id"],
                "first_name": data["user__first_name"],
                "last_name": data["user__last_name"],
                "email": data["user__email"],
                "phone": data["phone"],
                "address": data["address"],
                "user_id": data["user"],
            }
        )

    return HttpResponse(json.dumps({"code": 1, "edit_data": response}), content_type="json")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def profile_save(request):
    try:
        id = request.POST["profile_id"]
        user_id = request.POST.get("user_id")
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        phone = int(request.POST["phone"])
        email = request.POST["email"]
        address = request.POST["address"]
        username = request.POST.get("username")
        password = request.POST.get("password")
        response = []

        if (id is None or id == "") and (user_id is None or user_id == ""):
            user_data = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )

            MyProfile.objects.create(phone=phone, address=address, user=user_data)

            return HttpResponse(json.dumps({"code": 1, "msg": "Profile Created!"}), content_type="json")
        else:
            id = int(id)
            user_id = int(user_id)
            MyProfile.objects.filter(id=id, user=user_id).update(
                id=id,
                phone=phone,
                address=address,
            )

            User.objects.filter(id=user_id).update(
                id=user_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )

            return HttpResponse(json.dumps({"code": 1, "msg": "Profile updated!"}), content_type="json")
    except Exception:

        return HttpResponse(json.dumps({"code": 0, "msg": "Something went Wrong!"}), content_type="json")


@api_view(["POST"])
def profile_authentication(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    response = []

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        response.append({"msg_code": 1, "message": "You are authenticated!", "user": username})
        return Response(response)
    else:
        response.append({"msg_code": 0, "message": "Authentication failed! Try again!"})
        return Response(response)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    username = request.POST.get("username")
    old_password = request.POST.get("old_password")
    new_password = request.POST.get("new_password")

    user = authenticate(username=username, password=old_password)
    if user is not None:
        user = User.objects.get(id=user.id)
        user.set_password(new_password)
        user.save()
        return HttpResponse(json.dumps({"code": 1, "msg": "Password changed successfully!"}), content_type="json")
    else:
        return HttpResponse(json.dumps({"code": 0, "msg": "Try again with valid username"}), content_type="json")


class GeneratePdf(APIView):
    # permission_classes = ["IsAuthenticated"]

    def get(request, *args, **kwargs):
        # getting the template
        pdf = html_to_pdf("myprofile/print_profile.html")
        print("pdf", pdf)

        # rendering the template
        return HttpResponse(pdf, content_type="application/pdf")


# @api_view(["GET"])
# def pdf_img(request):

#     # Create the HttpResponse object
#     response = HttpResponse(content_type="application/pdf")

#     # This line force a download
#     response["Content-Disposition"] = 'attachment; filename="1.pdf"'

#     # READ Optional GET param
#     # get_param = request.GET.get("name", "World")

#     # Generate unique timestamp
#     ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

#     p = canvas.Canvas(response)

#     # Write content on the PDF
#     p.drawString(100, 500, "Hello world " + " (Dynamic PDF) - " + ts)

#     # Close the PDF object.
#     p.showPage()
#     p.save()

#     # Show the result to the user
#     return response


# def make_pdf(request, id):
#     print("id", id)
#     # profile_data = MyProfile.objects.filter(id=id).values("id", "phone", "address", "user", "user__first_name", "user__last_name", "user__email")
#     # print("profile_data", profile_data)

#     # getting the template
#     html_to_pdf("http://127.0.0.1:8000/print_profile/")

#     # rendering the template
#     # return HttpResponse(pdf, content_type="application/pdf")

#     # html = loader.render_to_string("http://127.0.0.1:8000/print_profile/", {"profile_data": profile_data})
#     # print("html", html)
#     # output = pdfkit.from_string(html, output_path=False)
#     # print("output", output)
#     # response = HttpResponse(content_type="application/pdf")
#     # print("response", response)
#     # response.write(output)
#     return HttpResponse(json.dumps({"code": 1, "msg": "success"}), content_type="json")
# return response


# @api_view(["POST"])
# def profile_search(request):
#     query = Q()
#     first_name = request.POST["first_name"]
#     last_name = request.POST["last_name"]
#     username = request.POST["username"]
#     email = request.POST["email"]
#     response = []

#     if first_name != "" or first_name is not None:
#         query.add(Q(user__first_name__icontains=str(first_name)), query.connector)
#     if last_name != "" or last_name is not None:
#         query.add(Q(user__last_name__icontains=str(last_name)), query.connector)
#     if username != "" or username is not None:
#         query.add(Q(user__username__icontains=str(username)), query.connector)
#     if email != "" or email is not None:
#         query.add(Q(user__email__icontains=str(email)), query.connector)

#     profiles_data = MyProfile.objects.filter(query).order_by("-id")

#     for data in profiles_data:
#         print("data", data)
#         response.append(
#             {
#                 "id": data.id,
#                 "first_name": data.user.first_name,
#                 "last_name": data.user.last_name,
#                 "username": data.user.username,
#                 "email": data.user.email,
#                 "phone": data.phone,
#                 "address": data.address,
#             }
#         )

#     return Response(response)
