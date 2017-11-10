#!/usr/bin/env python
# encoding: utf-8

import configargparse
import subprocess
import json
from datetime import datetime
import time
import sys
import os

def get_gpu_stat(hostname):
    try:
        cmd_args = ['ssh', hostname, 'gpustat', '--json']
        result = subprocess.check_output(cmd_args)
        return result
    except subprocess.CalledProcessError as e:
        return None

if __name__ == '__main__':
    parser = configargparse.ArgParser(default_config_files=['./config'])
    parser.add('-c', required=False, is_config_file=True)
    parser.add('--hosts', action='append')
    parser.add('--interval', type=int)
    parser.add('--log_path')

    args = parser.parse_args()

    if not os.path.exists(args.log_path):
        os.makedirs(args.log_path)

    while True:
        try:
            now = datetime.now()
            date = str(now).split()[0]

            results = []
            print(str(now))
            for hostname in args.hosts:
                result = get_gpu_stat(hostname)
                if result is not None:
                    result = json.loads(result)
                    results.append(result)
                    print('get result from {}'.format(hostname))

                else:
                    print('get error from {}'.format(hostname))

            print '=' * 89
            output_json = {'time': str(now), 'data': results}
            with open(args.log_path + '/' + date + '.log', 'a') as f:
                f.write(json.dumps(output_json) + '\n')

            sys.stdout.flush()
            time.sleep(args.interval)

        except KeyboardInterrupt:
            print('-' * 89)
            print('Exiting from keyboard interrupt')
            break


