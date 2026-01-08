#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Use IMAP CLI to get a summary of IMAP account state."""


import logging
import os
import sys
import time

import docopt

import imap_cli
from imap_cli import config

try:
    from plyer import notification
    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False


app_name = os.path.splitext(os.path.basename(__file__))[0]
usage = """Usage: imap-notify [options] <directories>...

Options:
    -d, --delay=<delay>         Delay (in seconds) between notifications
    -c, --config-file=<FILE>    Configuration file (`~/.config/imap-cli`)
    -f, --format=<FMT>          Output format
    -v, --verbose               Generate verbose messages
    -h, --help                  Show help options.
    --version                   Print program version.

----
Copyright (C) 2014 Romain Soufflet
License MIT
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Requires: pip install imap-cli[notify]
"""
log = logging.getLogger(app_name)


def main():
    args = docopt.docopt('\n'.join(usage.split('\n')))

    logging.basicConfig(
        level=logging.DEBUG if args['--verbose'] else logging.WARNING,
        stream=sys.stdout,
    )

    if not HAS_PLYER:
        log.error('plyer is required for notifications. '
                  'Install with: pip install imap-cli[notify]')
        return 1

    connection_config = config.new_context_from_file(args['--config-file'],
                                                     section='imap')
    if connection_config is None:
        return 1
    try:
        delay = int(args['--delay'] or 60)
    except ValueError:
        log.error('Wrong value for options "delay"')
        return 1
    format_str = args['--format'] or u'{recent:<3} new mails in {directory} ({count} total)'

    imap_account = imap_cli.connect(**connection_config)

    time_count = 0
    sys.stdout.write('\n')
    while True:
        time_count += 1
        if time_count % delay == 0:
            notifications = []
            for status in imap_cli.status(imap_account):
                if (status['directory'] in args['<directories>'] and
                        status['recent'] != '0'):
                    notifications.append(format_str.format(**status))
            if len(notifications) > 0:
                notification.notify(
                    title="IMAP Notify",
                    message='\n'.join(notifications),
                    app_name=app_name,
                    timeout=10,
                )
        time.sleep(1)

    return 0


if __name__ == "__main__":
    sys.exit(main())
