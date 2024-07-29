import numpy as np

from bokeh.plotting import figure, show
TOOLS = "pan,wheel_zoom"
x=[1,2,3,4,5]
y=[6,7,2,4,5]
p = figure(tools=TOOLS, output_backend="webgl")
p.circle(x, y, alpha=0.1, nonselection_alpha=0.001)

show(p)