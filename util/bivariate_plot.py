
import pandas as pd
import numpy as np
import math
import plotly.graph_objs as go
import json
import geopandas as gpd

"""
Function to set default variables
"""

def conf_defaults():
    # Define some variables for later use
    conf = {
        'plot_title': 'Bivariate choropleth map using Ploty',  # Title text
        'plot_title_size': 20,  # Font size of the title
        'width': 1000,  # Width of the final map container
        'ratio': 0.8,  # Ratio of height to width
        'center_lat': 0,  # Latitude of the center of the map
        'center_lon': 0,  # Longitude of the center of the map
        'map_zoom': 3,  # Zoom factor of the map
        'hover_x_label': 'Label x variable',  # Label to appear on hover
        'hover_y_label': 'Label y variable',  # Label to appear on hover
        'borders_width': 0.5,  # Width of the geographic entity borders
        'borders_color': '#f8f8f8',  # Color of the geographic entity borders

        # Define settings for the legend
        'top': 1,  # Vertical position of the top right corner (0: bottom, 1: top)
        'right': 1,  # Horizontal position of the top right corner (0: left, 1: right)
        'box_w': 0.04,  # Width of each rectangle
        'box_h': 0.04,  # Height of each rectangle
        'line_color': '#f8f8f8',  # Color of the rectagles' borders
        'line_width': 0,  # Width of the rectagles' borders
        'legend_x_label': 'Higher x value',  # x variable label for the legend 
        'legend_y_label': 'Higher y value',  # y variable label for the legend
        'legend_font_size': 9,  # Legend font size
        'legend_font_color': '#333',  # Legend font color
    }

    # Calculate height
    conf['height'] = conf['width'] * conf['ratio']
    
    return conf


"""
Function to recalculate values in case width is changed
"""
def recalc_vars(new_width, variables, conf=conf_defaults()):
    
    # Calculate the factor of the changed width
    factor = new_width / 1000
    
    # Apply factor to all variables that have been passed to the function
    for var in variables:
        if var == 'map_zoom':
            # Calculate the zoom factor
            # Mapbox zoom is based on a log scale. map_zoom needs to be set 
            # to value ideal for our map at 1000px.
            # So factor = 2 ^ (zoom - map_zoom) and zoom = log(factor) / log(2) + map_zoom
            conf[var] = math.log(factor) / math.log(2) + conf[var]
        else:
            conf[var] = conf[var] * factor

    return conf


"""
Function that assigns a value (x) to one of three bins (0, 1, 2).
The break points for the bins can be defined by break_1 and break_2.
"""

def set_interval_value(x, break_1, break_2):
    if x <= break_1: 
        return 0
    elif break_1 < x <= break_2: 
        return 1
    else: 
        return 2


"""
Function that adds a column 'biv_bins' to the dataframe containing the 
position in the 9-color matrix for the bivariate colors
    
Arguments:
    df: Dataframe
    x: Name of the column containing values of the first variable
    y: Name of the column containing values of the second variable

"""

def prepare_df(df, x='x', y='y'):
    
    # Check if arguments match all requirements
    if df[x].shape[0] != df[y].shape[0]:
        raise ValueError('ERROR: The list of x and y coordinates must have the same length.')
    
    # qua
    # Calculate break points at percentiles 33 and 66
    x_breaks = np.percentile(df[x], [33, 66])
    y_breaks = np.percentile(df[y], [33, 66])
    
    # Assign values of both variables to one of three bins (0, 1, 2)
    x_bins = [set_interval_value(value_x, x_breaks[0], x_breaks[1]) for value_x in df[x]]
    y_bins = [set_interval_value(value_y, y_breaks[0], y_breaks[1]) for value_y in df[y]]
    
    # Calculate the position of each x/y value pair in the 9-color matrix of bivariate colors
    df['biv_bins'] = [int(value_x + 3 * value_y) for value_x, value_y in zip(x_bins, y_bins)]
    
    return df
   


"""
Function to create a color square containig the 9 colors to be used as a legend
"""

