#!/usr/bin/env python
# -*- coding: utf-8 -*-

from billybob import BillyBob


bb = BillyBob(slack_token="xoxb-67971489922-kA41fi3F2LANkkdbsOhlOGuD",
              wit_token="PGCJHLO7LMO656YWKFNYLIIOOPEQL7GH")

bb.start_service()
