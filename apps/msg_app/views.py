from django.shortcuts import render, HttpResponse, redirect
from ..user_app.models import *

# the index function is called when root is visited
def message(request, user_id):

    print "in message view, user_id: ",user_id

    this_user = User.objects.get(id=user_id)

    msgs = Msg.objects.filter(to_user=this_user)

    context = {
        'user' : this_user,
        'msgs' : msgs
    }

    return render(request, "msg_app/message.html",context)
