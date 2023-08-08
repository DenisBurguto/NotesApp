import time
import uuid
import json
from datetime import datetime
from json import JSONDecodeError
from pprint import pprint


def add():
    out_dict = dict()
    out_dict['id'] = str(uuid.uuid4())
    out_dict['title'] = (input("please enter note title \n:"))
    out_dict['message'] = (input('please enter your message \n:'))
    out_dict['datetime'] = datetime.now().strftime("%Y %m %d %H %M")
    try:
        with open('notes_db.json', 'r', encoding='utf8') as file:
            try:
                data = json.load(file)
                data['notes'].append(out_dict)
            except JSONDecodeError:  # empty file case
                data = {'notes': [out_dict]}

        with open('notes_db.json', 'w', encoding='utf8') as outfile:
            json.dump(data, outfile)
    except IOError:  # file missing case
        with open('notes_db.json', 'w', encoding='utf8') as outfile:
            data = {'notes': [out_dict]}
            json.dump(data, outfile)
    print("successfully added, return to menu")


def mylist():
    try:
        with open('notes_db.json', 'r', encoding='utf8') as file:
            data = json.load(file)
            if input("would you like to use datetime filter? \033[3m\033[33myes/no\033[0m \n:") == 'no':
                pprint(data)
                print("we will return to menu now")
            else:
                try:
                    start = int(
                        input('enter start date and time \033[3m\033[33myyyy mm dd  HH MM\033[0m \n:').replace(" ", ''))
                    end = int(
                        input('enter end date and time \033[3m\033[33myyyy mm dd  HH MM\033[0m \n:').replace(" ", ''))
                    for note in data['notes']:
                        if start <= int(note['datetime'].replace(" ", '')) <= end:
                            print(note)
                            print("we will return to menu now")

                except TypeError:
                    print("wrong date time input, return to menu")

    except JSONDecodeError:  # empty file case:
        print("there is no any note in your list")


def find(keyword):
    try:
        with open('notes_db.json', 'r', encoding='utf8') as file:
            data = json.load(file)
            found = False
            for note in data['notes']:
                if note['title'].find(keyword) > -1 or note['message'].find(keyword) > -1:
                    print(f"we found next note with {keyword} {note}")
                    found = True
            print("return to menu" if found else "nothing found, return")
    except JSONDecodeError:  # empty file case:
        print("there is no any note in your list")


def edit(note_id):
    try:
        with open('notes_db.json', 'r', encoding='utf8') as file:
            data = json.load(file)
            changed = False
            for note in data['notes']:
                if note['id'].replace('-', '').find(note_id) > -1:
                    print(f"we found next note with id {note_id} {note}")

                    match input("what do you like to edit, title or message?  \033[3m\033[33mt/m\033[0m \n:"):
                        case 't':
                            note['title'] = input("enter new title \n:")
                            changed = True
                        case 'm':
                            note['message'] = input("enter new message \n:")
                            changed = True
                        case _:
                            print('wrong input')
                    break  # id is unique

        if changed:
            match input(f"final note is{note}, save? \033[3m\033[33myes/no\033[0m \n: "):
                case 'yes':
                    with open('notes_db.json', 'w', encoding='utf8') as outfile:
                        json.dump(data, outfile)
                        print('saved, return')
                case _:
                    print('return without saving changes')
        else:
            print("no such id found or nothing to save, return to menu")

    except JSONDecodeError:  # empty file case:
        print("there is no any note in your list")


def delete(note_id):
    try:
        with open('notes_db.json', 'r', encoding='utf8') as file:
            data = json.load(file)
            deleted = False
            for note in data['notes']:
                if note['id'].replace('-', '').find(note_id) > -1:
                    print(f"we found next note with id {note_id} {note}")
                    match input("Are you sure to delete it?  \033[3m\033[33myes/no\033[0m \n:"):
                        case 'yes':
                            data['notes'].remove(note)
                            deleted = True
                        case 'no':
                            print('canceling..')
                        case _:
                            print('wrong input')
                    break  # id is unique

        if deleted:
            with open('notes_db.json', 'w', encoding='utf8') as outfile:
                json.dump(data, outfile)
                print('deleted, return')
        else:
            print("no such id found or delete canceled, return to menu")

    except JSONDecodeError:  # empty file case:
        print("there is no any note in your list")


def menu():

    try:     # case file with database missing:
        with open('notes_db.json', 'a', encoding='utf8') as file:
            print("database connected successfully, possible commands:")
    except FileNotFoundError:
        print("no file found")

    print('\033[3m\033[33madd\033[0m #to add new note')
    print('\033[3m\033[33mmylist\033[0m  #to get list  notes submenu')
    print('\033[3m\033[33mfind -keyword\033[0m  #to search in notes by keyword')
    print('\033[3m\033[33medit -id\033[0m #to edit note by id(part of id)')
    print('\033[3m\033[33mdelete -id\033[0m #to delete  note by id(part of id)')
    print('\033[3m\033[33mexit\033[0m #to close the program')
    command = input('enter your command \n:').lower().replace('-', '').split()
    try:
        if command[0] == 'add':
            add()
        elif command[0] == 'mylist':
            mylist()
        elif command[0] == 'find':
            find(command[1])
        elif command[0] == 'edit':
            edit(command[1])
        elif command[0] == 'delete':
            delete(command[1])
        elif command[0] == 'exit':
            exit(0)
        else:
            print('incorrect command, try again')
    except IndexError:
        print('incorrect command, try again')


while True:
    menu()
    time.sleep(1)
