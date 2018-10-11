#Bugsy's Refractometer ABV Calculator
#Version 1.04.2
#10-10-2018
#Created By: Jonathan Braley
#Wort Correction Formula: http://seanterrill.com/2011/04/07/refractometer-fg-results/

from decimal import Decimal #decimal function used with round to manage decimal places
import time #time function used to pause calculations in command prompt
import os #used to clear screen when recalculating
from tkinter import * #used to create GUI

class beer():
    def __init__(self, og, fg):
        self.og = float(og) #convert input og to float
        self.fg = float(fg) #convert input fg to float

    def calculate_og_brix(self):
        self.brixog = (((182.4601 * self.og - 775.6821) * self.og + 1262.7794) * self.og - 669.5622) #convert original gravity to original brix
        self.brixog_output = round(self.brixog,2) #round function used to adjust decimal places
        
    def calculate_of_brix(self):
        self.brixfg = (((182.4601 * self.fg - 775.6821) * self.fg + 1262.7794) * self.fg - 669.5622) #convert preadjusted final gravity to preadjusted final brix
        self.brixfg_output = round(self.brixfg,2) #round function used to adjust decimal places

    def adjust_fg(self):
        self.adjusted_fg = 1.0000 - 0.00085683 * self.brixog + 0.0034941 * self.brixfg #adjust measured final gravity
        self.adjusted_fg_output = round(self.adjusted_fg,3) #round function used to adjust decimal places

    def calc_abv(self):
        self.abvCalc = self.og - self.adjusted_fg #calculate ABV with OG and adjusted FG
        self.abv = self.abvCalc * 131.25
        self.abv_output = round(self.abv,2) #round function used to adjust decimal places

    def calc_attenuation(self):
        self.attnCalc = (self.og - 1) * 1000 - (self.adjusted_fg - 1) * 1000 #calculate attenuation with OG and adjusted FG
        self.attn = self.attnCalc / (self.og - 1) * 0.1
        self.attn_output = round(self.attn,2) #round function to adjust decimal places

    def calc_calories(self):
        self.calAbv = 1881.22 * self.adjusted_fg * (self.og - self.adjusted_fg) / (1.775 - self.og) #calculate calories using OG and adjusted FG
        self.calCarb = 3550 * self.adjusted_fg * ((0.1808 * self.og) + (0.8192 * self.adjusted_fg) - 1.0004)
        self.calories = self.calAbv + self.calCarb
        self.calories_output = round(self.calories,2) #round function used to adjust decimal places

    def print_mug(self):
        print(' ')
        print('                    .sssssssss. ')
        print('                .sssssssssssssssssss ')
        print('              sssssssssssssssssssssssss ')
        print('             ssssssssssssssssssssssssssss ')
        print('              @@sssssssssssssssssssssss@ss ')
        print('              |s@@@@sssssssssssssss@@@@s|s ')
        print('       _______|sssss@@@@@sssss@@@@@sssss|s ')
        print('     /         sssssssss@sssss@sssssssss|s ')
        print('    /  .------+.ssssssss@sssss@ssssssss.| ')
        print('   /  /       |...sssssss@sss@sssssss...| ')
        print('  |  |        |.......sss@sss@ssss......| ')
        print('  |  |        |..........s@ss@sss.......| ')
        print('  |  |        |...........@ss@..........| ')
        print('   \  \       |............ss@..........| ')
        print('    \   ------+...........ss@...........| ')
        print('     \________ .........................| ')
        print('              |.........................| ')
        print('             /...........................\ ')
        print('            |.............................| ')
        print('               |.......................| ')
        print('                   |...............| ')
        print(' ')

