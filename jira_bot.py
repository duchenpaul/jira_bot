import requests
from requests import Request, Session
import urllib.parse

import os.path 
from os.path import dirname, abspath
import json, configparser

configFILE = "config_test.ini"

SCRIPT_PATH = dirname(abspath(__file__)) + '/'

try:
	print('Read config file: ' + configFILE )
	configRead = configparser.ConfigParser()
	configRead.read(configFILE)

	sectionName = 'jira_account'
	options = [ i.upper() for i in configRead.options(sectionName) ]
	config = {}
	for j in options:
		config[j] = configRead[sectionName][j]

except Exception as e:
	print("Error read config file, check config.ini")
	print(e)
	raise

jiraUrl = config['JIRA_URL']
username = config['USERNAME']
password = config['PASSWORD']


class Jira():
	headers_default = {
		'Host': '{}'.format(jiraUrl), 
		'Connection': 'keep-alive', 
		'Upgrade-Insecure-Requests': '1', 
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36', 
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 
		'Accept-Encoding': 'gzip, deflate', 
		'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7', 
		}

	cookies_dict = {}

	def __init__(self, username, password):
		self.Sess = requests.session()
		self.username = username
		self.password = password
		self.cookie_file = SCRIPT_PATH + 'cookies_{}.txt'.format(self.username)
		# print(self.cookie_file)


	def webpage_get(self, url, headers=headers_default):
		# print("Get: " + url)
		self.resp = self.Sess.get(url, headers=headers)		
		return self.resp

	def webpage_post(self, url, data, headers=headers_default):
		self.req = Request('POST', url, data=data, headers=headers)
		self.prepped = self.Sess.prepare_request(self.req)
		self.resp = self.Sess.send(self.prepped)
		return self.resp


	def login_w_pass(self):
		self.url = 'http://{}/rest/gadget/1.0/login'.format(jiraUrl)  
		data = {
			'os_username': self.username,
			'os_password': self.password,
			'os_cookie': 'true',
		}

		self.data = urllib.parse.urlencode(data)
		self.headers = {
			'Host': '{}'.format(jiraUrl), 
			'Connection': 'keep-alive', 
			'Accept': '*/*', 
			'Origin': 'http://{}'.format(jiraUrl), 
			'X-Requested-With': 'XMLHttpRequest', 
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36', 
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
			'Referer': 'http://{}/secure/Dashboard.jspa'.format(jiraUrl), 
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7', 
		}

		print('Login Jira with {}'.format(self.username))
		self.resp = self.webpage_post(self.url, self.data, self.headers)
		self.login_rtn_page = self.resp.content.decode('utf-8')

		# print(self.login_rtn_page)
		if '''"loginSucceeded":true''' in self.login_rtn_page:
			print('Authentication succeed!')
			self.cookies_dict.update(self.resp.cookies)
			# with open(self.cookie_file, 'w') as f:
			# 	f.write(str(self.cookies_dict))
		else:
			print('Authentication failed!')

	def create_ticket(self, pid,
							issuetype,
							summary,
							description,
							priority = '3',
							reporter = username,
							assignee = '',
							labelList = [] ):
		'''
		pid: Project ID
		issuetype: 10002 - task,
		summary: title
		reporter: reporter default username
		description: description
		priority: 3 medium
		dnd-dropzone: attachment
		issuelinks
		issuelinks-linktype
		labelList: list
		assignee: assignee
		'''
		new_url = 'http://{}/secure/QuickCreateIssue!default.jspa?decorator=none'.format(jiraUrl)
		url = 'http://{}/secure/QuickCreateIssue.jspa?decorator=none'.format(jiraUrl)

		headers = {
			'Host': '{}'.format(jiraUrl), 
			'Connection': 'keep-alive', 
			'Accept': '*/*', 
			'Origin': 'http://{}'.format(jiraUrl), 
			'X-Requested-With': 'XMLHttpRequest', 
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36', 
			'X-AUSERNAME': self.username, 
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
			'Referer': 'http://{}/secure/Dashboard.jspa'.format(jiraUrl), 
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7', 

		}

		resp = self.webpage_post(new_url, headers)
		respJson = json.loads(resp.content.decode('utf-8'))
		formToken = respJson['formToken']

		jira_data = {
			'atl_token': self.cookies_dict['atlassian.xsrf.token'],
			'formToken': formToken,
		}

		custom_data = {
			'pid': str(pid),
			'issuetype': str(issuetype),
			'summary': summary,
			'reporter': self.username,
			'description': description,
			'priority': str(priority),
			'dnd-dropzone': '',
			'issuelinks': 'issuelinks',
			'issuelinks-linktype': 'blocks',
			'assignee': assignee,
		}

		g = lambda x: 'labels=' + urllib.parse.quote_plus(x)
		data = '&'.join([urllib.parse.urlencode(jira_data), urllib.parse.urlencode(custom_data), ] + list(map(g, labelList)))
		# print(data)

		resp = self.webpage_post(url, data, headers)
		respJson = json.loads(resp.content.decode('utf-8'))
		issueKey = respJson['issueKey']
		if issueKey:
			print('Ticket has been creaeted as {}'.format(issueKey))
		else:
			print("Failed to create ticket.")




if __name__ == '__main__':
	jira = Jira(username, password)
	jira.login_w_pass()
	jira.create_ticket(10000, 10002, 'summarySP', 'descriptionSP', priority = '3', reporter = username, assignee = '', labelList = ['test', 'SP'] )
	jira.create_ticket(10000, 10002, 'summaryworkflow', 'descriptionworkflow', priority = '3', reporter = username, assignee = '', labelList = ['test', 'workflow'] )