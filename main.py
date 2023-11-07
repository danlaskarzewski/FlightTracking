import requests
import time
import json
import pandas as pd
import folium

def main():
    request_airport(0)
    # lat = 29.5337
    # lon = -98.469 
    # m = folium.Map(location=[lat, lon], zoom_start=9)
    # m.save("TEST.HTML")


def request_airport(interval):
    root_url = 'https://opensky-network.org/api'
    airport_code = 'KSAT'
    print(str(int(time.time())))
    start_time = int(time.time() - (30*60))     #15 mins ago
    end_time = int(time.time() + (60*60))       #30 mins from now
    arrival_data = '/flights/arrival?airport='+airport_code+'&begin='+str(start_time)+'&end='+str(end_time)
    arr_url = root_url + arrival_data
    print(arr_url)
#https://opensky-network.org/api/flights/arrival?airport=EDDF&begin=1517227200&end=1517230800
#https://opensky-network.org/api/flights/arrival?airport=KSAT&begin=1697412692&end=1697415392
    r = requests.get(arr_url)
    if r.status_code != 200:
        print(r)
    else:
        print(r.content)

def request():
    root_url = 'https://opensky-network.org/api'
    lat = 29.5337
    lon = -98.469 
    lamin = lat - .5
    lomin = lon - .5
    lamax = lat + .5
    lomax = lon + .5

    geo_data = '/states/all?lamin='+str(lamin)+'&lomin='+str(lomin)+'&lamax='+str(lamax)+'&lomax='+str(lomax)

    airport_code = 'KSAT'
    start_time = time.time() - (15*60)  #15 mins ago
    end_time = time.time() + (30*60)    #30 mins from now
    arrival_data = '/flights/arrival?airport='+airport_code+'&begin='+str(start_time)+'&end='+str(end_time)

    geo_url = root_url + geo_data
    arr_url = root_url + arrival_data

    r = requests.get(geo_url)
    # r = {"time":1697322885,"states":[["a4ab4a","N40LH   ","United States",1697322884,1697322884,-98.1529,30.0115,975.36,false,89.98,107.3,-1.63,null,1066.8,null,false,0],["aa2abc","AAL2348 ","United States",1697322884,1697322884,-98.0565,29.8152,3169.92,false,153.1,236.79,-6.83,null,3322.32,"3447",false,0],["0d0ccc","XAOAV   ","Mexico",1697322884,1697322884,-98.2926,29.5691,1775.46,false,114.81,219.18,0.65,null,1866.9,"4615",false,0],["a9eda4","N739MY  ","United States",1697322826,1697322837,-98.4204,29.2787,518.16,false,49.68,328.12,-0.33,null,548.64,null,false,0],["a1fff2","ENY3601 ","United States",1697322884,1697322884,-98.3043,29.0815,10668,false,233.57,346.24,0,null,11330.94,null,false,0],["a7c77c","N600CL  ","United States",1697322884,1697322884,-98.4191,29.963,10332.72,false,256.33,6.57,6.18,null,10949.94,"2473",false,0],["0d080e","SLI2686 ","Mexico",1697322884,1697322884,-98.4474,29.3265,7315.2,false,221.41,18.56,-0.33,null,7726.68,null,false,0],["abefc8","N8686Q  ","United States",1697322884,1697322884,-98.5398,29.6387,1615.44,false,61.36,86.15,0,null,1722.12,null,false,0],["aa13cd","N74882  ","United States",1697322883,1697322883,-98.6953,29.7297,null,true,2.31,90,null,null,null,null,false,0],["a14845","N182BT  ","United States",1697322731,1697322731,-98.0518,29.6843,365.76,false,39.61,90,-4.23,null,388.62,null,false,0],["a00562","N100GZ  ","United States",1697322762,1697322762,-98.4813,29.5117,289.56,false,56.77,43.53,-2.93,null,320.04,null,false,0],["a062ef","DAL2285 ","United States",1697322884,1697322884,-98.2699,29.6085,1493.52,false,140.76,79.47,4.55,null,1577.34,null,false,0],["a12378","UAL1166 ","United States",1697322884,1697322884,-98.1523,29.3786,11269.98,false,276.33,83.8,0,null,11948.16,null,false,0],["a2ecec","ENY3617 ","United States",1697322884,1697322884,-98.5953,29.3682,10363.2,false,214.61,203,0,null,11018.52,"2247",false,0]]}
    if r.status_code != 200:
        print(r)
        
    else:
        columns = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'longitude', 'latitude', 'baro_altitude', 'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source']
                    # ['a3472f', 'DAL1575 ', 'United States', 1697333940, 1697333940,         -98.5004, 29.4922,          419.1,          False,          67.35,      42.83,      -2.6,           None,       472.44,         None, False, 0]
        rjson = json.loads(r.content)

        plane_loc_data = pd.DataFrame(rjson['states'], columns=columns)
        print(plane_loc_data)


        m = folium.Map(location=[lat, lon], zoom_start=13)



if __name__ == "__main__":
    main()




