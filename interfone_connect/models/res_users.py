# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    click2call_uniqueid = fields.Char(string='Click2Call ID', copy=False)
    kazoo_id = fields.Char(string='Account ID', copy=False)
    kazoo_user_id = fields.Char(string='User ID', copy=False)
