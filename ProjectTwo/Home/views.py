import json

import requests
from django.http import HttpResponse
from django.shortcuts import render

# # Create your views here.


def home(request):
    url = "http://192.168.1.249:7001/profiles/"
    data = requests.get(url, data={}, verify=False)
    data = data.json()
    return render(request, "home/home.html", {"data": data})


def login_user(request):
    return render(request, "home/login.html")


def print_profile(request):
    print(request.POST)
    return render(request, "Home/print_profile.html")


def change_password(request):
    return render(request, "home/change_password.html")


# def search_profile(request):
#     url = "http://192.168.1.249:7001/profile_search/"
#     response = requests.post(
#         url,
#         data={
#             "username": request.POST.get("username"),
#             "first_name": request.POST.get("first_name"),
#             "last_name": request.POST.get("last_name"),
#             "email": request.POST.get("email"),
#         },
#     )

#     response = response.json()

#     return HttpResponse(json.dumps({"code": 1, "data": response}), content_type="json")


# def delete_profile(request):
#     url = "http://192.168.1.249:7001/profile_delete/"
#     response = requests.post(url, data={"id": int(request.POST.get("profile_id"))}, verify=False)
#     response = response.json()
#     response = response[0]

#     return HttpResponse(json.dumps({"code": 1, "msg": response["message"]}), content_type="json")


# def get_edit_profile(request):
#     url = "http://192.168.1.249:7001/profile_edit_details/"
#     data = requests.post(url, data={"id": int(request.POST.get("profile_id"))}, verify=False)
#     edit_data = data.json()
#     edit_data = edit_data[0]
#     return HttpResponse(json.dumps({"code": 1, "msg": "Profile Details Fetched", "edit_data": edit_data}), content_type="json")


# def save_profile(request):
#     if request.method == "POST":
#         url = "http://192.168.1.249:7001/profile_save/"
#         response = requests.post(
#             url,
#             data={
#                 "id": int(request.POST.get("profile_id")) if request.POST.get("profile_id") else "",
#                 "user_id": int(request.POST.get("user_id")) if request.POST.get("user_id") else "",
#                 "username": request.POST.get("username") if request.POST.get("username") else "",
#                 "password": request.POST.get("password") if request.POST.get("password") else "",
#                 "first_name": request.POST.get("first_name"),
#                 "last_name": request.POST.get("last_name"),
#                 "phone": request.POST.get("phone"),
#                 "email": request.POST.get("email"),
#                 "address": request.POST.get("address"),
#             },
#             verify=False,
#         )

#         response = response.json()
#         response = response[0]
#         print("response", response)

#         return HttpResponse(json.dumps({"code": response["msg_code"], "msg": response["message"]}), content_type="json")
#     else:
#         return HttpResponse(json.dumps({"code": 0, "msg": "Try again"}), content_type="json")


# def authenticate_profile(request):
#     url = "http://192.168.1.249:7001/profile_authentication/"
#     response = requests.post(
#         url,
#         data={
#             "username": request.POST.get("username"),
#             "password": request.POST.get("password"),
#         },
#         verify=False,
#     )
#     response = response.json()
#     response = response[0]

#     print("response", response)

#     return HttpResponse(json.dumps({"code": response["msg_code"], "msg": response["message"]}), content_type="json")


# # def logout(request):
# #     print(request.session)

# #     return HttpResponse(json.dumps({"code": 1, "msg": "logout"}), content_type="json")