class SetupManager:
    def __init__(self, master):
        self.master = master
        master.title("BUGSY'S REFRACTOMETER ABV CALCULATOR") #add title to the top of the window

        self.og = Entry(master) #create OG  entry box
        self.og.grid(row = 1, column = 1) # place OG entry box

        self.og_label = Label(master, text="Original Gravity") #create og label
        self.og_label.grid(row = 1) #place og label

        self.og_brix_label = Label(master, text="Original Brix") #create Original Brix label
        self.og_brix_label.grid(row = 1, column = 2) #place Original Brix label

        self.og_brix_label_value = Label(master, text="-----") #create Original Brix output label
        self.og_brix_label_value.grid(row = 1, column = 3) #place Original Brix output label

        self.abv_label = Label(master, text="Calculated ABV") #create ABV label
        self.abv_label.grid(row = 1, column = 4) #place ABV label

        self.abv_label_value = Label(master, text="-----") # create ABV output label
        self.abv_label_value.grid(row = 1, column = 5) #place ABV output label

        self.calories_label = Label(master, text="Calories") #create calories label
        self.calories_label.grid(row = 1, column = 6) #place calories label

        self.calories_label_value = Label(master, text="-----") #create calories output label
        self.calories_label_value.grid(row = 1, column = 7) #place calories output label

        self.fg = Entry(master) #create fg entry box
        self.fg.grid(row = 2, column = 1) #place fg entry box

        self.fg_label = Label(master, text="Final Gravity") #create final gravity label
        self.fg_label.grid(row = 2) #place final gravity label

        self.fg_brix_label = Label(master, text="Final Brix") #create fg brix label
        self.fg_brix_label.grid(row = 2, column = 2) #place fg brix label

        self.fg_brix_label_value = Label(master, text="-----") #create brix output label
        self.fg_brix_label_value.grid(row = 2, column = 3) #place bric output label

        self.attn_label = Label(master, text="Calculated Attenuation") #create attenuation label
        self.attn_label.grid(row = 2, column = 4) #place attenuation label

        self.attn_label_value = Label(master, text="-----") #create attenuation output label
        self.attn_label_value.grid(row = 2, column = 5) #place attenuation label

        #setup button to run calculation on click
        self.run_button = Button(master, text="Run", command=self.run_calculations)
        self.run_button.grid(column = 1, row = 3)

        #setup button to exit program
        self.close_button = Button(master, text="Exit", command=master.quit)
        self.close_button.grid(column = 2, row = 3)

        #setup button to clear previous values
        self.clear_button = Button(master, text="Clear", command=self.clear_labels)
        self.clear_button.grid(column = 3, row = 3)


    def run_calculations(self):
        calcBeer = beer(self.og.get(),self.fg.get()) #create calcBeer object
        calcBeer.calculate_og_brix() #calculate original brix from gravity reading
        calcBeer.calculate_of_brix() #calculate final brix from gravity reading
        calcBeer.adjust_fg() #calculate adjusted final gravity
        calcBeer.calc_abv() #calculate ABV
        calcBeer.calc_attenuation() #calculate estimated attenuation
        calcBeer.calc_calories() #calculate calories
        self.og_brix_label_value.config(text = calcBeer.brixog_output) #set original brix output label
        self.fg_brix_label_value.config(text = calcBeer.brixfg_output) #set final brix output label
        self.abv_label_value.config(text = calcBeer.abv_output) #set ABV output label
        self.attn_label_value.config(text = calcBeer.attn_output) #set attenuation output label
        self.calories_label_value.config(text = calcBeer.calories_output) #set calories output label
        del calcBeer #destroy calcBeer object 

    def clear_labels(self): #reset calculated labels and entry boxes
        self.og_brix_label_value.config(text = "-----")
        self.abv_label_value.config(text = "-----")
        self.calories_label_value.config(text = "-----")
        self.fg_brix_label_value.config(text = "-----")
        self.attn_label_value.config(text = "-----")
        self.og.delete(0,'end')
        self.fg.delete(0,'end')



def main():
    root = Tk() 
    my_gui = SetupManager(root)
    root.mainloop()

if __name__ == '__main__':
    main()


