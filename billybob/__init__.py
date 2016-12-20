#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import time
import sophiabus230
import datetime
from dateutil.tz import gettz
from slackclient import SlackClient
from wit import Wit


class BillyBob:
    def wit_send(self, request, response):
        print 'Sending to user... {0}'.format(response['text'])

    def _post_simple(self, channel, msg):
        self.slack_client.api_call("chat.postMessage",
                                   channel=channel,
                                   text=msg,
                                   as_user=True)

    def _post_fmt(self, channel, msg):
        self.slack_client.api_call("chat.postMessage",
                                   channel=channel,
                                   text="Here are the next bus passages !",
                                   attachments=msg,
                                   as_user=True)

    def _check_intent(self, intent, key_intent):
        return intent['entities'] and intent['entities'][key_intent]

    def wit_get_prs(self, params):
        chan = params['context']['chan'].encode("ascii", "ignore")
        print 'requested get_prs ! {0}'.format(params)
        if self._check_intent(params, 'pull_request'):
            entities = params['entities']['pull_request']
            if len(entities) == 1 and entities[0]['value']:
                repo = entities[0]['value']
                if repo == 'github':
                    self._post_simple(chan, 'You asked for the PRs from github')
                elif repo == 'bitbucket':
                    self._post_simple(chan, "Sorry bruh I don't know how to do that yet :(")
                elif repo == 'everywhere':
                    self._post_simple(chan, 'You asked for the PRs from github and bitbucket')
                else:
                    self._post_simple(chan, 'WTF is that ?')
        return {}

    def wit_get_bus_tt(self, params):
        red_color = "#ff0000"
        green_color = "#36a64f"
        buses = sophiabus230.get_next_buses()
        attachments = []
        tz = gettz('Europe/Paris')
        time_now = datetime.datetime.now(tz=tz)
        attachment = {}

        for passage in buses:
            bus_time = passage['bus_time']
            diff_t = bus_time.replace(tzinfo=tz) - time_now
            att_str = 'In {0} min (at {1})'.format(int(diff_t.total_seconds() / 60),
                                                   bus_time)
            if passage['is_real_time']:
                attachment['color'] = red_color
            else:
                attachment['color'] = green_color
            attachment['text'] = att_str
            attachment['fallback'] = att_str
            attachments.append(attachment)
        self._post_fmt(params['context']['chan'].encode("ascii", "ignore"), attachments)
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
