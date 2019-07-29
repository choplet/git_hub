import sys
from datetime import date, datetime
from _auto import storage
import sqlite3
get_connection = lambda: storage.connect('auto.sqlite')


def readImage(filename):
	fin = open(filename, "rb")
	img = fin.read()
	return img


def action_show_menu():
	print('''
1. Добавить авто
2. Авто в парке за указанный период
m. Показать меню
q. Выход
#Вывод даты происходит в фрмате год.месяц.день
		''')


def action_add_auto():
	id = input("\nВведите VIN ")

	created = datetime.strptime(input('\nДата введения в эксплуатацию в формате день.месяц.год '), "%d.%m.%Y")
	crashed = datetime.strptime(input('\nДата утилизации в формате день.месяц.год '), "%d.%m.%Y")

	photo = input("\nПереместите файл в директорию pts и введите название файла с расширением ")
	data = readImage('pts/{}'.format(photo))
	pts = sqlite3.Binary(data)

	with get_connection() as conn:
		added_task = storage.add(conn, id, created, crashed, pts, photo)
		print('Авто "{}" добавлено '.format(
			id))


def main():
	with get_connection() as conn:
		storage.initialize(conn)

	actions = {
	"1": action_add_auto,
	"2": action_find_date,
	"m": action_show_menu,
	"q": action_exit
	}

	action_show_menu()

	while 1:
		cmd = input('Введите команду ')
		action = actions.get(cmd)

		if action:
			action()
		else:
			print('Не известная команда')


def action_find_date():
	first_date = datetime.strptime(input('Введите первую дату промежутка '), "%d.%m.%Y")
	second_date = datetime.strptime(input('Введите вторую дату промежутка ' ), "%d.%m.%Y")

	if first_date > second_date:
		raise Exception('Неверно задан промежуток')

	with get_connection() as conn:
		print('''
VIN -    Дата выпуска     -   Дата утилизации   - Фото ПТС
_______________________________________________________
		''')

		find_date = storage.find_date(conn,first_date,second_date)
		for date in find_date:
			template = '{date[id]} - {date[created]} - {date[crashed]} - {date[photo]} '
			print(template.format(date=date))


def action_exit():
	'''Выход'''
	sys.exit(0)
