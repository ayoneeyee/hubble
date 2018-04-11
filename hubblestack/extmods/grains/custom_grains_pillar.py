'''
HubbleStack Custom Grains and Pillar

:maintainer: HubbleStack
:platform: All
:requires: SaltStack
'''

import re
import salt.modules.cmdmod
import logging

log = logging.getLogger(__name__)

__salt__ = {
        'cmd.run': salt.modules.cmdmod._run_quiet,
        'config.get': salt.modules.config.get,
}


def populate_custom_grains_and_pillar():
    '''
    To return grains and pillar fields values as specified in config file.
    For example:
    custom_grains_pillar:
      grains:
        - selinux: selinux:enabled
        - release: osrelease
      pillar:
        - ntpserver: network_services:ntpserver
    '''
    log.debug('Fetching custom grains and pillar details')
    grains = {}
    salt.modules.config.__opts__ = __opts__
    if __salt__['config.get']('custom_grains_pillar:grains'):
        custom_grains = __salt__['config.get']('custom_grains_pillar:grains')
    for grain in custom_grains:
        for key in grain:
            if _valid_command(grain[key]):
                value = __salt__['cmd.run']('salt-call grains.get {0}'.format(grain[key])).split('\n')[1].strip()
                grains[key] = value
    if __salt__['config.get']('custom_grains_pillar:pillar'):
        custom_pillar = __salt__['config.get']('custom_grains_pillar:pillar')
    for pillar in custom_pillar:
        for key in pillar:
            if _valid_command(pillar[key]):
                value = __salt__['cmd.run']('salt-call pillar.get {0}'.format(pillar[key])).split('\n')[1].strip()
                grains[key] = value
    log.debug('Done with fetching custom grains and pillar details')
    return grains


def _valid_command(string):
    invalid_characters = re.findall('[^a-zA-Z0-9:_-]',string)
    if len(invalid_characters) > 0:
        log.info("Command: {0} contains invalid characters: {1}".format(string, invalid_characters))
        return False
    else:
        return True
