import json
import folium
import pandas
 
data = pandas.read_csv("application2/Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_producer(elevation):
    if elevation < 1500:
        return 'green'
    elif 1500 <= elevation <3000:
        return 'orange'
    else:
        return 'red'
 
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""
 
map = folium.Map(location=[38.58, -99.09], zoom_start=5, tiles="Stamen Terrain")
fgv = folium.FeatureGroup(name = "Volcanoes")
 
for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=folium.Popup(iframe),
    fill_color=color_producer(el), color = color_producer(el), fill_opacity=0.8))

fgp = folium.FeatureGroup(name = "Population")
fgp.add_child(folium.GeoJson(data=open('application2/world.json', 'r', encoding='utf-8-sig').read(), 
style_function=lambda x: {'fillColor':'yellow' if x['properties']['POP2005'] < 10000000 
else 'red' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'blue'}))

map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl())
map.save("MapUS.html")