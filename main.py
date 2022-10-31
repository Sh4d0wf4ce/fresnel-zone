import tkinter as tk
from tkinter import ttk
import geojson as gj
import tkintermapview
import math
import json

window = tk.Tk()
window.geometry("800x500")

#tabs
tabControl = ttk.Notebook(window)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Tab 1')
tabControl.add(tab2, text='Tab 2')

tabControl.pack(expand=1, fill="both")


#----tab1 content----
def calculate():
    R = 6371*1000 #radius of earth
    h1 = round(slider1.get())
    h2 = round(slider2.get())
    d1 = math.sqrt(2*(4/3)*R*h1)
    d2 = math.sqrt(2*(4/3)*R*h2)
    d = round((d1 + d2)/1000,2)
    f = fEntry.get()
    if f in ('','0') or not f.isnumeric():
        frLabel.configure(text = "Insert frequency")
    else:
        fresnel = round(17.31*(math.sqrt((d)/(4*int(f)))),2)
        frLabel.configure(text = str(fresnel)+"m")
    drLabel.configure(text = str(d)+"km")
    

def save():
    with open('data.json', 'w') as file:
        f = frLabel["text"]
        d = drLabel["text"]
        data = {'LOS': d, 'Fresnel': f}
        json.dump(data, file)
    
    

#sliders
def change(slider, label, *args):
   num = round(slider.get())
   txt = str(num) + "m"
   label.configure(text = txt)

v1 = tk.IntVar()
v2 = tk.IntVar()

slider1 = ttk.Scale(tab1, from_=100, to=0, orient='vertical', variable = v1, command = lambda x: change(slider1, v1Label))
slider2 = ttk.Scale(tab1, from_=100, to=0, orient='vertical', variable = v2, command = lambda x: change(slider2, v2Label))
slider1.grid(row = 1, column = 2, padx = 10, pady = 10)
slider2.grid(row = 1, column = 3, padx = 10, pady = 10)

sLabel = ttk.Label(tab1, text = "Height: ")
sLabel.grid(row = 2, column = 1)

txt = str(v1.get()) + "m"
v1Label = ttk.Label(tab1, text = txt)
v1Label.grid(row = 2, column = 2)


txt = str(v2.get()) + "m"
v2Label = ttk.Label(tab1, text = txt)
v2Label.grid(row = 2, column = 3)

#Input for frequency
fLabel = ttk.Label(tab1, text = "Frequency(GHz): ")
fLabel.grid(row = 3, column = 1)

fValue = tk.IntVar()
fEntry = ttk.Entry(tab1, textvariable = fValue)
fEntry.grid(row = 3, column = 2, columnspan = 2)

#result
dLabel = ttk.Label(tab1, text = "Line of sight of 2 towers: ")
dLabel.grid(row = 1, column = 5, padx = 50)
drLabel = ttk.Label(tab1)
drLabel.grid(row = 1, column = 6)
fLabel = ttk.Label(tab1, text = "Diameter of fresnel zone: ")
fLabel.grid(row = 2, column = 5)
frLabel = ttk.Label(tab1)
frLabel.grid(row = 2, column = 6)

#buttons
b1 = ttk.Button(tab1, text = "Calculate", command = calculate)
b1.grid(row = 4, column = 2, columnspan = 2, pady = 20)

b2 = ttk.Button(tab1, text = "Save to JSON", command = save)
b2.grid(row = 4, column = 5)


#----tab2 content----
def doSomething():
    #saveCords
    h = int(hEntry.get())
    x = float(latitudeEntry.get())
    y = float(longitudeEntry.get())
    R = 6371*1000
    r = round((math.sqrt(2*(4/3)*R*h))/1000, 2)

    point = gj.Point((x, y))

    features = []
    features.append(gj.Feature(geometry=point, properties={"height": h}))

    feature_collection = gj.FeatureCollection(features)

    with open('cords.json', 'w') as f:
        gj.dump(feature_collection, f)

    #generateMap
    #mapWidget.set_position(52.16923796343757, 21.175650827298426)
    mapWidget.set_position(x, y)
    mapWidget.set_zoom(16)


#height
hLabel = ttk.Label(tab2, text = "Height(m):")
hLabel.grid(row = 1, column = 1, pady = 10, padx = 5)
hValue = tk.IntVar()
hEntry = ttk.Entry(tab2, textvariable = hValue)
hEntry.grid(row = 1, column = 2)

#latitude
latitudeLabel = ttk.Label(tab2, text = "Latitude:")
latitudeLabel.grid(row = 2, column = 1, pady = 10, padx = 5)
latitudeValue = tk.IntVar()
latitudeEntry = ttk.Entry(tab2, textvariable = latitudeValue)
latitudeEntry.grid(row = 2, column = 2)

#longitude
longitudeLabel = ttk.Label(tab2, text = "Longitude:")
longitudeLabel.grid(row = 3, column = 1, pady = 10, padx = 5)
longitudeValue = tk.IntVar()
longitudeEntry = ttk.Entry(tab2, textvariable = longitudeValue)
longitudeEntry.grid(row = 3, column = 2)

#save button
cordsButton = ttk.Button(tab2, text = "Save to JSON and display on map", command = doSomething)
cordsButton.grid(row = 4, column = 1, columnspan = 2, padx = 20)


#map
mapWidget = tkintermapview.TkinterMapView(tab2, width=550, height=450, corner_radius=0)
mapWidget.set_position(52.2227995, 20.9829361)
mapWidget.set_zoom(10)
mapWidget.place(x = 230, y = 10)

window.mainloop();
