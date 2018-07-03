import os
import os.path
import glob

def get_basename(FILE):
	'''
	Return the basename of a file. e.g. example.txt -> example
	'''
	return os.path.splitext(os.path.basename(FILE))[0]

def file_path(FILE):
	return os.path.dirname(os.path.realpath(FILE)) + os.sep

def script_path():
	return os.path.dirname(os.path.realpath(__file__))

def line_prepender(filename, line):
	'''
	Add line to the head of a file
	'''
	with open(filename, 'r+') as f:
		content = f.read()
		f.seek(0, 0)
		f.write(line.rstrip('\r\n') + '\n' + content)

def get_file_list(dirname):
	file_list = []
	for i in os.walk(dirname):
		if not i[1]:
			for j in i[2]:
				file_list.append(''.join(str(i[0]) + os.sep + j))
	return file_list

def purge_folder(folder):
	# filelist = [ f for f in os.listdir(folder) ] #if f.endswith(".bak") ]
	filelist = glob.glob(folder + os.sep + '*')
	for f in filelist:
		print(f)
		# os.remove(os.path.join(f)) # using glob
		# os.remove(os.path.join(folder, f)) # using listdir

if __name__ == '__main__':
	print(get_file_list('E:\\'))