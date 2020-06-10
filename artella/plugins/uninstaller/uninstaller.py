#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Artella Uninstall plugin implementation
"""

from __future__ import print_function, division, absolute_import

import os
import sys

import artella
from artella import dcc
from artella import logger
from artella import loader
from artella.core import plugin, utils, qtutils


class UninstallerPlugin(plugin.ArtellaPlugin, object):

    ID = 'artella-plugins-uninstaller'
    INDEX = 100

    def __init__(self, config_dict=None, manager=None):
        super(UninstallerPlugin, self).__init__(config_dict=config_dict, manager=manager)

    def uninstall(self, show_dialogs=True):
        artella_path = artella.__path__[0]
        if not os.path.isdir(artella_path):
            msg = 'Artella folder "{}" does not exists!'.format(artella_path)
            if show_dialogs:
                artella.DccPlugin().show_warning_message(text=msg)
            else:
                logger.log_warning(msg)
            return False

        res = qtutils.show_question_message_box(
            'Artella Uninstaller', 'Are you sure you want to uninstall Artella Plugin?')
        if not res:
            return False

        valid_uninstall = self._uninstall(artella_path)
        if not valid_uninstall:
            msg = 'Artella uninstall process was not completed!'.format(artella_path)
            if show_dialogs:
                artella.DccPlugin().show_error_message(text=msg)
            else:
                logger.log_error(msg)
            return False

        if os.path.isdir(artella_path):
            msg = 'Artella folder was not removed during uninstall process.\n\n{}\n\n Remove it manually if you' \
                  'want to have a complete clean uninstall of Artella plugin.'.format(artella_path)
            if show_dialogs:
                dcc.show_info('Artella Uninstaller', msg)
            else:
                logger.log_info(msg)
            utils.open_folder(os.path.dirname(artella_path))

        loader.shutdown()

        # Cleanup artella directories from
        artella_dir = os.path.dirname(artella_path)
        sys_paths = [artella_path, artella_dir, utils.clean_path(artella_path), utils.clean_path(artella_dir)]
        paths_to_remove = list()
        for sys_path in sys.path:
            if sys_path in sys_paths:
                paths_to_remove.append(sys_path)
                sys.path.remove(sys_path)
            elif 'artella-plugins' in sys_path:
                paths_to_remove.append(sys_path)
        for path_to_remove in paths_to_remove:
            if path_to_remove not in sys.path:
                continue
            sys.path.remove(path_to_remove)

        return True

    def _uninstall(self, artella_path):
        if not artella.DccPlugin().dev:
            try:
                utils.delete_folder(artella_path)
            except Exception as exc:
                logger.log_warning(
                    'Impossible to remove Artella Dcc plugin directory: {} | {}'.format(artella_path, exc))
                return False

        return True
