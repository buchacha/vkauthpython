from django.shortcuts import render, get_object_or_404
import vk_api
from .models import UserData

def home(request):
    if 'auth_status' in request.GET.keys():
        return render(request, 'user/home.html', {'auth_status':request.GET['auth_status']})
    else:
        return render(request, 'user/home.html')

def friends(request):

    curUser = request.user
    try:
        userDataObj = get_object_or_404(UserData, user=curUser)
        vk_session = vk_api.VkApi(token=userDataObj.vk_token)
        vk = vk_session.get_api()

        friendsIds = vk.friends.get()['items'][:5]
        friendsNames = []
        for friendId in friendsIds:
            curFriend = vk.users.get(user_id=friendId)[0]
            friendsNames.append(curFriend['first_name'] + ' ' + curFriend['last_name'])
        return render(request, 'user/friends.html', {'friend_names':friendsNames})
    
    except UserData.DoesNotExist:
        
        return render(request, 'user/friends.html', {'user_token':000})

    return render(request, 'user/friends.html', {'user_token':userDataObj.vk_token})
