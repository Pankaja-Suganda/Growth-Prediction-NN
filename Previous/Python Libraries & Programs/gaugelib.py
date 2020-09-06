import tkinter as tk
import cmath
from decimal import Decimal

#exec(open('images.py').read())

class ini(tk.Frame):
    def __init__(self, parent, size=100, **options):
        tk.Frame.__init__(self, parent, padx=0, pady=0, borderwidth=0,highlightthickness=0,
                          **options)
        self.size = size
    def to_absolute(self, x, y):
        return x + self.size/2, y + self.size/2
		
    
class DrawGauge2(ini):
    def __init__(self, parent,
                 max_value: (float, int) = 100.0,
                 min_value: (float, int) = 0.0,
                 size:      (float, int) = 100,
                 img_data:   str=None,
                 bg_col:str='blue',
                 unit: str=None,
                 bg_sel=1,
                 label: str=None,
                 **options):
        super().__init__(parent, size=size, **options)

        self.max_value = float(max_value)
        self.min_value = float(min_value)
        self.size = size
        self.bg_col = bg_col
        self.bg_sel=bg_sel
        self.unit = '' if not unit else unit
        self.label = '' if not label else label
        self.canvas = tk.Canvas(self, width=self.size, height=self.size-self.size/12,highlightthickness=0)
        self.canvas.grid(row=0)
        self.draw_background()
        self.draw_tick()
        initial_value = 0.0
        self.set_value(initial_value)

    def draw_background(self, divisions=100):
        self.canvas.create_arc(self.size/6, self.size/6, self.size-self.size/6, self.size-self.size/6,
                               width=self.size/10,style="arc",start=300, extent=300,
                               outline = "light gray")
        Unit = self.unit
        Label = self.label
        self.canvas.create_text(self.size/2,5*self.size/8, font=("Arial",int(self.size/18),'bold'),fill="gray", text=Unit,angle=0)
        self.canvas.create_text(self.size/2,8*self.size/10, font=("Times New Roman",int(self.size/28),'bold'),fill="black", text=Label,angle=0)
        self.readout = self.canvas.create_text(self.size/2,4*self.size/6, font=("Arial",int(self.size/18),'bold'),fill="black", text='')
        
    def draw_tick(self,divisions=100):
        inner_tick_radius = int((self.size-self.size/9) * 0.35)
        outer_tick_radius = int((self.size-self.size/9) * 0.45)
        self.readout = self.canvas.create_text(self.size/2,4*self.size/5, font=("Arial",int(self.size/18),'bold'),fill="white", text='')
        inner_tick_radius2 = int((self.size-self.size/9) * 0.48)
        outer_tick_radius2 = int((self.size-self.size/9) * 0.50)
        inner_tick_radius3 = int((self.size-self.size/9) * 0.35)
        outer_tick_radius3 = int((self.size-self.size/9) * 0.40)
        for tick in range(divisions+1):
            angle_in_radians = (2.0 * cmath.pi / 3.0)+tick/divisions * (5.0 * cmath.pi / 3.0)
            inner_point = cmath.rect(inner_tick_radius, angle_in_radians)
            outer_point = cmath.rect(outer_tick_radius, angle_in_radians)
            if (tick%10) == 0:
                self.canvas.create_line(
                    *self.to_absolute(inner_point.real, inner_point.imag),
                    *self.to_absolute(outer_point.real, outer_point.imag),
                    width=2,fill='blue')
            else:
                inner_point3 = cmath.rect(inner_tick_radius3, angle_in_radians)
                outer_point3 = cmath.rect(outer_tick_radius3, angle_in_radians)
                self.canvas.create_line(
                    *self.to_absolute(inner_point3.real, inner_point3.imag),
                    *self.to_absolute(outer_point3.real, outer_point3.imag),
                    width=1,fill='black')
            if (tick%10) == 0:
                inner_point2 = cmath.rect(inner_tick_radius2, angle_in_radians)
                outer_point2 = cmath.rect(outer_tick_radius2, angle_in_radians)
                x= outer_point2.real + self.size/2
                y= outer_point2.imag + self.size/2
                label = str(int(self.min_value + tick * (self.max_value-self.min_value)/100))
                self.canvas.create_text(x,y, font=("Arial",int(self.size/25)),fill="black", text=label)
                
    def set_value(self, number: (float, int)):
        number = number if number <= self.max_value else self.max_value
        number = number if number > self.min_value else self.min_value
        degree = 30.0 + (number- self.min_value) / (self.max_value - self.min_value) * 300.0
        self.canvas.create_arc(self.size/6, self.size/6, self.size-self.size/6, self.size-self.size/6,
                               style="arc",width=self.size/10,start=270-degree, extent=degree-30,
                               outline = self.bg_col)
#        draw_dial(self.canvas,self.size/2,self.size/2,-1*degree,self.size/3,8)
        label = str('%.2f' % number)
        self.canvas.delete(self.readout)
        self.draw_tick()
        self.readout = self.canvas.create_text(self.size/2,3*self.size/6, font=("Arial",int(self.size/16),'bold'),fill="black", text=label,angle=0)
