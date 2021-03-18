from django.shortcuts import render

# Create your views here.
from django.conf import settings
import requests
import json
from django.shortcuts import render
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse, JsonResponse
import slack

def index(request):
    client_id = settings.SLACK_CLIENT_ID
    return render(request, 'web/landing.html', {'client_id': client_id})

def slack_oauth(request):
    code = request.GET['code']
    print(code)
    params = {
        'code': code,
        'client_id': settings.SLACK_CLIENT_ID,
        'client_secret': settings.SLACK_CLIENT_SECRET
    }
    url = 'https://slack.com/api/oauth.access'
    json_response = requests.get(url, params)
    data = json.loads(json_response.text)
    print("--Data---")
    print(data)

    return HttpResponse('Bot added to your Slack team!')


@csrf_exempt
def event_hook(request):
    client = slack.WebClient(token=settings.BOT_USER_ACCESS_TOKEN)
    json_dict = json.loads(request.body.decode('utf-8'))
    if json_dict['token'] != settings.VERIFICATION_TOKEN:
        return HttpResponse(status=403)
    if 'type' in json_dict:
        if json_dict['type'] == 'url_verification':
            response_dict = {"challenge": json_dict['challenge']}
            return JsonResponse(response_dict, safe=False)
    if 'event' in json_dict:
        event_msg = json_dict['event']
        if 'bot_id' in event_msg:
            return HttpResponse(status=200)
    if event_msg['type'] == 'message':
        user = event_msg['user']
        channel = event_msg['channel']
        response_msg = ":wave:, Hello <@%s>" % user
        client.chat_postMessage(channel=channel, text=response_msg)
        return HttpResponse(status=200)
    return HttpResponse(status=200)

def get_list_of_users():
    client  = slack.WebClient(token=settings.BOT_USER_ACCESS_TOKEN)
    users = client.api_call("users.list")
    if users.get('ok'):
        return users['members']

def send_message_member(response_msg):
    client  = slack.WebClient(token=settings.BOT_USER_ACCESS_TOKEN)
    users = get_list_of_users()
    if users:
        for user in users:
            if user['is_bot'] == False:
                print(user['real_name'])
                client.chat_postMessage(channel=user['id'], text=response_msg)