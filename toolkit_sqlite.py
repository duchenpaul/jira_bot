import logging
import json
import sqlite3
import toolkit_file
import config

DB_FILE = config.Sqlitedb

class _sqlitedb():
	"""docstring for _sqlitedb"""
	def __init__(self, DB_FILE):
		self.conn = sqlite3.connect(DB_FILE)

	def __enter__(self):
		return self

	def __exit__(self,Type, value, traceback):  
		'''
		Executed after "with"
		'''
		print('Close the DB')
		self.cursor.close()
		
	def query(self, sql):
		self.cursor = self.conn.cursor()
		try:
			self.cursor.execute(sql)
			result = self.cursor.fetchall()
		except Exception as e:
			logging.error("sqlite query error: %s", e)
			return None
		finally:
			self.cursor.close()
		return result

	def execute(self, sql):
		self.cursor = self.conn.cursor()
		affected_row = -1
		try:
			self.cursor.execute(sql)
			self.conn.commit()
			affected_row = self.cursor.rowcount
		except Exception as e:
			logging.error("sqlite execute error: %s", e)
			return 0
		finally:
			print('affected_rows: ' + str(affected_row) )
			self.cursor.close()
		return affected_row

	def executemany(self, sql, params = None):
		self.cursor = self.conn.cursor()
		affected_rows = 0
		try:
			self.cursor.executemany(sql, params)
			self.conn.commit()
			affected_rows = self.cursor.rowcount
		except Exception as e:
			logging.error("sqlite executemany error: %s", e)
			return 0
		finally:
			self.cursor.close()
			print('affected_rows: ' + str(affected_rows) )
		return affected_rows

	def load_json(self, JSON_FILE, tableName = None):
		'''
		Load file into sqlite
		'''
		if not tableName:
			tableName = toolkit_file.get_basename(JSON_FILE)

		with open(JSON_FILE, 'r') as f:
			dicSet = json.load(f)

		print('Load json {} to table {}'.format(JSON_FILE, tableName))
		tupleList = []
		columnNames = list(dicSet[0].keys())
		columnNamesSqlJoined = ', '.join(map(lambda x: '`' + x + '`', columnNames))

		for dic in dicSet:
			tupleList.append(tuple(dic.values()))

		insertSql = "INSERT INTO {} ({}) VALUES(?{});".format(tableName, columnNamesSqlJoined, ',?'*(len(tupleList[0]) - 1))

		self.executemany(insertSql, tupleList)

def query_task():
	with _sqlitedb(DB_FILE) as sqlitedb:
		return sqlitedb.query('select * from Status_sheet;')


if __name__ == '__main__':
	create_view = '''CREATE TABLE IF NOT EXISTS `work_todo11` as select * from Status_sheet '''
	truncate_table = '''DELETE FROM `test` '''
	drop_table = '''DROP TABLE `work_todo11` '''
	# sqlitedb = _sqlitedb(DB_FILE)

	# with _sqlitedb(DB_FILE) as sqlitedb:
	# 	# print(sqlitedb.query('select * from Status_sheet'))
	# 	# sqlitedb.execute(create_view)
	# 	sqlitedb.execute(truncate_table)
	# 	sqlitedb.load_json(JSON_FILE, 'test')
	# 	# sqlitedb.executemany(batch_insert, tupleList)
	# 	# sqlitedb.execute(drop_table)

	query_task()