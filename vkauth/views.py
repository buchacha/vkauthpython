from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from user.models import UserData
import requests
import vk_api
import json
        
def vkcode(request):
    
    with open('../secure_data.json') as json_file:
	    client_secret = json.load(json_file)['client_secret']

    if 'code' in request.GET.keys():
        code = request.GET['code']
        response = requests.get('https://oauth.vk.com/access_token?'
            + 'client_id=7337548'
            + '&client_secret=' + client_secret 
            + '&code=' + str(code) 
            + '&redirect_uri=http://178.128.152.204:8000/auth/vkcode')
        jsonResponse = response.json()
        if 'access_token' in jsonResponse.keys():
            accessToken = jsonResponse['access_token']
            print(accessToken)
            vk_session = vk_api.VkApi(token=accessToken)
            vk = vk_session.get_api()
            userId = vk.users.get()[0]['id']

            try:
                user = User.objects.get(username=userId)
                auth.login(request, user)
                userData = UserData.objects.get(user=request.user)
                userData.vk_token = accessToken
                userData.save()
            except User.DoesNotExist:
                user = User.objects.create_user(username=userId, password='')
                auth.login(request, user)
                userData = UserData()
                userData.user = request.user
                userData.vk_token = accessToken
                userData.save()
                

            return redirect('/?' + 'auth_status=success')
        return redirect('/?' + 'auth_status=fail fetch access_token')
    return redirect('/?' + 'auth_status=fail fetch code')
        
    
        

    
        
        

    