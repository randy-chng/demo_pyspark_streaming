import socket
import requests
import requests_oauthlib
import json
import yaml


def get_tweets():

    my_auth = requests_oauthlib.OAuth1(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_TOKEN,
        ACCESS_SECRET
    )

    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    query_data = [('language', 'en'), ('locations', '-74,40,-73,41'), ('track', '#')]
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])

    response = requests.get(
        query_url,
        auth=my_auth,
        stream=True
    )

    print(query_url, response)

    return response


def send_tweets_to_spark(http_resp, tcp_connection):

    for line in http_resp.iter_lines():

        try:
            if len(line) != 0:
                full_tweet = json.loads(line)
                tweet_text = full_tweet['text']
                print("Tweet Text:", tweet_text)
                print("------------------------------------------")

                tcp_connection.send(str.encode(tweet_text + '\n'))

        except Exception as e:
            print('Error:', e)


if __name__ == "__main__":

    with open('config.yaml', 'r') as stream:
        details = yaml.safe_load(stream)

    TCP_IP = details['host']
    TCP_PORT = details['port']

    ACCESS_TOKEN = details['access_token']
    ACCESS_SECRET = details['access_secret']
    CONSUMER_KEY = details['consumer_key']
    CONSUMER_SECRET = details['consumer_secret']

    conn = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    print('Waiting for TCP connection...')
    conn, addr = s.accept()

    print('Connected... Starting getting tweets.')
    resp = get_tweets()
    send_tweets_to_spark(resp, conn)
