#!/usr/bin/env python
# -*- coding: utf-8 -*-

from billybob import BillyBob


bb = BillyBob(SLACK_API_TOKEN="slack api token", JENKINS_TOKEN="jenkins token")

bb.print_params()
