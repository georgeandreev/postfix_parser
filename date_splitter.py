from datetime import datetime
from datetime import timedelta
from random import randint

log_arr = []
i = 0
startdate = datetime(2018, 1, 1)
while i < 600000:
	log_arr.append((startdate + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S"))
	i += randint(1, 10)
enddate = datetime.strptime(log_arr[-1], '%Y-%m-%d %H:%M:%S')
add_const = int(len(log_arr) / ((enddate - startdate).days / 30)) * 2


# Pair (start, end)
indexes = []
start_index = 0
start = 0
end = add_const
last_index = len(log_arr)
print(end, last_index)
# exit()
# Binary search
cur_month = startdate.month
while True:
	cur_index = min(int((start_index + end) / 2), last_index)
	if cur_index == last_index:
		indexes.append((start_index, last_index))
		break
	curdate = datetime.strptime(log_arr[cur_index], '%Y-%m-%d %H:%M:%S')
	nextdate = datetime.strptime(log_arr[cur_index + 1], '%Y-%m-%d %H:%M:%S')
	previousdate = datetime.strptime(log_arr[cur_index - 1], '%Y-%m-%d %H:%M:%S')
	#print(curdate, previousdate, nextdate)
	#exit()
	#print(curdate.month, previousdate.month, nextdate.month)
	#exit()
	if curdate.month != cur_month:
		cur_month += 1
		indexes.append((start, cur_index))
		start_index = cur_index + 1
		start = cur_index + 1
		end = start_index + add_const
	else:
		start_index = cur_index
	#print(start, end)
	#print(log_arr[start])
	#exit()
for item in indexes:
	print(item)
