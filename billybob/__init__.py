#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import time
from slackclient import SlackClient
from wit import Wit


class BillyBob:

    def wit_send(self, request, response):
        print 'Sending to user... {0}'.format(response['text'])

    def wit_get_prs(self, params):
        print 'requested get_prs ! {0}'.format(params)
        self.slack_client.api_call("chat.postMessage",
                                   channel=params['context']['chan'].encode("ascii","ignore"),
                                   text='requested get_prs !',
                                   as_user=True)
        return {}

    def wit_get_bus_tt(self, params):
        print 'requested get_bus_tt ! {0}'.format(params)
        self.slack_client.api_call("chat.postMessage",
                                   channel='G3FS40MFA',
                                   text='requested get_bus_tt !',
                                   as_user=True)
        return {}

    def __init__(self, slack_token=None, wit_token=None, **kargs):
        self.BOT_NAME = 'BillyBob'
        self.BOT_ID = 'U1ZUKEDT4'
        if slack_token is None:
            self.slack_token = os.environ['SLACK_API_TOKEN']
        else:
            self.slack_token = slack_token
        if wit_token is None:
            self.wit_token = os.environ['WIT_API_TOKEN']
        else:
            self.wit_token = wit_token
        self._params = kargs
        if 'wit_actions' in kargs:
            actions = kargs['wit_actions']
        else:
            actions = {
                'send': self.wit_send,
                'get_prs': self.wit_get_prs,
                'get_bus_tt': self.wit_get_bus_tt
            }
        logging.basicConfig(format='%(asctime)s %(levelname)s '
                                   '[%(filename)s:%(lineno)d] %(message)s')
        self.slack_client = SlackClient(self.slack_token)
        self.wit_client = Wit(access_token=self.wit_token, actions=actions)

    def _parse_slack_output(self, slack_rtm_output):
        at_bot = "<@{0}>".format(self.BOT_ID)
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                print 'command: {0}'.format(output)
                if output and 'text' in output and at_bot in output['text']:
                    cmd = output['text'].split(at_bot)[1].strip().lower()
                    chan = output['channel']
                    print 'detected cmd: {0}'.format(cmd)
                    return cmd, chan
        return None, None

    def handle_command(self, command, chan):
        self.wit_client.run_actions('titoi', command, {'chan': chan})

    def start_service(self):
        print 'Waking up {0}...'.format(self.BOT_NAME)
        if self.slack_client.rtm_connect():
            print '{0} is connected !'.format(self.BOT_NAME)
            while True:
                read_payload = self.slack_client.rtm_read()
                command, chan = self._parse_slack_output(read_payload)
                if command:
                    self.handle_command(command, chan)
                time.sleep(1)
        else:
            print "Connection failed. Invalid Slack token or bot ID?"
