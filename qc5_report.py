import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit
#import matplotlib.font_manager as font_manager
import mplhep as hep
#from fpdf import FPDF
import argparse

def main():
    "------------------------------------------------------"
    acquisition_time = args.acq_time  
    date = args.qc5_date  
    primaries = args.primaries
    plateau_point = args.plateau_point 
    module_type = args.module_type
    module_number = args.module_number
    "------------------------------------------------------"
    filename = r'./data/QC5_GE21-MODULE-{}-{}_{}.txt'.format(module_type, module_number, date)
    data = pd.read_csv(filename, sep = "\t", names = ['Vmon','Imon', 'Time', 'Pressure', 'Temp', 'Counts_OFF', 'Counts_OFF_err', 'Counts_ON', 'Counts_ON_err', 'Current_OFF', 'Current_OFF_err', 'Current_ON', 'Current_ON_err'])
    data.drop(data.head(3).index, inplace=True)
    pressure = data['Pressure'].tolist()[0]
    temperature = data['Temp'].tolist()[0]

    data_reverse = data.iloc[::-1]

    divider_current = data_reverse['Imon'].to_numpy().astype(float)
    countsON = data_reverse['Counts_ON'].to_numpy().astype(float)
    countsOFF = data_reverse['Counts_OFF'].to_numpy().astype(float)
    countON_err = data_reverse['Counts_ON_err'].to_numpy().astype(float)
    countOFF_err = data_reverse['Counts_OFF_err'].to_numpy().astype(float)
    currentON = data_reverse['Current_ON'].to_numpy().astype(float)
    currentOFF = data_reverse['Current_OFF'].to_numpy().astype(float)
    currentON_err = data_reverse['Current_ON_err'].to_numpy().astype(float)
    currentOFF_err = data_reverse['Current_OFF_err'].to_numpy().astype(float)
    
    #Imon correction
    p0 = 964.4 #mbar
    t0 = 297.1 #K 
    p = float(pressure)
    t = float(temperature)
    divider_current = divider_current * pow((t/t0 )*(p0/p),0.43)

    #Current calculation
    current = np.absolute(np.subtract(currentON, currentOFF))
    current_err = np.sqrt(np.power(currentON_err,2) + np.power(currentOFF_err,2))

    #Rate calculation
    rate = np.subtract(countsON, countsOFF)/acquisition_time
    rate_err = np.sqrt(np.power(countON_err,2) + np.power(countOFF_err,2))/acquisition_time 

    #Rate plateau for gain calculation (if there are less than 3 points at the plateau a warning is sent
    percentage_diff = np.diff(rate)/rate[:-1]*100
    points_plateau = (percentage_diff<1.).sum()
    index_plateau = len(rate)-plateau_point+1 
    if points_plateau < 3 :
        print("--------- WARNING ---------")
        print("There are less than 3 points in plateau")
        print("Choose the proper point for the gain from command line")
    elif points_plateau >= 3:
        indices = percentage_diff<1.
        sel_indices = (np.where(indices)[0]) 
        index_plateau = sel_indices[1]   

    #Gain calculation
    gain = current/(rate[index_plateau]*primaries*1.602E-19) 
    gain_err_den = np.power(rate[index_plateau]*primaries*1.602E-19,2)
    gain_err_rel_rate = np.power((rate_err[index_plateau]/rate[index_plateau]),2)
    gain_err_rel_prim = np.power((2.9/primaries),2)
    gain_err = np.sqrt((np.power(current_err,2)+np.power(current,2)*(gain_err_rel_rate+gain_err_rel_prim))/gain_err_den)

    #Divider current correction for the gain

    #-------------------
    plt.style.use(hep.style.CMS)
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.15, right=0.85)
    #plots
    ax2 = ax.twinx()
    ax.errorbar(divider_current, gain, yerr = gain_err, linestyle='', marker='o', markersize=5, label='Gain', color='r')
    ax2.errorbar(divider_current, rate, yerr = rate_err, linestyle='', marker='o', markersize=5, label='Rate', color='b')
    ax.set_yscale('log')
    ax.set_xlabel('Divider current ($\mu$A)')
    ax.set_ylabel('Effective gain')
    ax2.set_ylabel('Rate (Hz)')
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1+h2, l1+l2, loc='lower right')

    ymin = gain[0]
    ymax = gain[-1]
    xmin = divider_current[0]
    ax.text(xmin, ymax-(ymax-ymin)/6., 'GE21-MODULE-{}-{}'.format(module_type, module_number), fontsize=18) 
    ax.text(xmin, ymax-1.5*(ymax-ymin)/5., "Pressure: "+str(round(float(pressure),1)) +" mBar", fontsize=14) 
    ax.text(xmin, ymax-2*(ymax-ymin)/5., "Temperature: "+str(round(float(temperature),1)) + "$^\circ$C", fontsize=14) 
    ax.text(xmin, ymax-2.4*(ymax-ymin)/5., "Number of primaries: " + str(primaries) , fontsize=14)
    ax.text(xmin, ymax-2.8*(ymax-ymin)/5., "Gas: Ar/CO2 (70/30)" , fontsize=14)
    ax.text(xmin, ymax-3.2*(ymax-ymin)/5., "X-ray setting: 40kV 5$\mu$A" , fontsize=14)
    #plt.show()

    plt.savefig('./plot/QC5_GE21-MODULE-{}-{}.png'.format(module_type, module_number))

if __name__ == '__main__':
    descrString = "Gain plot"
    parser = argparse.ArgumentParser()
    parser.add_argument("-at", "--acq_time", dest="acq_time", type=float,  help="Acquisition time in seconds, default = 60 s", default =60.)
    parser.add_argument("-np", "--primaries", dest="primaries", type=float, help ="Number of primaries, default = 346", default=346)
    parser.add_argument("-pp", "--plateau_point",dest="plateau_point", type=int, help = "Plateau rate index (count from higher current)", default = 1 )
    parser.add_argument("-mt", "--module_type", dest="module_type", help="module type")
    parser.add_argument("-mn", "--module_number", dest="module_number", help="module number (XXXX)")
    parser.add_argument("-d",  "--qc5_date", dest="qc5_date", help="qc5 test date (YYYYMMDD)")
    args = parser.parse_args()
    main()
