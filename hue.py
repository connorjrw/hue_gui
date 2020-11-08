#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 22:20:49 2020

@author: con
"""

import requests
import time
import random
import os
from pathlib import Path
import json


from custom_errors import GenericHueError, LinkButtonNotPressedError, UnauthorizedUserError


class Bridge:
    def __init__(self):
        self.ipaddress = ''
        self.userid = ''

    def get_lights(self):
        """
        Get all lights connected to bridge
        """
        api_string = self.ipaddress + 'api/' + self.userid + '/lights'
        resp = requests.get(api_string)
        if resp.status_code != 200:
            raise Exception(api_string, resp.status_code) from None
        else:
            return resp.json()

    def set_state(self, task, light):
        """
        Set state of light
        """
        api_string = self.ipaddress + 'api/' + self.userid + '/lights/' + str(light) + '/state'
        resp = requests.put(api_string, json=task)
        # when response is blank it failed!
        try:
            json_error_details = resp.json()[0]['error']
            self.error_handler(json_error_details)
        except KeyError:
            if resp.status_code != 200:
                raise Exception(api_string, resp.status_code) from None  # Improve

    def get_ip_address(self):
        resp = requests.get('https://discovery.meethue.com/')
        return 'http://' + resp.json()[0]['internalipaddress'] + '/'

    def create_user(self):
        """
        Register new user on Bridge, returns username if successful
        """
        api_string = self.ipaddress + 'api'
        resp = requests.post(api_string, json={'devicetype': 'philip'})
        if 'error' in resp.json()[0]:
            self.error_handler(resp.json()[0]['error'])
        else:
            return resp.json()[0]['success']['username']

    def get_state(self, light):
        """
        Gets state of light
        """
        api_string = self.ipaddress + 'api/' + self.userid + '/lights/' + str(light)
        resp = ''
        try:
            resp = requests.get(api_string)
            return resp.json()['state']
        except TypeError:
            json_error_details = resp.json()[0]
            if 'error' in resp.json()[0]:
                print(json_error_details)
                self.error_handler(json_error_details['error'])
        except requests.exceptions.MissingSchema:
            return {}

    def check_connection(self, ip_add, user_id):
        api_string = ip_add + 'api/' + user_id
        status = True
        try:
            resp = requests.get(api_string)
            if type(resp.json()) is list:
                if 'error' in resp.json()[0]:
                    status = False
        except requests.exceptions.MissingSchema:
            status = False
        finally:
            return status

    def connected(self):
        return self.check_connection(self.ipaddress, self.userid)

    def connect(self):
        config_path = os.getenv('HOME') + '/hue/'
        try:
            with open(config_path + 'config.txt') as json_file:
                data = json.load(json_file)
                if self.check_connection(data['ip_address'], data['user_id']):
                    self.ipaddress = data['ip_address']
                    self.userid = data['user_id']
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            if not Path.exists(Path(config_path)):
                os.mkdir(config_path)
            self.ipaddress = self.get_ip_address()
            self.userid = self.create_user()
            json_config = {
                "ip_address": self.ipaddress,
                "user_id": self.userid
                }
            self.ipaddress = self.ipaddress
            self.userid = self.userid
            with open(config_path + 'config.txt', 'w') as outfile:
                json.dump(json_config, outfile)

    def error_handler(self, json_error_details):
        if json_error_details['type'] == 1:
            raise UnauthorizedUserError
        elif json_error_details['type'] == 101:
            raise LinkButtonNotPressedError
        else:
            raise GenericHueError(json_error_details)


class Light:
    def __init__(self, bridge, light_id):
        self.speed = 0
        self.userid = bridge.userid
        self.ipaddress = bridge.ipaddress
        self.light_id = light_id
        self.bridge = bridge
        self.strobe = False

    def get_status(self):
        return self.bridge.get_state(self.light_id)

    def on(self):
        task = {'on': True}
        self.bridge.set_state(task, self.light_id)

    def off(self):
        task = {'on': False}
        self.bridge.set_state(task, self.light_id)

    def brightness(self, percent):
        task = {"bri": percent}
        self.bridge.set_state(task, self.light_id)

    def strobe_start(self, colors, speed, is_random):
        prev_color = ''
        self.strobe = True
        self.speed = speed
        while self.strobe and self.speed < 4.5:
            if is_random:  # Needs to be cleaned up to match non-random
                new_colors = colors[:]
                if prev_color != '':
                    new_colors.remove(prev_color)
                    prev_color = random.choice(new_colors)
                    self.color(prev_color)
                    time.sleep(int(self.speed))
            else:
                color_index = 0
                while color_index < len(colors) and self.speed < 4.5:
                    self.color(colors[color_index])
                    prev_speed = self.speed
                    no_itr = self.speed / 0.1
                    for i in range(int(no_itr)):
                        if prev_speed != self.speed:
                            break
                        time.sleep(0.1)
                    if self.speed == prev_speed:
                        color_index += 1
                    elif color_index == len(colors) - 1:
                        color_index = 0

    def strobe_stop(self):
        self.strobe = False

    def strobe_speed(self, speed):
        self.speed = speed

    def color(self, color):
        colors = {'blue': [0.154, 0.0806], 'red': [0.6661, 0.296], 'green': [0.1945, 0.6816],
                  'purple': [0.2337, 0.1167], 'pink': [0.4511, 0.1996], 'orange': [0.6455, 0.3428],
                  'yellow': [0.4701, 0.4746], 'lightblue': [0.1577, 0.2217]}
        try:
            task = {"xy": colors[color]}
            self.bridge.set_state(task, self.light_id)
        except KeyError:
            raise ValueError('Color does not exist') from None
