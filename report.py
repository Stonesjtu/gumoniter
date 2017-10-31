"""Process the log file to get statistics for every user in cluster

This is file serves as an example getting the overall GPU usages for user
"""

import json

filename = './logs/all.log'


class OverallReporter(object):
    """A reporter class

    Properties:
        - filename: log file to load
        - interval: log file interval
        - user2usage: a dictionary from user to usage
    """
    def __init__(self, filename):
        self.filename = filename
        self.interval = 600
        self.user2usage = {}
        self.process()

    def process(self):
        """Process the log file line by line
        One line in log is a timeslot defined before
        """
        for line in open(self.filename, 'r'):
            data = json.loads(line)
            self.add_timeslot(data)

    def add_timeslot(self, data):
        """Process one timeslot
        The data in one timeslot consists of multi-machines,
        each has multi-gpus, gpu has multi-tasks"""
        machines = data['data']
        for machine in machines:
            gpus = machine['gpus']
            for gpu in gpus:
                tasks = gpu['processes']
                utilization = int(gpu['utilization.gpu'])
                for task in tasks:
                    user = task['user']
                    memory = task['used_memory']
                    self.add_usage(user, utilization)

    def add_usage(self, user, utilization):
        if user not in self.user2usage:
            self.user2usage[user] = []
        self.user2usage[user].append(utilization)

    def report_occupy(self):
        """report the usages for user sorted by overall usages"""
        time_occupy = {}
        for k,v in self.user2usage.iteritems():
            time_occupy[k] = len(v)
        print('-'*89)
        print('User\t-->\tGPU*minutes')
        for user, time in sorted(time_occupy.items(), key=lambda x:x[1], reverse=True):
            print('%s\t-->\t%d' % (user, time*10))
        print('-'*89)

    def report_avg_util(self):
        """report the average gpu utilization among users"""
        avg_util = {}
        for k,v in self.user2usage.iteritems():
            avg_util[k] = sum(v) / len(v)
        print('-'*89)
        print('User\t-->\tutils')
        for user, util in sorted(avg_util.items(), key=lambda x:x[1], reverse=True):
            print('%s\t-->\t%d' % (user, util))
        print('-'*89)


reporter = OverallReporter(filename=filename)
reporter.report_occupy()
reporter.report_avg_util()
