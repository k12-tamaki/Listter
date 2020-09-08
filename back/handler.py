import json
import tweepy
import os

def _set_token(access_token, secret):
    ''' set twitter token '''

    CK = os.environ['CONSUMER_KEY']
    CS = os.environ['CONSUMER_SECRET']
    # AT = os.environ['ACCESS_TOKEN']
    # AS = os.environ['ACCESS_TOKEN_SECRET']
    AT = access_token
    AS = secret

    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    return tweepy.API(auth)

def get_me(event, context):
    try:
        access_token = event['headers']['x-access-token']
        secret = event['headers']['x-secret']

        api = _set_token(access_token, secret)
        my_info = api.me()

        response = {
            'name': my_info.name,
            'screen_name': my_info.screen_name,
            'profile_image': my_info.profile_image_url,
        }

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response, ensure_ascii=False)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(e, ensure_ascii=False)
        }

def get_follow(event, context):
    try:
        access_token = event['headers']['x-access-token']
        secret = event['headers']['x-secret']

        api = _set_token(access_token, secret)
        my_info = api.me()

        follows = []

        friends_ids = []
        for friend_id in tweepy.Cursor(api.friends_ids, user_id=my_info.id).items():
            friends_ids.append(friend_id)

        for i in range(0, len(friends_ids), 100):
            for user in api.lookup_users(user_ids=friends_ids[i:i+100]):
                follows.append({
                    'id_str': user.id_str,
                    'name': user.name,
                    'screen_name': user.screen_name,
                    'profile_image': user.profile_image_url,
                    'lists': []
                })

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(follows, ensure_ascii=False)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(e, ensure_ascii=False)
        }

def get_list(event, context):
    try:
        access_token = event['headers']['x-access-token']
        secret = event['headers']['x-secret']

        api = _set_token(access_token, secret)
        my_info = api.me()

        twitter_lists = []

        for twitter_list in api.lists_all(user_id=my_info.id):

            users = []
            for user in api.list_members(list_id=twitter_list.id_str):
                users.append({
                    'id_str': user.id_str,
                    'name': user.name,
                    'screen_name': user.screen_name,
                    'profile_image': user.profile_image_url
                })

            twitter_lists.append({
                'id_str': twitter_list.id_str,
                'name': twitter_list.name,
                'users': users
            })

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(twitter_lists, ensure_ascii=False)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(e, ensure_ascii=False)
        }

def post_list(event, context):
    try:
        access_token = event['headers']['x-access-token']
        secret = event['headers']['x-secret']

        api = _set_token(access_token, secret)

        name = event['body']['name']
        description = event['body']['description']
        mode = event['body']['mode']

        # リスト追加
        new_list = api.create_list(name=name, mode=mode, description=description)
        response = {
            'id_str': new_list.id_str,
            'name': new_list.name,
            'users': []
        }

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response, ensure_ascii=False)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(e, ensure_ascii=False)
        }

def delete_list(event, context):
    try:
        access_token = event['headers']['x-access-token']
        secret = event['headers']['x-secret']

        api = _set_token(access_token, secret)

        id = event['body']['id']

        # リスト削除
        delete_list = api.destroy_list(list_id=id)
        response = {
            'id_str': delete_list.id_str
        }

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response, ensure_ascii=False)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(e, ensure_ascii=False)
        }

def post_list_members(event, context):
    try:
        access_token = event['headers']['x-access-token']
        secret = event['headers']['x-secret']

        api = _set_token(access_token, secret)

        # テストデータ
        # list_id = '1287292676048449536'
        # user_ids = '949438177,341374118,249489751,4138421,114373430,996871'.split(',')

        list_id = event['body']['list_id']
        user_ids = event['body']['user_ids']

        # 対象リストのデータを削除
        member_ids = [m.id_str for m in api.list_members(list_id=list_id)]
        delete_member_ids = list(set(member_ids) - set(user_ids))
        for i in range(0, len(delete_member_ids), 100):
            api.remove_list_members(list_id=list_id, user_id=delete_member_ids[i:i+100])

        # リストの追加
        add_user_ids = list(set(user_ids) - set(member_ids))
        for i in range(0, len(add_user_ids), 100):
            api.add_list_members(list_id=list_id, user_id=add_user_ids[i:i+100])

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(e, ensure_ascii=False)
        }

def hello(event, context):
    body = {
        'message': 'Go Serverless v1.0! Your function executed successfully!',
        'input': event
    }

    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    '''
    return {
        'message': 'Go Serverless v1.0! Your function executed successfully!',
        'event': event
    }
    '''
