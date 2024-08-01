#!/usr/bin/env python
"""Pull completed tasks from RTM and show only the last 30 days of them.
Largely copied from the examples in the RtmApi codebase.

call the program with the following environment variables:
     API_KEY
     SHARED_SECRET
     TOKEN (optional - if not provided, it will get one via a web browser
            request and display it so you can put it into your environment)
get those parameters from  http://www.rememberthemilk.com/services/api/keys.rtm

If you are using virtualenvwrapper, your virtualenv will be in the
~/.virtualenvs directory.  Edit the bin/activate script in the virtualenv
and add the above-mentioned environment variables there so ensure you have
them set each time you run the script!
"""
import click
import datetime
import os
import webbrowser
from rtmapi import Rtm


@click.command()
def get_filtered_tasks():
    """ Gets tasks from RTM and prints them """
    api_key = os.environ['API_KEY']
    shared_secret = os.environ['SHARED_SECRET']
    if 'TOKEN' in os.environ:
        token = os.environ['TOKEN']
    else:
        token = None
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
        'study german',
        'meditate',
        'oreo medicine',
        'clean basement',
        'cleaning',
        'bread',
        'meditate',
        'waterbottle note',
        'job search',
        'fill birdfeeder',
        'bring water bottles in from car',
        'charge phone',
        'yardwaste bin',
        'girls bath',
        'update monsters blog',
        'sprinklers',
        'lastpass cleanup',
        'update backup task',
        'pay bills',
        'make lunch for girls',
        'make my lunch',
        'django studying',
        'download audiobooks',
        'Python studying',
        'yoga toes',
        'watermelon',
        'pycon lectures  lucasz 60:00',

    ]
    # TODO add method for modifying time range
    start_date = datetime.datetime.now() + datetime.timedelta(-30)
    # get all completed tasks
    result = api.rtm.tasks.getList(filter="status:completed")
    tasks = list()
    for tasklist in result.tasks:
        for taskseries in sorted(tasklist, key=lambda ts: ts.task.completed):
            date_completed = datetime.datetime.strptime(
                taskseries.task.completed[:10], '%Y-%m-%d')
            if date_completed > start_date:
                # completed after the start of the range
                if taskseries.name not in repeated_tasks and not \
                     taskseries.name.startswith('quicken'):
                    tasks.append("{0} {1}".format(taskseries.task.completed,
                                                  taskseries.name))
    # print out the tasks in order!
    click.echo_via_pager('\n'.join(sorted(tasks)))

if __name__ == '__main__':
    get_filtered_tasks()
