# -*- coding: utf-8 -*-
##############################################################################
#
# Author: Yannick Buron
# Copyright 2015, TODAY Clouder SASU
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License with Attribution
# clause as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License with
# Attribution clause along with this program. If not, see
# <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, modules
from openerp.exceptions import ValidationError


class ClouderContainer(models.Model):
    """
    Adds methods to manage magneto specificities.
    """

    _inherit = 'clouder.container'

    @api.multi
    def deploy_post(self):
        super(ClouderContainer, self).deploy_post()
        if self.application_id.type_id.name == 'magento':
            if self.application_id.code == 'exec' \
                    and self.parent_id and self.parent_id.parent_id \
                    and self.parent_id.parent_id.application_id.code == 'magentodoo':

                # Making directories and installing odoo connector module in magento
                self.execute([
                    'mkdir',
                    '-p',
                    '/opt/magento/exec/app/code/community'
                ])
                self.execute([
                    'cp',
                    '-r',
                    '/opt/magento/magento-module/Openlabs_OpenERPConnector-1.1.0/Openlabs',
                    '/opt/magento/exec/app/code/community/'
                ])
                self.execute([
                    'mkdir',
                    '-p',
                    '/opt/magento/exec/app/etc/modules'
                ])
                self.execute([
                    'cp',
                    '/opt/magento/magento-module/Openlabs_OpenERPConnector-1.1.0' +
                    '/Openlabs/app/etc/modules/Openlabs_OpenERPConnector.xml',
                    '/opt/magento/exec/app/etc/modules/'
                ])
                self.execute([
                    'chown',
                    '-r',
                    'www-data:www-data'
                    '/opt/magento/exec/'
                ])


