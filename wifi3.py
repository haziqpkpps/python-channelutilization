# Standard Library imports go here
import argparse
import contextlib
import io
import logging
import sys
import json
import re
import string
import xlsxwriter
import subprocess
import time
# External library imports go here
#
from sys import exit
# Standard Library from-style imports go here
from pathlib import Path

# External library from-style imports go here
from datetime import datetime

#Matplotlib library
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as dates
from matplotlib import style
import warnings
#
# Ideally we all live in a unicode world, but if you have to use something
# else, you can set it here
ENCODE_IN = 'utf-8'
ENCODE_OUT = 'utf-8'

# Set up a global logger. Logging is a decent exception to the no-globals rule.
# We want to use the logger because it sends to standard error, and we might
# need to use the standard output for, well, output. We'll set the name of the
# logger to the name of the file (sans extension).
# log = logging.getLogger(Path(__file__).stem)
#
# class PInterface:
#     def __init__(self, name):
#         self.name = name
#         self.threshold = []

# List SSID
ssid = [
    "SSID"
]

# List STA count
sta_count = [
    "station count"
]
# #Freq display
# freq_int = [
#     "freq"
# ]

# List of Channel utilization
chan_util = [
    "channel utilisation"
]

# signals_txt = [
#     "signal"
# ]

