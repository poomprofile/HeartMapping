from math import pi
import numpy as np
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CustomJS, RadioButtonGroup, TapTool
from bokeh.layouts import column

# Create data for segments
segments = np.linspace(0, 2 * pi, 7)  # 6 segments + 1 to close the circle
radii = [0.33, 0.66, 1.0, 1.33]  # Radii for 4 rings (center, basal, mid, apical)

# Define initial colors for each segment
colors = [
    "#d3a4ff", "#d3a4ff", "#d3a4ff", "#d3a4ff", "#d3a4ff", "#a9ff97",  # Basal segments
    "#a9ff97", "#a9ff97", "#a9ff97", "#d3a4ff", "#d3a4ff", "#a9ff97",  # Mid-cavity segments
    "#ffdab9", "#ffdab9", "#ffdab9", "#ffdab9", "#d3a4ff"              # Apical segments
]

data = {
    'start_angle': [],
    'end_angle': [],
    'inner_radius': [],
    'outer_radius': [],
    'color': colors,
}

# Create data for the rings
for i in range(3):  # 3 rings (basal, mid, apical)
    for j in range(6):  # 6 segments per ring
        data['start_angle'].append(segments[j])
        data['end_angle'].append(segments[j + 1])
        data['inner_radius'].append(radii[i])
        data['outer_radius'].append(radii[i + 1])

# Add center segment (17th segment)
data['start_angle'].append(0)
data['end_angle'].append(2 * pi)
data['inner_radius'].append(0)
data['outer_radius'].append(radii[0])
data['color'].append("#d3a4ff")  # Adding color for the 17th segment

# Add segments 13 to 16 (inner ring)
inner_segments = np.linspace(0, 2 * pi, 5)  # 4 segments + 1 to close the circle
for j in range(4):  # 4 segments
    data['start_angle'].append(inner_segments[j])
    data['end_angle'].append(inner_segments[j + 1])
    data['inner_radius'].append(radii[0])
    data['outer_radius'].append(radii[1])
    data['color'].append("#ffdab9")

source = ColumnDataSource(data=data)

# Create polar plot
p = figure(height=600, width=600, title="LV 17 Segment Polar Plot",
           tools="", x_range=(-1.5, 1.5), y_range=(-1.5, 1.5))

p.annular_wedge(x=0, y=0, inner_radius='inner_radius', outer_radius='outer_radius',
                start_angle='start_angle', end_angle='end_angle', color='color',
                source=source, line_color="black")

# Radio button widget for selecting colors
color_picker = RadioButtonGroup(labels=["LAD", "LCx", "RCA"], active=0)
color_map = ["#d3a4ff", "#a9ff97", "#ffdab9"]  # Colors corresponding to LAD, LCx, RCA

# JavaScript callback to update color on segment click
callback = CustomJS(args=dict(source=source, color_picker=color_picker, color_map=color_map), code="""
    const data = source.data;
    const selected_color = color_map[color_picker.active];
    const selected = source.selected.indices;
    for (let i = 0; i < selected.length; i++) {
        data['color'][selected[i]] = selected_color;
    }
    source.change.emit();
""")

# Add tap tool and callback
taptool = TapTool(callback=callback)
p.add_tools(taptool)

# Layout
layout = column(p, color_picker)

# Output to static HTML file
output_file("lv17_segment_polar_plot.html")

# Show plot
show(layout)
