# Copyright 2019 Salinity Developers <http://salinity.in/>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import requests

from odoo import _, http, models
from odoo.exceptions import UserError
from werkzeug.urls import url_join
_logger = http.logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def phone_click2call_action(self):
        phone = self.clean_number(self.phone)
        self.send_request(phone)

    def mobile_click2call_action(self):
        mobile = self.clean_number(self.mobile)
        self.send_request(mobile)

    def clean_number(self, number):
        number = number.replace(" ", "")
        number = number.replace("+", "")
        return number
    
    def send_request(self, number):
        self.ensure_one()
        if not self.env.user.click2call_uniqueid:
            raise UserError(_("""Please configure Click2Call
                              UniqueID in User -> Preference."""))
        self.env.user.notify_info(_("Initiating Call..."))
        interfone_url = self.env['ir.config_parameter'].sudo().get_param('interfone_url', False)
        if interfone_url:
            request = requests.get(f"""{interfone_url}{self.env.user.kazoo_id}/clicktocall/{self.env.user.click2call_uniqueid}/connect?contact={number}""")
            data = request.json()
            _logger.info(f"""Initiated call for {self.name}(ID:{self.id}) on this number:
                        {self.phone}. Response: {data}""")
        else:
            raise UserError(_("No url configured"))
