# -*- coding: utf-8 -*-
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from plyer import accelerometer

'''
This example uses Kivy Garden Graph addon to draw graphs plotting the
accelerometer values in X,Y and Z axes.
The package is installed in the directory: ./libs/garden/garden.graph
To read more about kivy garden, visit: http://kivy-garden.github.io/.
'''
from kivy_garden.graph import Graph, LinePlot

kv = '''
#:import Graph kivy_garden.graph.Graph
<AccelerometerDemo>:
    orientation: 'vertical'

    Graph:
        id: graph_plot
        background_color: (0.5, 0.5, 0.5, 1)
        xlabel: 't'
        ylabel: 'accelerometer'
        x_grid: True
        y_grid: True
        x_grid_label: True
        y_grid_label: True
        x_ticks_minor: 5
        x_ticks_major: 25
        ymin: 0
        ymax: 10
        y_ticks_major: 1

    ToggleButton:
        id: toggle_button
        on_release: root.do_toggle()
        text: 'Start Accelerometer'
        size_hint: 1, None
        height: self.texture_size[1] * 5
'''
Builder.load_string(kv)

class AccelerometerDemo(BoxLayout):
    def __init__(self):
        super(AccelerometerDemo, self).__init__()

        self.sensorEnabled = False
        self.graph = self.ids.graph_plot

        # For all X, Y and Z axes
        self.plot = []
        self.plot.append(LinePlot(color=[1, 0, 0, 1], line_width=3)) #X - Red
        self.plot.append(LinePlot(color=[0, 1, 0, 1], line_width=3)) #Y - Green
        self.plot.append(LinePlot(color=[0, 0, 1, 1], line_width=3)) #Z - Blue

        self.reset_plots()

        for plot in self.plot:
            self.graph.add_plot(plot)

    def reset_plots(self):
        for plot in self.plot:
            plot.points = [(0,0)]

        self.counter = 1

    def do_toggle(self):
        if not self.sensorEnabled:
            accelerometer.enable()
            Clock.schedule_interval(self.get_acceleration, 1 / 20.)

            self.sensorEnabled = True
            self.ids.toggle_button.text = "Stop Accelerometer"
        else:
            accelerometer.disable()
            self.reset_plots()
            Clock.unschedule(self.get_acceleration)

            self.sensorEnabled = False
            self.ids.toggle_button.text = "Start Accelerometer"

    def get_acceleration(self, dt):
        val = accelerometer.acceleration
        if val[0] is None:
            return

        if (self.counter == 100):
            # We re-write our points list if number of values exceed 100.
            # ie. Move each timestamp to the left.
            for plot in self.plot:
                del(plot.points[0])
                plot.points[:] = [(i[0] - 1, i[1]) for i in plot.points[:]]
                pass

            self.counter = 99

        self.plot[0].points.append((self.counter, val[0]))
        self.plot[1].points.append((self.counter, val[1]))
        self.plot[2].points.append((self.counter, val[2]))

        self.counter += 1

class AccelerometerDemoApp(App):
    def build(self):
        return AccelerometerDemo()

if __name__ == '__main__':
    AccelerometerDemoApp().run()