from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import sys
from datetime import datetime

def get_time_value(data_updated):
    """ This function will take the file data and parse the time values and calls get_time_period() function to 
         get the time difference.
         data_updated           : Data from the file
    """
      
    format = "%I:%M:%p"
    time = 0;
    index = data_updated.find("TIME LOG:")
    if index!=-1:
        data_updated = data_updated[index+len("TIME LOG:"):]
        index = data_updated.find('-')
        count = 1
        while (index!=-1):
            if data_updated[index+1]==' ':
                data_updated = data_updated[:index-1] + "#" + data_updated[index+2:];
            elif data_updated[index-1]==' ':
                 data_updated = data_updated[:index-2] + "#" + data_updated[index+1:]
            else:
                data_updated = data_updated[:index-1] + "#" + data_updated[index+1:];
            index = data_updated.find("#",index-2,index+2);
            start_time = data_updated.rfind(" ",0,index);
            start_time = data_updated[start_time+1:index];
            end_time = data_updated.find("M",index,index+15);
            end_time = data_updated[index+1:end_time+1];
            start_time = start_time[:len(start_time)-2] + ":" + start_time[len(start_time)-2:]
            end_time = end_time[:len(end_time)-2] + ":" + end_time[len(end_time)-2:]
            
            try:
                start_time_list = start_time.split(":")
                end_time_list = end_time.split(":")
                
                if int(start_time_list[0]) >12 or int(end_time_list[0])> 12:
                    error = "There is a Error at line "+str(count)                  
                    
                else:                               
                    period = get_time_period(end_time,start_time)
                    error = False
                 
                time = time + period
                
            except:
                index = data_updated.find('-')
                continue;
            index = data_updated.find('-')
            count = count+1
            
    hours = int(time/60)
    minutes = int(time%60)          
    
    return error,hours,minutes
    
    #print(error) if error else print("Total Time spent in the file is",hours,"hours",minutes,"mins")
                
                

def get_time_period(start_time,end_time):
    """ This functions takes the start_time,end_time and calculate the difference between them.
        start_time                : Start time of the line
        end_time                  : End time of the line
    """
    
    start_time_list = start_time.split(":")
    end_time_list = end_time.split(":")   
    
    
    if int(start_time_list[0]) == 12:
        start_time_list[0] = 0
    if int(end_time_list[0]) == 12:
        end_time_list[0] = 0
    
    if start_time_list[2] == "PM":
        start_time_list[0] = int(start_time_list[0]) + 12
    if end_time_list[2] == "PM":
        end_time_list[0] = int(end_time_list[0]) + 12
    
    del end_time_list[2], start_time_list[2]
  
    
    start_time_list = list(map(int, start_time_list))
    end_time_list = list(map(int, end_time_list))
    
    if end_time_list[1] > start_time_list[1]:
        start_time_list[1] = start_time_list[1]+60
        start_time_list[0] = start_time_list[0]-1
        
    
    hours_diff =  start_time_list[0] - end_time_list[0]
    minutes_diff = start_time_list[1] - end_time_list[1]
    
        
    hours_diff = hours_diff +24 if hours_diff<0 else hours_diff
    
    time_diff = (hours_diff*60)+minutes_diff            

    return time_diff   


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/"

    
@app.route('/')
def upload_file():
    return render_template('index.html')
 
@app.route('/display', methods = ['GET', 'POST'])
def parse():
    if request.method == 'POST':
        f = request.files['file']        
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        f1 = open(app.config['UPLOAD_FOLDER']+filename,'r').read()
        #t,e = GetTimeValue(f1)        
        data_updated = f1.upper()
        error,hours,minutes = get_time_value(data_updated)
        
        if error:
            output = error
            
        else:   
            output = "Total Time spent in the file is " + str(hours) + " hours " + str(minutes) + "mins"
        
        return render_template('index.html',prediction_text=output)
    return render_template('index.html')
        
 
    
if __name__ == '__main__':
    app.run(debug = True)