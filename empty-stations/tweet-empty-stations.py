import json
import requests
import tweepy
import textwrap
from configparser import ConfigParser


def _get_TW_apis_key(description):
    """Fetch the API key from your configuration file.
    Expects a configuration file named "secrets.ini" with structure:
        [twitter]
        consumer_key=
        consumer_secret=
        access_token=
        access_token_secret=
    """
    config = ConfigParser()
    config.read("secrets.ini")
    return config["twitter"][description]


def tweet_empty_stations(event, context):
    consumer_key = _get_TW_apis_key("consumer_key")
    consumer_secret = _get_TW_apis_key("consumer_secret")

    access_token = _get_TW_apis_key("access_token")
    access_token_secret = _get_TW_apis_key("access_token_secret")

    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )


    station_status_url = "https://gbfs.mex.lyftbikes.com/gbfs/es/station_status.json"
    station_information_url = "https://gbfs.mex.lyftbikes.com/gbfs/es/station_information.json"

    number_of_stations = 0
    number_of_working_stations = 0
    number_of_empty_stations = 0
    number_of_available_bikes = 0
    number_of_disabled_bikes = 0
    total_bikes_available = 0
    empty_stations = []
    number_of_stations_with_less_2_bikes = 0
    total_docks_available = 0

    response = requests.get(station_status_url)
    station_status_data = json.loads(response.text)

    response = requests.get(station_information_url)
    station_information_data = json.loads(response.text)

    # Create a dictionary to map station IDs to station names
    name_dict = {}
    for station in station_information_data['data']['stations']:
        name_dict[station['station_id']] = station['name']
        total_docks_available += station['capacity']

    # Find the station(s) where num_bikes_available is 0
    for station in station_status_data['data']['stations']:
        if station['is_installed'] == 1 and station['is_renting'] == 1:
            number_of_working_stations += 1
            if station['num_bikes_available'] == 0:
                # Print the name of the station
                number_of_empty_stations += 1
                empty_stations.append(name_dict[station['station_id']])
            if station['num_bikes_available'] > 0 and station['num_bikes_available'] <= 2:
                number_of_stations_with_less_2_bikes += 1
        number_of_available_bikes += station['num_bikes_available']
        number_of_disabled_bikes += station['num_bikes_disabled']

    total_bikes_available = number_of_available_bikes - number_of_disabled_bikes
    number_of_stations = len(station_status_data["data"]["stations"])

    message = "📢 Estatus Ecobici 🚲\nTotal estaciones habilitadas: " + \
        str(number_of_working_stations)+"\nTotal estaciones existentes: " + str(number_of_stations) + \
        "\nTotal estaciones habilitadas sin bicicletas: " + \
        str(number_of_empty_stations)+"\nTotal de bicicletas disponibles en estación: " + \
        str(total_bikes_available)+"\nTotal de estaciones con <= 2 🚲: " +str(number_of_stations_with_less_2_bikes) + \
        "\nTotal anclajes: " + str(total_docks_available) + "\n@ecobici @HSBC_MX #ecobici\n"

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

    client.create_tweet(text=message)
    # print(message)


#tweet_empty_stations()
