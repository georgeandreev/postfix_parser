import re


class Parser(object):
	buff = {}
	list_of_mails = {}

	INIT_PATTERN = "([ABCDEF0-9]{11})\:\s.+sasl_username\=(\S+)"
	FROM_PATTERN = "([ABCDEF0-9]{11})\:\sfrom\=<(\S+)>"
	TO_PATTERN = "([ABCDEF0-9]{11})\:\sto\=<(\S+)>.+status\=(\S+)"
	REMOVED_PATTERN = "([ABCDEF0-9]{11})\:\sremoved"


	def __init__(self, log_path):
		super(Parser, self).__init__()
		self.log_path = log_path


	def parse_str(self, s):
		groups = re.search(self.INIT_PATTERN, s)
		if groups:
			groups = groups.groups()
			t = 0
			mail_id = groups[0]
			self.add_to_buffer(mail_id, groups)
			return t
		groups = re.search(self.FROM_PATTERN, s)
		if groups:
			groups = groups.groups()
			t = 1
			mail_id = groups[0]
			self.add_to_mail(mail_id, t, groups)
			return t
		groups = re.search(self.TO_PATTERN, s)
		if groups:
			groups = groups.groups()
			t = 2
			mail_id = groups[0]
			self.add_to_mail(mail_id, t, groups)
			return t
		groups = re.search(self.REMOVED_PATTERN, s)
		if groups:
			groups = groups.groups()
			t = 3
			mail_id = groups[0]
			self.remove_buff(mail_id)
			return t


	def add_to_buffer(self, mail_id, groups):
		self.buff[mail_id] = {'groups': []}
		self.buff[mail_id]['groups'].append([groups, 0])


	def remove_buff(self, mail_id):
		if mail_id in self.buff.keys():
			self.list_of_mails[mail_id] = self.buff[mail_id]['groups']
			del(self.buff[mail_id])


	def add_to_mail(self, mail_id, t, groups):
		if mail_id in self.buff.keys():
			self.buff[mail_id]['groups'].append([groups, t])


class Logical(Parser):
	mails = {}


	def __init__(self, log_path):
		super(Logical, self).__init__(log_path)


	def get_all_mails_info(self):
		for mail_id in self.list_of_mails:
			self.get_mail_info(mail_id)


	def get_mail_info(self, mail_id):
		groups = self.list_of_mails[mail_id]
		mail_info = []
		tries_count = 0
		statuses = []
		for group in groups:
			params = group[0]
			t = group[1]
			if t == 0:
				mail_from = params[1]
			elif t == 2:
				tries_count += 1
				mail_to = params[1]
				status = params[2]
				statuses.append(status)
		mail_info = [mail_id, mail_from, mail_to, tries_count, statuses]
		self.mails[mail_id] = mail_info


class SimpleReport(Logical):
	info = {}


	def __init__(self, log_path):
		super(SimpleReport, self).__init__(log_path)


	def get_all_info(self):
		for mail_id in self.mails:
			self.get_info(mail_id)


	def get_info(self, mail_id):
		mail = self.mails[mail_id]
		mail_from = mail[1]
		mail_to = mail[2]
		full_tries = mail[3]
		statuses = mail[4]
		statuses_info = {}
		for status in statuses:
			if not status in statuses_info.keys():
				statuses_info[status] = 0
			statuses_info[status] += 1
		final_status = statuses[-1]
		info = ""
		info += "Mail id: %s\n" % (mail_id)
		info += "Sender e-mail: %s\n" % (mail_from)
		info += "Reciever e-mail: %s\n" % (mail_to)
		info += "Statuses statistics:\n"
		for status in statuses_info:
			info += "	%s - %s\n" % (status, str(statuses_info[status]))
		info += "Final status: %s" % (statuses[-1])
		info = "%s %s %s %s" % (mail_id, mail_from, mail_to, final_status)
		self.info[mail_id] = info
		return info
	

if __name__ == '__main__':
	p = SimpleReport('maillog')
	f = open('maillog', 'r')
	line = '_'
	while line:
		line = f.readline()
		p.parse_str(line)
	f.close()
	p.get_all_mails_info()
	p.get_all_info()
	for item in p.info:
		print(p.info[item])
	# print(list(p.mails.keys())[0])
	# print(p.get_info('38126DF05B1'))
