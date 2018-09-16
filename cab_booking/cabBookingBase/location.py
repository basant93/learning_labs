import requests

#address = "1600 Amphitheatre Parkway, Mountain View, CA"
origin = 'Washington,DC'
destinations ='New+York+City,NY'
api_key = 'AIzaSyCiNWrfTbzFxxle_OkQfl5mwwoKtDG8_MM'
#api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
#api_response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origin={0}&destinations={1}&key={2}'.format(origin, destinations,api_key))
#api_response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origin={0}&destinations={1}&key={2}'.format(origin, destinations,api_key))
api_response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=40.6655101,-73.89188969999998&destinations=40.6905615%2C-73.9976592&key=AIzaSyCiNWrfTbzFxxle_OkQfl5mwwoKtDG8_MM')
api_response_dict = api_response.json()

if api_response_dict['status'] == 'OK':
    distance = api_response_dict['rows'][0]['elements'][0]['distance']['text']
    duration = api_response_dict['rows'][0]['elements'][0]['duration']['text']

    print ('Latitude:', distance)
    print ('Longitude:', duration)