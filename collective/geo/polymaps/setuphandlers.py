# -*- coding: utf-8 -*-
import logging
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

from collective.geo.settings.interfaces import IGeoSettings
# The profile id of your package:
PROFILE_ID = 'profile-collective.geo.polymaps:default'

CGP_VIEWLETS = ['polymaps:plone.abovecontentbody|Polymap Above Content',
                'polymaps:plone.belowcontentbody|Polymap Below Content']

def add_cgp_viewlets(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('collective.geo.polymaps')
    settings = getUtility(IRegistry).forInterface(IGeoSettings)
    viewlet_managers = settings.map_viewlet_managers
    for vm in CGP_VIEWLETS:
        if vm not in viewlet_managers:
            viewlet_managers.append(vm)
            logger.info('add viewlet %s' % vm)
    logger.info('Polymap viewlets added')


def setupVarious(context):
    """Import step for configuration that is not handled in xml files.
    """
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('collecive.geo.polymaps_various.txt') is None:
        return
    logger = context.getLogger('collective.geo.polymaps')
    site = context.getSite()
    add_cgp_viewlets(site, logger)
