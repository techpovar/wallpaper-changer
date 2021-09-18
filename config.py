try:
	import configparser
except ImportError:
	import ConfigParser as configparser
import os

default_filename = 'settings.ini'

data = {
	'Settings': {
		'standby_time': 120,
		'shift_mode': 0
	},
	'Directory': {
		'folder': 'images',
		'path': os.path.dirname(os.path.abspath(__file__))
	},
	'Constants': {
		'threshold_time': 30,
		'extensions': 'jpg, jpeg, png'
	}
}

def create_new(filename = default_filename):
	config = configparser.ConfigParser()
	for chapter in data:
		config.add_section(str(chapter))
		for key in data.get(chapter):
			config.set(str(chapter), str(key), str(data.get(chapter).get(key)))
	with open(filename, 'w') as config_file:
		config.write(config_file)
		config_file.close()
	return data

def read_config(filename = default_filename):
	config = configparser.ConfigParser()
	config.read(filename)
	array = {}
	for chapter in data:
		for key in data.get(chapter):
			if chapter not in dict(config):
				raise KeyError('Критическая ошибка: не обнаружен раздел %s' % str(chapter).upper())
			if key not in dict(dict(config).get(chapter)):
				raise KeyError('Критическая ошибка: не обнаружен ключ %s' % str(key).upper())
			if config.get(str(chapter), str(key)):
				_ = str(config.get(str(chapter), str(key)))
				if _.isdigit() != str(data.get(chapter).get(key)).isdigit():
					raise KeyError('Критическая ошибка: ключ %s содержит неправильное значение!' % str(key).upper())
				if array.get(chapter):
					array[str(chapter)][str(key)] = int(_) if _.isdigit() else _
				else:
					array[str(chapter)] = {str(key): int(_) if _.isdigit() else _}
	return array

def get(filename = default_filename):
	if not os.path.exists(filename):
		return create_new()
	else:
		return read_config()