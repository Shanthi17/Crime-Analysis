from bokeh.plotting import gmap
from bokeh.models import GMapOptions
from bokeh.models import HoverTool
import os
# import config



def plot_map(df, lat, lng, zoom = 11, map_type = 'roadmap'):
    bokeh_width, bokeh_height = 1000,800
    lat, lng = 39.7392, -104.9903
    api_key = os.environ['api_key']
    attributes = list(df.columns)
    attribute_list = []
    for item in attributes:
        appended_string = '@'+item
        attribute_list.append((item,appended_string))
    hover = HoverTool(tooltips = attribute_list)
    gmap_options = GMapOptions(lat=lat, lng=lng, map_type=map_type, zoom=zoom)
    p = gmap(api_key, gmap_options, title='Denver', width=bokeh_width, height=bokeh_height, 
                tools=[hover, 'reset', 'wheel_zoom', 'pan'])
    

    center = p.circle('GEO_LON', 'GEO_LAT', size=10, alpha=0.5, color='red', source=df)

    # show(p)
    return p




