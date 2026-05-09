'''This code is the FINAL code used to analyze data steps to analyze'''
'''STEPS
1.) Open raw data excel sheet
2.) Open data analysis sheet
3.) Copy and paste local paths into section labeled #Input raw data file excel path & #Input analysis excel path & sheet name
4.) Copy and paste the names of the sheet to analyze
5.) 3 Functions to use:
    -append_all(start ROI, end ROI):
    ***appends many ROIs to excel sheet automatically***
    start ROI = ROI that you want to start with
    end ROI = ROI that you want to end with

    -all(column_name)
    ***Used for analysis, select ROI name and it will give you a graph and values to analzye***
    column_name = ROI

    -find_max(ROI, start, stop)
    ***When going back to analyze a specific ROI of interest, can find the peak from a specific time stamp if it did not get recognized***
    ROI = ROI to analyze
    start = what time stamp you want to start reading from
    stop = what time stamp you want to end reading from

NOTES:
-Can definetly clean up to be much more user friendly
-Excel sheet, when ROIS are appended, they show up as 0.5x the time they should. Ex: If a peak occurs at second 6.00, excel will show 
it occured at second 3.00. This is alright, because it is fixed in analysis but it is confusing to read when looking over ROI data
-When copy and pasting data into raw data sheet, must make sure that the peak is occuring at timestamp second 2.00 for 2HZ and 1.00
for 20HZ. To do this, delete all of the background and ROI intensity before the first peak so that the peak will occur at this values.
This is to standardize the data.
'''

import pandas as pd
import matplotlib.pyplot as plt
import statistics as st
import xlwings as xw
import math
import numpy as np


#Input Action Potential, Hertz, and FPS
ACTION_POTENTIAL = 10
HZ = 2
FPS = 20 #SHOUlD always be 20

#Input raw data file excel path
raw_excel_path = r'PLACEHOLDER'
raw_sheet_name = 'PLACEHOLDER'

#Input analysis excel path & sheet name
analysis_excel_path = r'PLACEHOLDER'
analysis_sheet_name = 'PLACEHOLDER'

#Input file name, header=BLANK represents where column header is (starts from 0, 1, 2 ...)
###########
# Open workbook without reopening if already open
wb_raw = xw.Book(raw_excel_path)

# Access the sheet
ws_raw = wb_raw.sheets[raw_sheet_name]

# Get data range assuming headers are on row 3 (index 2 in pandas)
# Adjust range as needed — here we assume B3 is top-left of the data table
data_range = ws_raw.range('BV3:DA154')

# Read it into a DataFrame
df = data_range.options(pd.DataFrame, header=1).value
##########3

#Constants for def
frame_multiplier_center = FPS/HZ #what frame is the first frame of the sequence of impulse frames
if FPS % HZ != 0:
    raise ValueError('Frames/sec do not divide by HZ')
IMPULSE_CENTERS = [int(frame_multiplier_center) * i for i in range(ACTION_POTENTIAL + HZ)]
for _ in range(HZ):
    IMPULSE_CENTERS.pop(0)
IMPULSE_RANGE = 3 
TIME_STEP= 1 / FPS
THRESHOLD_MULTIPLIER_SYNC = 4 #WAS 3.7
THRESHOLD_MULTIPLIER_OTHER = .1
TOLERANCE_VESICLE_COUNT = 0.35

#Defining lists - do not touch
synch_data = {}
asynch_data = {}
spon_data = {}

def get_impulse_indices(): 
    indices = []
    for center in IMPULSE_CENTERS:
        indices.extend(range(center - IMPULSE_RANGE, center + IMPULSE_RANGE + 1))
    return indices


def quick_calculate_threshold(column_list, impulse_indices): #impulse indices not used in this version
    # Ensure filtered_vals is always a list of numeric values, not sure how this works
    filtered_vals = []
    '''for i, val in enumerate(column_list):
        if i not in impulse_indices and pd.notna(val):
            try:
                print(i)
                filtered_vals.append(float(val))
            except ValueError:
                continue  # Skip anything non-numeric''' ###THIS PART IS LEFT OUT BECAUSE OF 2 HZ
    for i, val in enumerate(column_list):
        if 0 <= i <= 15 or 124 <= i <= 200 and pd.notna(val):
            try:
                filtered_vals.append(float(val))
            except ValueError:
                continue
    ###CORRECTED 2 HZ VALUE ---> IMPORTANT!!!! THIS IS ALSO USED FOR THE MULTIPLE FUNCTION

            
    std_dev = st.stdev(filtered_vals)
    avg = st.mean(filtered_vals)
    threshold = avg + (THRESHOLD_MULTIPLIER_SYNC * std_dev)

    return threshold

def calculate_other_thershold():
    min_sync_value = min(synch_data.keys())
    threshold_other = float(min_sync_value) * (1-THRESHOLD_MULTIPLIER_OTHER)
    return threshold_other
    
