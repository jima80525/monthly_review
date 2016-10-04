#!/usr/bin/env python
"""Pull completed tasks from RTM and show only the last 30 days of them.
Largely copied from the examples in the RtmApi codebase."""
import datetime
import sys
import os
import webbrowser
from rtmapi import Rtm


def get_filtered_tasks(api_key, shared_secret, token):
    """ Gets tasks from RTM and prints them """
    # call the program with the following environment variables:
    #     API_KEY
    #     SHARED_SECRET
    #     TOKEN (optional - if not provided, it will get one via a web browser
    #     request and display it so you can put it into your environment)
    # get those parameters from
    # http://www.rememberthemilk.com/services/api/keys.rtm
    api = Rtm(api_key, shared_secret, "delete", token)

    # authenication block, see
    # http://www.rememberthemilk.com/services/api/authentication.rtm
    # check for valid token
    if not api.token_valid():
        # use desktop-type authentication
        url, frob = api.authenticate_desktop()
        # open webbrowser, wait until user authorized application
        webbrowser.open(url)
        input("Continue?")
        # get the token for the frob
        api.retrieve_token(frob)
        # print out new token, should be used to initialize the Rtm object next
        # time (a real application should store the token somewhere)
        print("New token: %s" % api.token)

    repeated_tasks = [
        'log miles',
        'clean basement',
        'cleaning',
        'bread',
        'waterbottle note',
        'job search',
        'fill birdfeeder',
        'bring water bottles in from car',
        'charge phone',
        'yardwaste bin',
        'girls bath',
        'update girls blog',
        'lastpass cleanup',
        'update backup task',
        'pay bills',
    ]
    # TODO add method for modifying time range
    start_date = datetime.datetime.now() + datetime.timedelta(-30)
    # get all completed tasks
    result = api.rtm.tasks.getList(filter="status:completed")
    for tasklist in result.tasks:
        for taskseries in sorted(tasklist, key=lambda ts: ts.task.completed):
            date_completed = datetime.datetime.strptime(
                taskseries.task.completed[:10], '%Y-%m-%d')
            if date_completed > start_date:
                # completed after the start of the range
                if taskseries.name not in repeated_tasks:
                    print(taskseries.task.completed, taskseries.name)

if __name__ == '__main__':
    sys.exit(get_filtered_tasks(os.environ['API_KEY'],
                                os.environ['SHARED_SECRET'],
                                os.environ['TOKEN']))
