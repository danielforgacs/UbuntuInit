"""
Module to run system diagnostics.

- diag funcs are auto discovered: any func starting with
    DIAGNOSTIC_FUNC_PREFIX is run in the main function.
- there's a dependency free wsgi server to serve results as html.
- the server version works by collecting messages from return
    values. A diagnostic func without a returned message will
    be missing from the online results.
"""

import sys
import os
import io
import re
import datetime
import subprocess
import types
import functools
import wsgiref.simple_server as simpserv


DO_PRINT = True
DO_CAPTURE_STDOUT = False
ERRORS_ONLY = False
DIAGNOSTIC_FUNC_PREFIX = 'check_'

SWAPFILE = '/swapfile'
EXPECTED_SWAP_SIZE = 6 * 1024 * 1024 * 1024
EXPECTED_SWAPPINESS = 30
GRUBFILE = '/etc/default/grub'
SPLASH_SCREEN_MARKER = 'quiet splash'
PARTITIONS = [
    '/dev/sda2',
    '/dev/sda3',
]
REPOS = [
    'git-core',
]
SERVICES = [
    [' ', 'avahi-daemon.service'],
    [' ', 'avahi-daemon.socket'],
    [' ', 'motd-news.service'],
    [' ', 'motd-news.timer'],
                # [' ', 'snapd.service'],
                # [' ', 'snapd.socket'],
                # ['--user', 'gsd-wacom.target'],
                # ['--user', 'gsd-print-notifications.target'],
    ['--user', 'org.gnome.SettingsDaemon.Wacom.target'],
    ['--user', 'org.gnome.SettingsDaemon.Wacom.service'],
]
INSTALLED_PACKAGES = [
    'ghostscript*',
]
MISSING_PACKAGES = [
    'git',
    'git-gui',
    'gitk',
    'ranger',
    'doublecmd*',
    'synaptic',
    'dconf-editor',
    'baobab',
    'gthumb',
    'gnome-tweaks',
    'curl',
    'vim',
    'tree',
    'docker-compose',
    'xournal',
]




class StdOutCapture:
    """
    Context manager for temporarily redirecting stdout
    to prevent print output. The "data" property contains
    the actual ouput.
    """
    def __enter__(self, *args):
        self.stdout = io.StringIO()
        sys.stdout = self.stdout
        return self

    def __exit__(self, *args):
        sys.stdout = sys.__stdout__

    @property
    def data(self):
        return self.stdout.getvalue()





def print_func_result(func):
    @functools.wraps(func)
    def wrapper():
        result = func()
        funcname = func.__name__[len(DIAGNOSTIC_FUNC_PREFIX):]
        header = f'--- {funcname.upper()} '.ljust(79, '-')
        result = f'\n{header}\n{result}'
        if DO_PRINT:
            is_error = '[ERROR]' in result
            if not ERRORS_ONLY or is_error:
                print(result)
        return result
    return wrapper




def capture_stdout(func):
    @functools.wraps(func)
    def wrapper():
        with StdOutCapture() as stdout:
            result = func()
        if not DO_CAPTURE_STDOUT:
            print(stdout.data)
        return result
    return wrapper




# @capture_stdout
# @print_func_result
# def check_swappiness():
#     cmd = ['cat', '/proc/sys/vm/swappiness']
#     swappinesscheck = subprocess.run(cmd, capture_output=True)
#     swappinessnum = int(swappinesscheck.stdout.decode().strip())
#     msg = '[INFO] swappiness OK.'
#
#     if swappinessnum != EXPECTED_SWAPPINESS:
#         msg = '[ERROR] swappiness is: '+str(swappinessnum)+'; expected: '+str(EXPECTED_SWAPPINESS)
#
#     return msg




# @capture_stdout
# @print_func_result
# def check_boot_splash_screen():
#     with open(GRUBFILE, 'r') as filestream:
#         grubconfig = filestream.read()
#
#     msg = '[INFO] boot splash screen is OFF.'
#
#     if SPLASH_SCREEN_MARKER in grubconfig:
#         msg = '[ERROR] boot splash screen is turned ON in grub config'
#
#     return msg




# @capture_stdout
# @print_func_result
# def check_services():
#     msg = ''
#
#     for service in SERVICES:
#         response = subprocess.run(['systemctl', 'status']+ service, capture_output=True)
#         output = response.stdout.decode()
#
#         if 'Active: inactive' not in output:
#             msg += '[ERROR] service is running: '+service[1]+'\n'
#
#     msg = msg.strip()
#
#     return msg
#



