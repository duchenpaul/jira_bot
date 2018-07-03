import jira_bot
import toolkit_sqlite

nameDict = {
	'Chenny': 'chdu',
	'Karl': 'klcen',
}


if __name__ == '__main__':
	jira = jira_bot.Jira(jira_bot.username, jira_bot.password)
	jira.login_w_pass()
	for task in toolkit_sqlite.query_task():
		print(task)
		labelList = []
		summary = '[{}] {}'.format(task[2], task[1])

		assignee = nameDict.get(task[5])
		# print(assignee)
		# print(summary)
		description = '''*Job Group:* {}\n*Workflow/SP:* {}\n*Type:* {}\n*Database:* {}\n*DEV:* {}\n*Code change Status:* {}\n*Unit test status:* {}\n*Description:* 	{}\n'''.format(task[0], task[1], task[2], task[4], task[5], task[6], task[7], task[8])
		labelList.append(task[2])
		jira.create_ticket(10000, 10002, summary, description, priority = '3', reporter = jira_bot.username, assignee = assignee, labelList = labelList)