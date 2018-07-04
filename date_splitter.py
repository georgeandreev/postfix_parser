from datetime import datetime
from datetime import timedelta
from random import randint

log_arr = []
i = 0
startdate = datetime(2018, 1, 1)
while i < 500000:
	log_arr.append((startdate + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S"))
	i += randint(1, 10)
enddate = datetime.strptime(log_arr[-1], '%Y-%m-%d %H:%M:%S')
add_const = int(len(log_arr) / ((enddate - startdate).days / 30)) * 2


indexes = []
start_index = 0
start = 0
end_index = add_const
last_index = len(log_arr)

cur_month = startdate.month
while True:

	cur_index = min(int((start_index + end_index) / 2), last_index)
	if cur_index == last_index:
		indexes.append((start_index, last_index))
		break
	curdate = datetime.strptime(log_arr[cur_index], '%Y-%m-%d %H:%M:%S')
	nextdate = datetime.strptime(log_arr[cur_index + 1], '%Y-%m-%d %H:%M:%S')
	previousdate = datetime.strptime(log_arr[cur_index - 1], '%Y-%m-%d %H:%M:%S')
	
	if curdate.month > previousdate.month or curdate.year > previousdate.year:
		indexes.append((start, cur_index))
		start = cur_index
		start_index = cur_index
		end_index = start_index + add_const
		cur_month += 1
		cur_month = max(1, cur_month % 13)
		continue

	if curdate.month < nextdate.month or curdate.year < nextdate.year:
		indexes.append((start, cur_index))
		start = cur_index + 1
		start_index = cur_index + 1
		end_index = start_index + add_const
		cur_month += 1
		cur_month = max(1, cur_month % 13)
		continue
		
	if curdate.month != cur_month:
		end_index = cur_index
	else:
		start_index = cur_index
	
for item in indexes:
	print(item)
