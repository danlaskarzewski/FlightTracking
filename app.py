import os
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import folium
import requests, time, json
import pandas as pd

app = Dash(__name__)

def post(text, files="", type="auto"):
    hook = "https://discord.com/api/webhooks/1163269569138409492/MwqKdATcjr_fOZY6jXcZRx6Q-L6DSWaAXSr41ePMD8-RGnCYOa1hzdAbeqUBHrSrVa20"
    payload = {"content": text,
               "username" : "PLANE APP",
               "avatar_url" : r"https://media.istockphoto.com/id/1414160809/vector/airplane-icon-plane-flight-pictogram-transport-symbol-travel.jpg?s=1024x1024&w=is&k=20&c=2R8H_YGkkMEbbFn6Ns_OtZcsEeOlau5C0i1TcLIPsBc="
               }
    
    if files == "":
        files1 = {'payload_json': (None, json.dumps(payload))} # None in this tuple sets no filename and is needed to send the text
    else: 
        files1 = {
        'payload_json': (None, json.dumps(payload)), # None in this tuple sets no filename and is needed to send the text
        'media': files
        }

    response = requests.post(hook, files=files1)
    # print(response.status_code)
    # print(response.content)

@app.callback(Output('map', 'srcDoc'),
              Input('interval-component', 'n_intervals'))
def request_map(interval):
    root_url = 'https://opensky-network.org/api'
    lat = 29.4437
    lon = -98.469 
    lamin = lat - .5
    lomin = lon - .5
    lamax = lat + .5
    lomax = lon + .5
    
    home_lat = 29.439843
    home_lon =  -98.797659
    km_deg = .01
    distance = 5*km_deg


    geo_data = '/states/all?lamin='+str(lamin)+'&lomin='+str(lomin)+'&lamax='+str(lamax)+'&lomax='+str(lomax)
    geo_url = root_url + geo_data

    r = requests.get(geo_url)
    if r.status_code != 200:
        print(r)
        
    else:
        columns = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'longitude', 'latitude', 'baro_altitude', 'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source']
                    # ['a3472f', 'DAL1575 ', 'United States', 1697333940, 1697333940,         -98.5004, 29.4922,          419.1,          False,          67.35,      42.83,      -2.6,           None,       472.44,         None, False, 0]
        rjson = json.loads(r.content)

        plane_loc_data = pd.DataFrame(rjson['states'], columns=columns)
        # print(plane_loc_data)


        m = folium.Map(location=[lat, lon], zoom_start=11)

        home_box = folium.Rectangle(
                bounds=[[home_lat-distance, home_lon-distance], [home_lat+distance, home_lon+distance]],
                fill=True,
                fill_color='red',
                weight=1,
                ).add_to(m)

        for index, plane in plane_loc_data.iterrows():
            if int(plane['true_track']) < 90:
                angle = int(plane['true_track']) +270
            else: angle = int(plane['true_track']) -90

            if plane['on_ground']:
                icon = folium.Icon(prefix='fa', icon='plane', angle=int(angle), color="lightgray")
            elif plane['latitude'] <= home_lat+distance and plane['latitude'] >= home_lat-distance and plane['longitude'] <= home_lon+distance and plane['longitude'] >= home_lon-distance:
                icon = folium.Icon(prefix='fa', icon='plane', angle=int(angle), color="orange")
                post(f"Plane overhead at altitude {plane['baro_altitude']} with callsign {plane['callsign']}\b.")
            else: icon = folium.Icon(prefix='fa', icon='plane', angle=int(angle), color="blue")
            marker = folium.Marker(location = [plane['latitude'], plane['longitude']], icon=icon, popup=(f"callsign {plane['callsign']}\nangle {plane['true_track']}\naltitude {plane['baro_altitude']}"))
            marker.add_to(m)

        try:
            os.remove('map.html')
        except OSError:
            pass

        m.save('map.html')
        return open('map.html', 'r').read()  


# @app.callback(Output('map', 'srcDoc'),
#               Input('interval-component', 'n_intervals'))
# def request_airport(interval):
#     root_url = 'https://opensky-network.org/api'
#     airport_code = 'KSAT'
#     start_time = time.time() - (15*60)  #15 mins ago
#     end_time = time.time() + (30*60)    #30 mins from now
#     arrival_data = '/flights/arrival?airport='+airport_code+'&begin='+str(start_time)+'&end='+str(end_time)

#     arr_url = root_url + arrival_data



app.layout = html.Div([
    html.H1('SATX Plane Trackings'),
    html.Div(id='arr-dep-text'),
    html.Iframe(id='map', srcDoc=open('map.html', 'r').read(), width='100%', height='600'),
    dcc.Interval(
            id='interval-component',
            interval=100000, # in milliseconds
            n_intervals=0
        )
])

if __name__ == '__main__':
    app.run_server(debug=True)