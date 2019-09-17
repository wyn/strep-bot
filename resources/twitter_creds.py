import json

# Enter your keys/secrets as strings in the following fields
credentials = {}
credentials['CONSUMER_KEY'] = "CONSUMER_KEY"
credentials['CONSUMER_SECRET'] = "CONSUMER_SECRET"
credentials['ACCESS_TOKEN'] = "ACCESS_TOKEN"
credentials['ACCESS_SECRET'] = "ACCESS_SECRET"

if __name__ == '__main__':
    # Save the credentials object to file
    with open("twitter_credentials.json", "w") as f:
        json.dump(credentials, f)
