import os
import numpy as np
import pandas as pd
import time, datetime
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
from oneday_example import summary as oneday_example
from config import data_info, months


# get date from filename
def get_date(filename):
	sep = 0
	for i in range(len(filename)):
		if not filename[i].isdigit():
			sep += 1
			if sep == 3:
				break
	date = filename[:i]
	if not date[6].isdigit():
		date = date[:5] + '0' + date[5:]
	if len(date) < 10:
		date = date[:8] + '0' + date[8:]
	return date


def str_to_datetime(date_time):
	if date_time[4] == '0':
		month_index = eval(date_time[5]) - 1
	else:
		month_index = eval(date_time[4:6]) -1
	month = months[month_index]
	if len(date_time) < 14:
		date_time = date_time[0:8] + (14-len(date_time))*'0' + date_time[8:]
	x = month + ' ' + date_time[6:8] + ', ' + date_time[0:4] +', ' + date_time[8:10] + ':' + date_time[10:12] + ':' + date_time[12:14]
	time_struct = time.strptime(x, '%B %d, %Y, %H:%M:%S')
	dt_time = datetime.datetime.fromtimestamp(time.mktime(time_struct))
	return dt_time
# print(str_to_datetime('20141023124523')-str_to_datetime('20141023124501'))


def sort_by_date(dist_dict):
	dist_list = []
	for key, val in dist_dict.items():
		dist_list.append((get_date(key), val))
	dist_list.sort()
	return dist_list


def sort_by_dist(dist_dict):
	dist_list = [0 for i in range(30)]
	dist_car_list = []
	for key, val in dist_dict.items():
		dist_car_list.append((val, key))
	dist_car_list.sort()
	# minimum = dist_list[0][0], maximum = dist_list[-1][0]
	for dist_car in dist_car_list:
		for i in range(30):
			if dist_car[0] > 50*i and dist_car[0] <= 50*(i+1):
				dist_list[i] += 1
				break
	return dist_list


# given taxi data on one day, divide it into different files by taxi ID
def separate_taxis(filename):
	a = 0
	date =  get_date(filename)
	try:
		os.makedirs('./one_day/' + date + '/')
	except:
		pass
	all_oneday = open(filename, 'r')
	# for line in open(filename):
		# line = all_oneday.readline()
	for line in all_oneday.readlines():
		taxi_id = line[:7]
		fwrite = open('./one_day/'+date+'/'+date+'-'+taxi_id+'.txt', 'a')
		fwrite.write(line)
		fwrite.write('\n')
		fwrite.close()
	return 0
# separate_taxis('2014-10-1-formatted.txt')


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    distance = 6367 * c
    return distance


def onedir_distances(indir):
	fnames = os.listdir(indir)
	distances = {}
	for fname in fnames:
		oneday = open(indir+fname, 'r')
		distance = 0; count = 0
		for line in oneday.readlines():
			if len(line) > 1:
				line_list = line.split()
				line_list_np = np.array(line_list).astype(float)
				if count == 0:
					lon1, lat1 = line_list_np[1], line_list_np[2]
				lon2, lat2 = line_list_np[1], line_list_np[2]
				distance += haversine(lon1, lat1, lon2, lat2)
				lon1, lat1 = lon2, lat2
				count += 1
		distances[fname] = distance
	return distances