# channels_txt = [
#     "DS Parameter set"
# ]
#
# HT_txt = [
#     "HT20/"
# ]
#
# cipher_txt = [
#     "Group cipher"
# ]
#
# auth_txt = [
#     "Authentication suites"
# ]
def manipulate_data(data, row, worksheet,xtime,ydata1,ydata2,ssid_list,ssid_title):
    """This function is where the real work happens (or at least starts).

    Probably you should write some real documentation for it.

    Arguments:

    * data_in: the data to be manipulated

    """



    #Cell width
    # worksheet.set_column(0, 0, 16)
    # worksheet.set_column(1, 1, 20)
    # worksheet.set_column(2, 2, 15)
    worksheet.set_column(3, 3, 8)
    worksheet.set_column(4, 4, 12)
    worksheet.set_column(5, 5, 6)
    worksheet.set_column(6, 6, 21)
    worksheet.set_column(7, 7, 10)
    worksheet.set_column(8, 8, 20)
    worksheet.set_column(9, 9, 21)
    #


    # # Add a format. Light red fill with dark red text.
    # format1 = workbook.add_format({'bg_color': '#FFC7CE',
    #                                'font_color': '#9C0006'})
    #
    # # Add a format. Green fill with dark green text.
    # format2 = workbook.add_format({'bg_color': '#C6EFCE',
    #                                'font_color': '#006100'})
    #
    # #Apply format
    # worksheet.conditional_format('J2:J200', {'type':     'cell',
    #                                     'criteria': '>=',
    #                                     'value':    75,
    #                                     'format':   format1})
    # worksheet.conditional_format('J2:J200', {'type':     'cell',
    #                                     'criteria': '<=',
    #                                     'value':    74,
    #                                     'format':   format2})

    #row = 0
    col = 0
    lines = data.split('\n')
    i = 1
    alarm_counter = 0
    threshold_counter = 0
    associated = 0

    for line in lines:
        match = re.search('([0-9a-f]{2}:){5}[0-9a-f]{2}\(on wlan0\)(\s*)([-]*)(\s*)(\w*)', line)
        if match:
            if match.group(5)!='associated':
                associated = 0
            else:
                associated = 1
            row += 1
            col =1
            worksheet.write(row,col,'{0}'.format(match.group(0)))
            i += 1
            col =0
            worksheet.write(row,col,'{:%Y-%m-%d %H:%M:%S}'.format(datetime.now()))
            if associated == 1:
                xtime.append('{:%H:%M:%S}'.format(datetime.now()))
        # Timestamp
        match = re.search('(\w+) (\d{2}) (?:(?:(\d{2}):)?(\d{2}):)?(\d{2})', line)
        if match:
            print(str("Processing").format(line))

        # if associated==0: continue
        # Write SSID
        # col =0
        # worksheet.write(row,col,'{:%Y-%m-%d %H:%M:%S}'.format(datetime.now()))
        # xtime.append('{:%H:%M:%S}'.format(datetime.now()))

        for t in ssid:
            pattern = '\W+' + t + ': (\w+)'
            match = re.search(pattern, line)
            if match:
                col =2
                worksheet.write(row,col,match.group(1))
                ssid_title=match.group(1)
                ssid_list.append(match.group(1))


        # Write Client Count
        for t in sta_count:
            pattern = '\W+' + t + ': (\d+)'
            match = re.search(pattern, line)
            if match:
                col =3
                worksheet.write(row,col,match.group(1))
                if associated == 1:
                    ydata1.append(int(match.group(1)))

        # Write Radio Frequency
        # for freq in freq_int:
        #     pattern = '\W+' + freq + ': (\d+)'
        #     match = re.search(pattern, line)
        #     if match:
        #         if int(match.group(1)) < 3000:
        #             col =2
        #             worksheet.write(row,col,'2.4GHz')
        #         else:
        #             col =2
        #             worksheet.write(row,col,'5GHz')
        #
        # for signal in signals_txt:
        #     pattern = '\W+' + signal + ': (.+)'
        #     match = re.search(pattern, line)
        #     #match = re.split(r'dBm',match.group(1))
        #     if match:
        #         col =4
        #         match = match.group(1)[:-4]
        #         worksheet.write(row,col,match)
        #
        # for channel in channels_txt:
        #     pattern = '\W+' + channel + ': (.+)'
        #     match = re.search(pattern, line)
        #     #match = re.split(r'dBm',match.group(1))
        #     if match:
        #         col =3
        #         match = match.group(1)[8:]
        #         worksheet.write(row,col,match)
        #
        # for t in HT_txt:
        #     pattern = '\W+' + t + '(.+)'
        #     match = re.search(pattern, line)
        #     if match:
        #         col =6
        #         worksheet.write(row,col,match.group(1))
        #
        # for t in cipher_txt:
        #     pattern = '\W+' + t + '(.+)'
        #     match = re.search(pattern, line)
        #     if match:
        #         col =7
        #         match = match.group(1)[2:]
        #         worksheet.write(row,col,match)
        #
        # for t in auth_txt:
        #     pattern = '\W+' + t + '(.+)'
        #     match = re.search(pattern, line)
        #     if match:
        #         col =8
        #         match = match.group(1)[2:]
        #         worksheet.write(row,col,match)
        #         #worksheet.write(row,col,match.group(1))

        # Thresholds
        for t in chan_util:
            pattern = '\W+' + t + ': (\d+)/(\d+)'
            match = re.search(pattern, line)
            if match:
                col =4
                worksheet.write(row,col,round(100*float(match.group(1))/float(match.group(2)),2))
                if associated == 1:
                    ydata2.append(int(round(100*float(match.group(1))/float(match.group(2)),2)))
                col =0
                #row +=1

    buf = "Finish"
    return json.dumps(buf)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    # If user doesn't specify an input file, read from standard input. Since
    # encodings are the worst thing, we're explicitly expecting std
    parser.add_argument('-i', '--infile',
                        type=lambda x: open(x, encoding=ENCODE_IN),
                        default=io.TextIOWrapper(
                            sys.stdin.buffer, encoding=ENCODE_IN)
                        )
    # Same thing goes with the output file.
    parser.add_argument('-o'
	                    ,'--outfile'
                        ,type=lambda x: open(x, 'w', encoding=ENCODE_OUT)
						,default=io.TextIOWrapper(sys.stdout.buffer, encoding=ENCODE_OUT)
                        )
    return parser.parse_args()


def read_instream(instream):
    # """Convert raw input for to a manipulatable format.
    #
    # Arguments:
    #
    # *Instream: a file-like object
    #
    # """
    # print(instream)
    # If you need to read a csv, create a DataFrame, or whatever it might be,
    # do it here.
    return instream.read()

