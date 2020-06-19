#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Artella Uninstaller plugin implementation for Maya
"""

from __future__ import print_function, division, absolute_import

import os
import logging

from artella.core import utils
from artella.plugins.uninstaller import uninstaller

ARTELLA_MOD_NAMES = ['artella.mod']

logger = logging.getLogger('artella')


class UninstallerMayaPlugin(uninstaller.UninstallerPlugin, object):
    def __init__(self, config_dict=None, manager=None):
        super(UninstallerMayaPlugin, self).__init__(config_dict=config_dict, manager=manager)

    def _uninstall(self, artella_path):
        super(UninstallerMayaPlugin, self)._uninstall(artella_path)

        maya_module_paths = os.environ.get('MAYA_MODULE_PATH', None)
        if not maya_module_paths:
            logger.warning('No Maya module paths found ...')
            return False

        module_files_to_remove = list()
        maya_module_paths = maya_module_paths.split(';')
        for maya_module_path in maya_module_paths:
            module_files = os.listdir(maya_module_path)
            for module_file in module_files:
                if module_file in ARTELLA_MOD_NAMES:
                    module_file_to_remove = os.path.join(maya_module_path, module_file)
                    module_files_to_remove.append(module_file_to_remove)
        if not module_files_to_remove:
            logger.warning('No Artella Maya module file found ...')
            return False

        logger.info('Removing Artella Maya module files: {}'.format(module_files_to_remove))
        valid_remove = False
        for module_file_to_remove in module_files_to_remove:
            if not os.path.isfile(module_file_to_remove):
                continue
            valid_remove = utils.delete_file(module_file_to_remove)
            if not valid_remove:
                logger.info('Was impossible to remove Artella module file: {}'.format(module_file_to_remove))
                break

        return valid_remove