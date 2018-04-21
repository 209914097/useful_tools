from PIL import Image,ImageFilter

img = Image.open('nuo.jpg')
img.convert('L').save('gray.jpg')
img = Image.open('gray.jpg')
img = img.filter(ImageFilter.GaussianBlur(radius=2)).save('gray.jpg')
img = Image.open('gray.jpg')
pixdata = img.load()
w, h = img.size

for y in range(h):
    line = []
    for x in range(w):

        line.append(pixdata[x,y])
    line=[str(int(x/4)) for x in line ]
    with open('gray.csv','a') as f:
        f.write(",".join(line)+'\n')

import plotly.graph_objs as go
import plotly.plotly
import pandas as pd

# Read data from a csv
z_data = pd.read_csv('gray.csv')

data = [
    go.Surface(
        z=z_data.as_matrix(),

    ),

]
layout = go.Layout(
    title='Nobel',
    autosize=True,
    # width=500,
    # height=500,
    # margin=dict(
    #     l=65,
    #     r=50,
    #     b=65,
    #     t=90
    # )
    # scene={
    #     "aspectratio": {
    #         "x": 1,
    #         "y": 1,
    #         "z": 1,
    #     },
    # },
)

fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='elevations-3d-surface')
