import json
import requests
import tweepy
import textwrap
from configparser import ConfigParser


def _get_TW_apis_key(description):
    """Fetch the API key from your configuration file.
    Expects a configuration file named "secrets.ini" with structure:
        [twitter]
        api_key=<YOUR-OPENWEATHER-API-KEY>
    """
    config = ConfigParser()
    config.read("secrets.ini")
    return config["twitter"][description]


def tweet_empty_stations(event, context):
    consumer_key = _get_TW_apis_key("consumer_key")
    consumer_secret = _get_TW_apis_key("consumer_secret")

    access_token = _get_TW_apis_key("access_token")
    access_token_secret = _get_TW_apis_key("access_token_secret")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    station_status_url = "https://gbfs.mex.lyftbikes.com/gbfs/es/station_status.json"
    station_information_url = "https://gbfs.mex.lyftbikes.com/gbfs/es/station_information.json"

    number_of_stations = 0
    number_of_working_stations = 0
    number_of_empty_stations = 0
    number_of_available_bikes = 0
    number_of_disabled_bikes = 0
    total_bikes_available = 0
    empty_stations = []

    response = requests.get(station_status_url)
    station_status_data = json.loads(response.text)

    response = requests.get(station_information_url)
    station_information_data = json.loads(response.text)

    # Create a dictionary to map station IDs to station names
    name_dict = {}
    for station in station_information_data['data']['stations']:
        name_dict[station['station_id']] = station['name']

    # Find the station(s) where num_bikes_available is 0
    for station in station_status_data['data']['stations']:
        if station['is_installed'] == 1 and station['is_renting'] == 1:
            number_of_working_stations += 1
            if station['num_bikes_available'] == 0:
                # Print the name of the station
                number_of_empty_stations += 1
                empty_stations.append(name_dict[station['station_id']])
        number_of_available_bikes += station['num_bikes_available']
        number_of_disabled_bikes += station['num_bikes_disabled']

    total_bikes_available = number_of_available_bikes - number_of_disabled_bikes
    number_of_stations = len(station_status_data["data"]["stations"])

    message = "📢 Estatus Ecobici\nTotal estaciones habilitadas: " + \
        str(number_of_working_stations)+"\nTotal estaciones existentes: " + str(number_of_stations) + \
        "\nTotal estaciones habilitadas sin bicicletas: " + \
        str(number_of_empty_stations)+"\nTotal de bicicletas disponibles en estación: " + \
        str(total_bikes_available)+"\n@ecobici @HSBC_MX\n"

    # TODO: Tweet the empty stations

    # message_with_empty_stations = ""

    # for station in empty_stations:
    #    message_with_empty_stations = message_with_empty_stations + station + "\n"

    # tweet_list = textwrap.wrap(
    #    message_with_empty_stations, width=280)

    # count = 0

    # for tweet in tweet_list:
    #    count += 1
    #    print(count)
    #    print(tweet)

    api.update_status(status=message)
    # print(message)


#tweet_empty_stations()
