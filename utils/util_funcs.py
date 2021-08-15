import requests
import os
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
print(dotenv_path)
load_dotenv(dotenv_path)


def get_headers():
    return {'Authorization': 'Bearer {access_token}'.format(
        access_token=os.environ['BEARER_TOKEN'])}


def get_twitter_v1_request():
    from requests_oauthlib import OAuth1Session
    twitter = OAuth1Session(os.environ.get('CONSUMER_API_KEY'),
                            client_secret=os.environ.get('CONSUMER_SECRET'),
                            resource_owner_key=os.environ.get('ACCESS_TOKEN'),
                            resource_owner_secret=os.environ.get('TOKEN_SECRET'))
    return twitter


def get_followers():
    followers = []
    count = 1

    print('Fetching page {page}'.format(page=count))
    r = requests.get(
        'https://api.twitter.com/2/users/{my_id}/followers'.format(my_id=os.environ['MY_ID']), headers=get_headers())
    result = r.json()
    followers = followers + result['data']

    while "next_token" in result['meta']:
        next_token = result['meta']['next_token']
        count = count + 1
        print('Fetching page {page}'.format(page=count))

        r = requests.get(
            'https://api.twitter.com/2/users/{my_id}/followers?pagination_token={next_token}'.format(my_id=os.environ['MY_ID'], next_token=next_token), headers=get_headers())
        result = r.json()

        followers = followers + result['data']
        next_token = result['meta']['next_token']

    print('There are {followers_length} followers'.format(
        followers_length=len(followers)))
    return followers


def get_followings():
    followings = []
    count = 1

    print('Fetching page {page}'.format(page=count))
    r = requests.get(
        'https://api.twitter.com/2/users/{my_id}/following'.format(my_id=os.environ['MY_ID']), headers=get_headers())
    result = r.json()
    followings = followings + result['data']

    while "next_token" in result['meta']:
        next_token = result['meta']['next_token']
        count = count + 1
        print('Fetching page {page}'.format(page=count))

        r = requests.get(
            'https://api.twitter.com/2/users/{my_id}/following?pagination_token={next_token}'.format(my_id=os.environ['MY_ID'], next_token=next_token), headers=get_headers())
        result = r.json()

        followings = followings + result['data']
        next_token = result['meta']['next_token']

    print('There are {followings_length} followings'.format(
        followings_length=len(followings)))
    return followings


def get_who_never_follow_back(following=[], followers=[]):
    result = []
    follower_names = list(map(lambda x: x['id'], followers))
    for user in following:
        if user['id'] not in follower_names:
            result.append(user)
    return result


def get_whom_i_never_follow_back(following=[], followers=[]):
    result = []
    following_names = list(map(lambda x: x['id'], following))
    for user in followers:
        if user['id'] not in following_names:
            result.append(user)
    return result


def unfollow_user(username, user_id):
    request_v1 = get_twitter_v1_request()
    request_v1.post(
        'https://api.twitter.com/1.1/friendships/destroy.json?user_id={user_id}'.format(user_id=user_id))
    print("Successfully unfollow {username}".format(username=username))


def follow_user(username, user_id):
    request_v1 = get_twitter_v1_request()
    request_v1.post(
        'https://api.twitter.com/1.1/friendships/create.json?user_id={user_id}'.format(user_id=user_id))
    print("Successfully follow {username}".format(username=username))
