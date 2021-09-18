from random import shuffle, random
import config
import ctypes
import time
import os

CONFIG = config.get()

DEF_PATH = CONFIG.get('Directory').get('path') + '\\%s\\' % CONFIG.get('Directory').get('folder')

if str(CONFIG.get('Settings').get('standby_time')).isdigit() == False:
	raise ValueError('Время указанное в конфиге SETTINGS не является числом')
elif CONFIG.get('Settings').get('standby_time') < CONFIG.get('Constants').get('threshold_time'):
	raise ValueError('Нельзя указывать время меньше %d секунд' % CONFIG.get('Constants').get('threshold_time'))

if CONFIG.get('Settings').get('shift_mode') not in [*range(0, 2 + 1)]:
	raise ValueError('Указа неверный режим работы, доступны следующие режимы работы: %s' % ', '.join(map(str, [*range(0, 2 + 1)])))

def get_list(path = DEF_PATH):
	if os.path.exists(path) == True:
		ext = CONFIG.get('Constants').get('extensions').split(', ')
		array = []
		for (dirpath, dirnames, filenames) in os.walk(path):
			for file in filenames:
				if file.split('.')[1] in ext:
					array.append(file)
		if not array:
			raise FileNotFoundError('Дериктория %s пустая, для работы требуется наличие файлов изображения (%s)' % (CONFIG.get('Directory').get('folder').upper(), ', '.join(ext)))
		elif len(array) <= 1:
			raise IOError('Для работы требуется добавить 2 и более файлов')
		return array
	else:
		raise FileNotFoundError('Для работы программы требуется наличие папки %s' % CONFIG.get('Directory').get('folder').upper())
		return False

def exist(path = DEF_PATH, filename = None):
	if not filename:
		print('*** Название файла не было указано!')
		return False
	if os.path.exists(path + filename) is True:
		return True
	else:
		return False

def get_file(imgs, mode = 1):
	if mode == 0:
		imgs = sorted(imgs, key=lambda A: random())
		for item in imgs:
			yield item
	else:
		if mode == 2:
			imgs = sorted(imgs, reverse=True)
		for item in imgs:
			yield item

def change_wallpaper(filename, path = DEF_PATH):
	if exist(filename = filename) == True:
		return ctypes.windll.user32.SystemParametersInfoW(0x14, 0, DEF_PATH + filename, 10)
		# ctypes.windll.user32.SystemParametersInfoW(20, 0, DEF_PATH + filename, 0)
	else:
		return False

def check_for_update(list, path = DEF_PATH):
	if os.path.exists(path) == True:
		ext = CONFIG.get('Constants').get('extensions').split(', ')
		array = []
		for (dirpath, dirnames, filenames) in os.walk(path):
			for file in filenames:
				if file.split('.')[1] in ext:
					array.append(file)
		matches = 0
		if len(array) > len(list) < len(array):
			return True
		else:
			for primal in list:
				if primal not in array:
					matches += 1
			if matches > 0:
				return True
			else:
				return False
	else:
		raise FileNotFoundError('Для работы программы требуется наличие папки %s' % CONFIG.get('Directory').get('folder').upper())
		return False

def main():
	images = get_list()
	content = get_file(images, CONFIG.get('Settings').get('shift_mode'))
	index = None
	print('* Папка с изображениями: %s' % CONFIG.get('Directory').get('folder'))
	print('* Количество: %s' % len(images))
	print()
	while True:
		time.sleep(CONFIG.get('Settings').get('standby_time'))
		if check_for_update(images):
			print('** Зафиксировано изменения списков изображений, ввожу коррективы.')
			images = get_list()
		try:
			index = next(content)
		except StopIteration:
			content = get_file(images, CONFIG.get('Settings').get('shift_mode'))
			index = next(content)
		print('* Установлены новые обои', index)
		change_wallpaper(index)

if __name__ == '__main__':
	main()