# @capture_stdout
# @print_func_result
# def check_free_space():
#     cmd = ['df', '-h', *PARTITIONS]
#     response = subprocess.run(cmd, capture_output=True)
#     result = response.stdout.decode()
#     result = result.strip()
#
#     return result
#



# @capture_stdout
# @print_func_result
# def check_swapfile_size():
#     msg = '[INFO] Swapfile size OK.'
#
#     if os.stat(SWAPFILE).st_size < EXPECTED_SWAP_SIZE:
#         msg ='[ERROR] swapfile is smaller than: '+str(EXPECTED_SWAP_SIZE)
#
#     return msg
#



# @capture_stdout
# @print_func_result
# def check_drives_on_dock():
#     cmd = ['gsettings', 'get', 'org.gnome.shell.extensions.dash-to-dock', 'show-mounts']
#     response = subprocess.run(cmd, capture_output=True)
#     output = response.stdout.decode().strip()
#     msg = '[INFO] Drives hidden from dock OK.'
#
#     if output != 'false':
#         msg = '[ERROR] Drives shown on dock.'
#
#     return msg




# @capture_stdout
# @print_func_result
# def check_apt_repositories():
#     msg = ''
#     cmd = ['apt-add-repository', '--list']
#
#     for repo in REPOS:
#         response = subprocess.run(cmd, capture_output=True)
#         output = response.stdout.decode().strip()
#
#         if repo not in output:
#             msg += '[ERROR] Apt repo not added: ' + repo + '\n'
#
#     msg = msg.strip()
#
#     return msg




# @capture_stdout
# @print_func_result
# def check_unnecessary_packages():
#     msg = ''
#
#     for package in INSTALLED_PACKAGES:
#         cmd = ['apt', 'list', '--installed', package]
#         response = subprocess.run(cmd, capture_output=True)
#         output = response.stdout.decode().strip()
#
#         if output != 'Listing...':
#             msg += '[ERROR] package is installed: '+package+'\n'
#
#     msg = msg.strip()
#
#     return msg





# @capture_stdout
# @print_func_result
# def check_missing_packages():
#     msg = ''
#
#     for package in MISSING_PACKAGES:
#         cmd = ['apt', 'list', '--installed', package]
#         response = subprocess.run(cmd, capture_output=True)
#         output = response.stdout.decode().strip()
#
#         if output == 'Listing...':
#             msg += '[ERROR] package is missing: '+package+'\n'
#
#     msg = msg.strip()
#
#     return msg





def collect_diag_funcs(globalsdict):
    """
    If this is not called late anough in the module
    it won't collect all the funcs!
    """
    is_func = lambda item: isinstance(item[1], types.FunctionType)
    is_diag = lambda item: item[0].startswith(DIAGNOSTIC_FUNC_PREFIX)
    diagfuncs = tuple(globalsdict.items())
    diagfuncs = filter(is_func, diagfuncs)
    diagfuncs = filter(is_diag, diagfuncs)

    for item in diagfuncs:
        func = item[1]

        yield func




def main():
    for func in collect_diag_funcs(globalsdict=globals()):
        func()

    print('\n... REPORT DONE.')




def htmlify_report(report):
    report = re.sub('\n', '<br/>\n', report)
    report = re.sub('(\[ERROR\].*)\n', '<div style="background-color: lightcoral;">\g<1></div>\n', report)
    report = re.sub('(\[INFO\].*)\n', '<div style="background-color: lightgreen;">\g<1></div>\n', report)

    return report




def responde_html_report(environ, start_response):
    messages = ''
    time0 = datetime.datetime.now()

    for func in collect_diag_funcs(globalsdict=globals()):
        messages += f'\n{func()}'

    messages += '\n'
    timedelta = datetime.datetime.now() - time0
    html = htmlify_report(report=messages)
    html += '<p>elapsed time: '+str(timedelta)+'</p>'
    response = [html.encode()]

    start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])

    return response




def serve_diagnostics():
    print('-'*79)
    with simpserv.make_server(host='', port=8000, app=responde_html_report) as httpd:
        print('http://localhost:8000')
        httpd.serve_forever()




if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 2:
        DO_CAPTURE_STDOUT = True
        serve_diagnostics()
