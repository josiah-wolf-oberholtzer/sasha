#! /usr/bin/env python

import json
import os
from ConfigParser import ConfigParser


def remap_event_data(old_data):
    new_data = {}
    new_data['fingering'] = old_data['fingering.instrument_keys.name'].split()
    new_data['instrument'] = old_data['instrument.name']
    new_data['name'] = old_data['name']
    new_data['performer'] = old_data['performer.name']
    return new_data


def remap_instrument_data(old_data):
    new_data = {}
    if 'instrument_keys.name' in old_data:
        new_data['key_names'] = old_data['instrument_keys.name'].split()
    new_data['name'] = old_data['name']
    if 'parent.name' in old_data:
        new_data['parent'] = old_data['parent.name']
    if 'transposition' in old_data:
        new_data['transposition'] = old_data['transposition']
    return new_data


def remap_performer_data(old_data):
    new_data = {}
    new_data['name'] = old_data['name']
    return new_data


def make_json_fixtures(directory, remap_function):
    for ini_file_name in os.listdir(directory):
        if not ini_file_name.endswith('.ini'):
            continue
        ini_file_path = os.path.join(directory, ini_file_name)
        config = ConfigParser()
        with open(ini_file_path, 'r') as file_pointer:
            config.readfp(file_pointer)
        old_data = dict(config.items('main'))
        new_data = remap_function(old_data)
        new_contents = json.dumps(new_data, indent=4, sort_keys=True)
        print(new_contents)
        json_file_name = os.path.splitext(ini_file_name)[0] + '.json'
        json_file_path = os.path.join(directory, json_file_name)
        with open(json_file_path, 'w') as file_pointer:
            file_pointer.write(new_contents)


fixtures_directory = os.path.abspath(os.path.curdir)
events_directory = os.path.join(fixtures_directory, 'events')
instruments_directory = os.path.join(fixtures_directory, 'instruments')
performers_directory = os.path.join(fixtures_directory, 'performers')

make_json_fixtures(events_directory, remap_event_data)
make_json_fixtures(instruments_directory, remap_instrument_data)
make_json_fixtures(performers_directory, remap_performer_data)