def create_legend(fig, colors, conf=conf_defaults()):
    
    # Reverse the order of colors
    legend_colors = colors[:]
    legend_colors.reverse()

    # Calculate coordinates for all nine rectangles
    coord = []

    # Adapt height to ratio to get squares
    width = conf['box_w']
    height = conf['box_h']/conf['ratio']
    
    # Start looping through rows and columns to calculate corners the squares
    for row in range(1, 4):
        for col in range(1, 4):
            coord.append({
                'x0': round(conf['right']-(col-1)*width, 4),
                'y0': round(conf['top']-(row-1)*height, 4),
                'x1': round(conf['right']-col*width, 4),
                'y1': round(conf['top']-row*height, 4)
            })

    # Create shapes (rectangles)
    for i, value in enumerate(coord):
        # Add rectangle
        fig.add_shape(go.layout.Shape(
            type='rect',
            fillcolor=legend_colors[i],
            line=dict(
                color=conf['line_color'],
                width=conf['line_width'],
            ),
            xref='paper',
            yref='paper',
            xanchor='right',
            yanchor='top',
            x0=coord[i]['x0'],
            y0=coord[i]['y0'],
            x1=coord[i]['x1'],
            y1=coord[i]['y1'],
        ))
    
        # Add text for first variable
        fig.add_annotation(
            xref='paper',
            yref='paper',
            xanchor='left',
            yanchor='top',
            x=coord[8]['x1'],
            y=coord[8]['y1'],
            showarrow=False,
            text=conf['legend_x_label'] + ' 🠒',
            font=dict(
                color=conf['legend_font_color'],
                size=conf['legend_font_size'],
            ),
            borderpad=0,
        )
        
        # Add text for second variable
        fig.add_annotation(
            xref='paper',
            yref='paper',
            xanchor='right',
            yanchor='bottom',
            x=coord[8]['x1'],
            y=coord[8]['y1'],
            showarrow=False,
            text=conf['legend_y_label'] + ' 🠒',
            font=dict(
                color=conf['legend_font_color'],
                size=conf['legend_font_size'],
            ),
            textangle=270,
            borderpad=0,
        )
    
    return fig


"""
Function to create the map

Arguments:
    df: The dataframe that contains all the necessary columns
    colors: List of 9 blended colors
    x: Name of the column that contains values of first variable (defaults to 'x')
    y: Name of the column that contains values of second variable (defaults to 'y')
    ids: Name of the column that contains ids that connect the data to the GeoJSON (defaults to 'id')
    name: Name of the column conatining the geographic entity to be displayed as a description (defaults to 'name')
"""

def create_bivariate_map(df, colors, geojson, x='x', y='y', ids='id', name='name', conf=conf_defaults()):
    
    if len(colors) != 9:
        raise ValueError('ERROR: The list of bivariate colors must have a length eaqual to 9.')
    
    # Recalculate values if width differs from default
    if not conf['width'] == 1000:             
        conf = recalc_vars(conf['width'], ['height', 'plot_title_size', 'legend_font_size', 'map_zoom'], conf)
        
    # Prepare the dataframe with the necessary information for our bivariate map
    df_plot = prepare_df(df, x, y)
    # locations="WKC", 
    # Create the figure
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson,
        locations=df_plot[ids],
        featureidkey="properties.WK_CODE",
        z=df_plot['biv_bins'],
        marker_line_width=.5,
        # mapbox_style="carto-positron",
        colorscale=[
            [0/8, colors[0]],
            [1/8, colors[1]],
            [2/8, colors[2]],
            [3/8, colors[3]],
            [4/8, colors[4]],
            [5/8, colors[5]],
            [6/8, colors[6]],
            [7/8, colors[7]],
            [8/8, colors[8]],
        ],
        customdata=df_plot[[name, ids, x, y]],  # Add data to be used in hovertemplate
        hovertemplate='<br>'.join([  # Data to be displayed on hover
            '<b>%{customdata[0]}</b> (ID: %{customdata[1]})',
            conf['hover_x_label'] + ': %{customdata[2]}',
            conf['hover_y_label'] + ': %{customdata[3]}',
            '<extra></extra>',  # Remove secondary information
        ])
    ))

    # Add some more details
    fig.update_layout(
        title=dict(
            text=conf['plot_title'],
            font=dict(
                size=conf['plot_title_size'],
            ),
        ),
        mapbox_style='carto-positron',
        width=conf['width'],
        height=conf['height'],
        autosize=True,
        mapbox=dict(
            center=dict(lat=conf['center_lat'], lon=conf['center_lon']),  # Set map center
            zoom=conf['map_zoom']  # Set zoom
        ),
    )

    fig.update_traces(
        marker_line_width=conf['borders_width'],  # Width of the geographic entity borders
        marker_line_color=conf['borders_color'],  # Color of the geographic entity borders
        showscale=False,  # Hide the colorscale
    )

    # Add the legend
    fig = create_legend(fig, colors, conf)
    
    return fig

# Define sets of 9 colors to be used
# Order: bottom-left, bottom-center, bottom-right, center-left, center-center, center-right, top-left, top-center, top-right

color_sets = {
    'pink-blue':   ['#e8e8e8', '#ace4e4', '#5ac8c8', 
                    '#dfb0d6', '#a5add3', '#5698b9', 
                    '#be64ac', '#8c62aa', '#3b4994'],
    'teal-red':    ['#eae3f5', '#e4acac', '#c85a5a', 
                    '#b0d5df', '#ad9ea5', '#985356', 
                    '#64acbe', '#627f8c', '#574249'],
    'blue-organe': ['#fef1e4', '#fab186', '#f3742d',  
                    '#97d0e7', '#b0988c', '#ab5f37', 
                    '#18aee5', '#407b8f', '#5c473d']
}