def main():
    args = parse_args()
    #Creating file
    workbook = xlsxwriter.Workbook('report-'+datetime.now().strftime('%H%M_%d%m%Y')+'.xlsx')
    #workbook = xlsxwriter.Workbook('report.xlsx')
    worksheet = workbook.add_worksheet()

    #Matplotlib grid setting
    plt.ion()
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    #fig, (ax1,ax3) = plt.subplots(2, sharex=True,figsize=(20, 20))

    xtime = []
    ydata1 = []
    ydata2 = []
    ssid_list = []
    sum_ssid = []
    avg = []

    plt.plot(xtime, ydata2)

    # #Cell formating
    bold = workbook.add_format({'bold': True})

    #Header for every data
    col =0
    row = 0
    worksheet.write(row,col,'Timestamp',bold)
    col =1
    worksheet.write(row,col,'Radio MAC',bold)
    col =2
    worksheet.write(row,col,'SSID',bold)
    # col =2
    # worksheet.write(row,col,'Frequency(Ghz)',bold)
    # col =3
    # worksheet.write(row,col,'Channel',bold)
    # col =4
    # worksheet.write(row,col,'Signal(dBm)',bold)
    col =3
    worksheet.write(row,col,'Client',bold)
    # col =6
    # worksheet.write(row,col,'High Throughput (HT40)',bold)
    # col =7
    # worksheet.write(row,col,'Cipher',bold)
    # col =8
    # worksheet.write(row,col,'Authentication suites',bold)
    col =4
    worksheet.write(row,col,'Channel Utilization(%)',bold)

    time_format = "%H:%M:%S"
    #Graphing(row,xtime,ydata1,ydata2,worksheet)
    #ani = animation.FuncAnimation(fig, Graphing, interval=1000)
    #args.outfile.write(results)

    # print(args.outfile)
    ssid_title=""
    #Hide warning
    warnings.filterwarnings("ignore", ".*GUI is implemented.*")
    try:
        while 1:
            data = subprocess.run(['sudo','iw','dev','wlan0','scan'],stdout=subprocess.PIPE).stdout.decode('utf-8')
            #data = read_instream(args.infile)
            results = manipulate_data(data, row, worksheet,xtime,ydata1,ydata2,ssid_list,ssid_title)
            row += 1
            time.sleep(15)
            avg.append(sum(ydata2)/len(ydata2))
            time_list = [datetime.strptime(i, time_format) for i in xtime]
            #print([x for x in time_list])
            sum_ssid.append(len(ssid_list))
            ssid_list = []
            ax1.plot(time_list,sum_ssid, 'r-',marker='o')
            ax1.set_ylabel("Number of SSID")
            ax3=fig.add_subplot(2,1,2)
            ax2 = ax3.twinx()

            #print("X length: " + str(len(xtime)))
            #print([x for x in xtime])
            print(ssid_title)
            #print("Y length: " + str(len(ydata2)))
            # ax3.clear()
            # ax2.clear()
            ax3.set_title("Channel Utilization vs Client Count", fontsize='large')
            ax1.set_title("Total SSID")
            ax3.plot(time_list,ydata2,'b-',marker='o')
            ax3.plot(time_list,avg,'g--')
            ax3.set_xlabel("Time")
            ax3.set_ylabel("Channel Utilization",color='blue')
            ax3.set_ylim([0, 100])
            ax2.set_ylim([0,50])
            ax2.fill_between(time_list, 0, ydata1,alpha=0.5,color='red')
            ax2.set_ylabel("Client count",color='red')
            ax3.xaxis_date()
            fig.autofmt_xdate()
            #plt.ylim([0,50])
            plt.draw()
            plt.pause(0.01)
            #fig.clear()
            ax3.clear()
            ax2.clear()
            ax1.clear()

    except KeyboardInterrupt:
        print("\nSystem interrupt")
        #print([x for x in time_list])
        workbook.close()
        plt.close()
        sys.exit(0)

if __name__ == "__main__":
    main()