def classify_multiple(column_name, dict, observed, base, tolerance=TOLERANCE_VESICLE_COUNT):
    column_list = df[column_name].values.tolist()
    #impulse_indices = get_impulse_indices()
    filtered_vals = []
    for i, val in enumerate(column_list):
        if 0 <= i <= 15 or 124 <= i <= 200 and pd.notna(val):
            try:
                filtered_vals.append(float(val))
            except ValueError:
                continue
            
    avg = st.mean(filtered_vals)
    ratio = (float(observed) - avg) / (float(base) - avg)
    nearest = round(ratio)
    error = abs(ratio - nearest)
    
    if list(dict.keys())[0] == 0:
        return 0
    elif error <= tolerance:
        return nearest
    #elif observed > quick_calculate_threshold(dict): 
    else:
        return math.floor(ratio)

def update_vesicles_released(column_name, dict): #min_dict_values=synch_data
    min_dict_value = min(synch_data.keys())
    for intensity in dict: 
        vesicles_released = classify_multiple(column_name, dict, intensity, min_dict_value)
        dict[intensity] = [dict[intensity], vesicles_released]

'''def pop_zeros(dictionary):
    helper_dict = list(dictionary.keys())
    x = 0
    for intensity in helper_dict:
        if dictionary[intensity][1] == 0:
            dictionary.pop(intensity)
            x += 1'''

def pop_zeros(dictionary):
    if 0 in dictionary:
        dictionary.pop(0)


# --- SYNCHRONOUS ---
def sync(column_name):
    #column_list = df[column_name].tolist()
    column_list = df[column_name].values.tolist()
    impulse_indices = get_impulse_indices()
    threshold = quick_calculate_threshold(column_list, impulse_indices)
    
    counter = 0
    for center in IMPULSE_CENTERS:
        region = range(center - IMPULSE_RANGE, center + IMPULSE_RANGE + 1)
        peak_val = float('-inf')
        peak_idx = None

        for idx in region:
            if 0 <= idx < len(column_list):
                val = column_list[idx]
                if val >= threshold and val > peak_val:
                    peak_val = val
                    peak_idx = idx

        if peak_idx is not None:
            #print(f"{peak_val:.3f} at time {peak_idx * TIME_STEP:.2f} sec - VESICLES: {BLANK}")
            synch_data.update({round(peak_val, 3): round(peak_idx * TIME_STEP, 2)})
            counter += 1
    if counter == 0:
        synch_data.update({0: 0})
    
    update_vesicles_released(column_name, synch_data)
    for i in synch_data:
        print(f"{i} at time {float(synch_data[i][0])*2} - VESICLES: {synch_data[i][1]}")
    
    print(f"\033[31mSynchronous Peak Count: {counter}\033[0m")

# --- Asynchronous ---
def asyn(column_name):
    column_list = df[column_name].values.tolist()
    impulse_indices = get_impulse_indices()
    threshold = quick_calculate_threshold(column_list, impulse_indices)
    threshold = calculate_other_thershold()
    
    counter = 0

    for i, val in enumerate(column_list):
        if i in impulse_indices or i < 20:
            continue
        time = round(i * 0.05, 2)
        if time > 5.75:
            break
        if val >= threshold:
            if round(time-0.05, 2) in asynch_data.values():
                prev_val = next(k for k, v in asynch_data.items() if v == round(time-0.05, 2))
                if val > column_list[i-1]:
                    asynch_data.pop(prev_val)
                    asynch_data[val] = time
            elif round(time-0.1, 2) in asynch_data.values():
                prev_val = next(k for k, v in asynch_data.items() if v == round(time-0.1, 2))
                if val > column_list[i-2]:
                    asynch_data.pop(prev_val)
                    asynch_data[val] = time
            else:
                asynch_data[val] = time
                counter += 1

    if counter == 0:
        asynch_data.update({0: 0})
    
    #print(asynch_data) --- just a test
    update_vesicles_released(column_name, asynch_data)
    #print(f"new data: {asynch_data}") just a test
    for i in asynch_data:
        print(f"{i:.3f} at time {float(asynch_data[i][0])*2} - VESICLES: {asynch_data[i][1]}")

    print(f"\033[31mAsynchronous Peak Count: {counter}\033[0m")

# --- Spontaneous ---
def spon(column_name):
    column_list = df[column_name].values.tolist()
    impulse_indices = get_impulse_indices()
    threshold = quick_calculate_threshold(column_list, impulse_indices)
    threshold = calculate_other_thershold()

    counter = 0
    multi_peak_checker = []
    
    for i, val in enumerate(column_list):
        time = i * TIME_STEP
        if i in impulse_indices or time < 6: #1.5 is good for this setting
            continue
        if val >= threshold:
            if any(abs(i - j) <= 2 for j in multi_peak_checker):
                continue
            
            #print(f"{val:.3f} at time {time:.2f} sec")
            spon_data.update({f"{val:.3f}": f"{time:.2f}"})
            multi_peak_checker.append(i)
            counter += 1
        
        
    if counter == 0:
        spon_data.update({0: 0})

    update_vesicles_released(column_name, spon_data)
    for i in spon_data:
        print(f"{i} at time {float(spon_data[i][0])*2} - VESICLES: {spon_data[i][1]}")
        
    print(f"\033[31mSpontaneous Peak Count: {counter}\033[0m")