def daily_trip_analysis(onecar_ndays):
	fnames = os.listdir(onecar_ndays)
	daily_trip_dict = {}
	for fname in fnames:
		tripnum = 0
		trip_dist = 0 
		empty_car_time = 0 
		oneday = pd.read_table(onecar_ndays+fname, sep=' ').iloc[:, 0:9]
		oneday.columns = data_info[0:9]
		# oneday_count = oneday[(oneday.init_status+oneday.final_status)==1]
		if oneday.iloc[0][8] == 1:
			trip_sign = 1
		else:
			trip_sign = 0 
		time_start = 0
		for i in range(oneday.shape[0]):
			if trip_sign == 0 and time_start == 0:
				time0 = str_to_datetime(str(int(oneday.iloc[i][5]))+str(int(oneday.iloc[i][6]))); time_start += 1
			if (oneday.iloc[i][7:9] == [0, 1]).all() and trip_sign == 0:
				trip_sign = 1; [lon1, lat1] = oneday.iloc[i][1:3]
				if time_start == 1:
					time1 = str_to_datetime(str(int(oneday.iloc[i][5]))+str(int(oneday.iloc[i][6])))
					empty_car_time += (time1 - time0).total_seconds()/3600
			if trip_sign == 1:
				[lon2, lat2] = oneday.iloc[i][1:3]
				trip_dist += haversine(lon1, lat1, lon2, lat2)
				[lon1, lat1] = [lon2, lat2]
			if (oneday.iloc[i][7:9] == [1, 0]).all() and trip_sign == 1:
				trip_sign = 0
				tripnum += 1
				time0 = str_to_datetime(str(int(oneday.iloc[i][5]))+str(int(oneday.iloc[i][6])))		
		daily_trip_dict[get_date(fname)] = (tripnum, trip_dist/tripnum, empty_car_time)
	return daily_trip_dict
# print(daily_trip_analysis('D:/taxi project/wjw/2014-10-formatted-1439141/'))
daily_trip_result = sort_by_date(daily_trip_analysis('D:/taxi project/wjw/2014-10-formatted-1439141/'))
# print(daily_trip_result)


# one_car = sort_by_date(onedir_distances('D:/taxi project/wjw/2014-10-formatted-1439141/'))
# oneday = sort_by_dist(oneday_example)
# print(sort_by_date(onedir_distances('D:/taxi project/wjw/2014-10-formatted-1439141/')))
# print(onedir_distances('D:/Git/taxi-project/one_day/2014-10-1/'))


def plot_onecar():
	global one_car
	plt.xlabel('Date')
	plt.ylabel('Distance')
	plt.title('The distance summary of one car in Oct 2014')
	plt.bar(left=[i for i in range(1, 32)], height=[j[1] for j in one_car])
	plt.show()


def plot_oneday():
	global oneday
	plt.xlabel('Distance range')
	plt.ylabel('Number of taxis')
	plt.title('The distribution of distances on Oct 1st, 2014')
	rects = plt.bar(left=[i*50 for i in range(30)], height=oneday, width=50)
	for rect in rects:
		height = rect.get_height()
		plt.text(rect.get_x()+rect.get_width()-50, 1.03*height, "%s"%(int(height)))
	plt.show()


def plot_trip_num():
	global daily_trip_result
	plt.xlabel('Date')
	plt.ylabel('Number of trips')
	plt.title('The distribution of number of trips of one car in October')
	rects = plt.bar(left=[i for i in range(1, 32)], height=[i[1][0] for i in daily_trip_result], width=1)
	for rect in rects:
		height = rect.get_height()
		plt.text(rect.get_x()+rect.get_width()-50, 1.03*height, "%s"%(int(height)))
	plt.show()


def plot_trip_dist():
	global daily_trip_result
	plt.xlabel('Date')
	plt.ylabel('Average distance of per trip')
	plt.title('The distribution of average distance of per trip of one car in October')
	rects = plt.bar(left=[i for i in range(1, 32)], height=[i[1][1] for i in daily_trip_result], width=1)
	for rect in rects:
		height = rect.get_height()
		plt.text(rect.get_x()+rect.get_width()-50, 1.03*height, "%s"%(int(height)))
	plt.show()


def plot_trip_empty_time():
	global daily_trip_result
	plt.xlabel('Date')
	plt.ylabel('Empty car time (Hours)')
	plt.title('The distribution of empty car time of one car in October')
	rects = plt.bar(left=[i for i in range(1, 32)], height=[i[1][2] for i in daily_trip_result], width=1)
	for rect in rects:
		height = rect.get_height()
		plt.text(rect.get_x()+rect.get_width()-50, 1.03*height, "%s"%(int(height)))
	plt.show()


# plot_onecar()
# plot_oneday()
# plot_trip_num()
# plot_trip_dist()
plot_trip_empty_time()