def plot_fig(column_name):
    fig, ax = plt.subplots(figsize=(10,6))
    
    ### FOR 2 HZ GRAPH
    time_list = df['Time']
    new_times = []
    for time in time_list:
        new_times.append((time*2))
    ###
    # Main plot
    #ax.plot(df['Time'], df[column_name], marker='o', linestyle='-', color='blue', label='Synapse Intensity') #### CHANGED FOR 2HZ
    ax.plot(new_times, df[column_name], marker='o', linestyle='-', color='blue', label='Synapse Intensity')

    # Titles and labels
    ax.set_title(column_name, fontsize=16)
    ax.set_xlabel('Time (s)', fontsize=14)
    ax.set_ylabel('Intensity', fontsize=14)
    ax.set_xticks(np.arange(1, 15, 1))
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.legend()

    # Red highlights
    max_time = df['Time'].max() ###Dont use because of time for 2HZ
    highlight_centers = IMPULSE_CENTERS

    ###FOR 2HZ GRAPH
    new_highlight_centers = []
    for i in highlight_centers:
        new_highlight_centers.append(i*2)###

    for center in new_highlight_centers:
        ax.axvspan((center-IMPULSE_RANGE)*TIME_STEP, (center+IMPULSE_RANGE+1)*TIME_STEP, color='red', alpha=0.3)
    
    
    
    plt.show()

###Helper functions for append
def keys(d):
    return [float(d[k][0]) for k in d]

def vesicle_values(d):
    return [float(d[k][1]) for k in d]


def intensity_values(d):
    return list(d.keys())
###

def append(roi):
    wb = xw.Book(analysis_excel_path)
    sheet = wb.sheets[analysis_sheet_name]

    data = {
        'Type': (
            ['Synch.'] + ['-']*(len(synch_data)-1) +
            ['Asynch.'] + ['-']*(len(asynch_data)-1) +
            ['Spon.'] + ['-']*(len(spon_data)-1)
        ),
        'Time': (
            keys(synch_data) + keys(asynch_data) + keys(spon_data)
        ),
        'Intensity': (
            intensity_values(synch_data) + intensity_values(asynch_data) + intensity_values(spon_data)
        ),
        'Vesicles': (
            vesicle_values(synch_data) + vesicle_values(asynch_data) + vesicle_values(spon_data)
        )
    }

    df = pd.DataFrame(data)

    # find first empty column
    col = 30  # AD on excel
    while sheet.cells(2, col).value is not None:
        col += 1

    # write header
    sheet.cells(1, col).value = roi

    # write DataFrame
    sheet.cells(2, col).options(index=False).value = df

def all(column_name):
    roi = f"ROI{column_name}B"
    sync(roi)
    print(f'-------------------------\n')
    asyn(roi)
    print(f'-------------------------\n')
    spon(roi)
    print(f'-------------------------\n')
    column_list = df[roi].values.tolist()
    impulse_indices = get_impulse_indices()
    threshold = quick_calculate_threshold(column_list, impulse_indices)
    min_synch_value = min(synch_data.keys())
    print(f"Sync threshold: {threshold}\nMin Sync: {min_synch_value} - Time: {(synch_data[min_synch_value][0])*2}\nAsync/Spon threshold: {calculate_other_thershold()}")
    filtered_vals = []
    for i, val in enumerate(column_list):
        if 0 <= i <= 15 or 124 <= i <= 200 and pd.notna(val):
            try:
                filtered_vals.append(float(val))
            except ValueError:
                continue
    #print(synch_data) --- tests data
    #print(asynch_data)
    #print(spon_data)
    print(f"\nStandard dev: {st.stdev(filtered_vals)}\nAverage: {st.mean(filtered_vals)}\nThreshold multiplier {THRESHOLD_MULTIPLIER_SYNC}"
        "\nFormula: avg + (THRESHOLD_MULTIPLIER_SYNC * std_dev)")
    append(roi)
    plot_fig(roi)


def append_all(start_roi, end_roi):
    roi = start_roi
    while roi <= end_roi: 
        roi_name = f"ROI{roi}B"
        synch_data.clear()
        asynch_data.clear()
        spon_data.clear()
        sync(roi_name)
        asyn(roi_name)
        spon(roi_name)
        print('----------------')
        append(roi_name)
        roi += 1

###############################################################################################
#Code for appending data tables w/ weighted averages and find max key

def find_max(ROI, start, stop):
    roi = f"ROI{ROI}B"
    column_list = df[roi].values.tolist()
    section = {}
    for i, val in enumerate(column_list):
        time = round(i * 0.1, 2)
        if start <= time <= stop:
            section[time] = val
    if section:
        max_time = max(section, key=section.get)
        print(max_time, section[max_time])
    else:
        print("No data in the specified time range.")



#find_max(7, 5.5, 6.5)

all(2)
#append_all(1, 12)

