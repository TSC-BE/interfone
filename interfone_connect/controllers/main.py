from odoo import SUPERUSER_ID, _, http
from odoo.http import Response, request
from werkzeug.urls import url_join

from odoo.addons.mail.controllers.bus import MailChatController

_logger = http.logging.getLogger(__name__)


class ControllerREST(MailChatController):

    @http.route('/api/kazoo', methods=['GET', 'POST'], type='http',
                auth='public', csrf=False)
    def api_kazoo_call(self, **post):
        _logger.info('Kazoo API Call: Request Received.')
        kazoo_id = post.get('kazoo_id', False)
        kazoo_user_id = post.get('user_id', False)
        callerid = post.get('callerid')
        if not kazoo_id or not kazoo_user_id or not callerid:
            _logger.info('Kazoo API Call: Not Enough Arguments Provided.')
            return Response('Not Enough Arguments Provided.', status=400)
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url', False)
        _logger.info(f"""Kazoo API Call: kazoo_id: {kazoo_id},
                     user_id: {kazoo_user_id}, callerid: {callerid}""")
        res_user_id = request.env['res.users'].sudo().search([
            ('kazoo_id', '=', kazoo_id),
            ('kazoo_user_id', '=', kazoo_user_id)],
            limit=1)
        if not res_user_id:
            _logger.info('Kazoo API Call: User Not Found.')
            return Response('User Not Found.', status=404)
        caller = callerid.replace(' ', '')
        partner_id = request.env['res.partner'].sudo().search([
            '|',
            ('phone', 'like', caller),
            ('mobile', 'like', caller)])
        if not partner_id:
            _logger.info('Kazoo API Call: Caller Not Found.')
            return Response('Partner Not Found.', status=400)
        _logger.info(f"""Kazoo API Call: Calling Partner ID: {partner_id.id},
                     Calling Partner Name: {partner_id.name}""")
        user_id = request.env['res.users'].sudo().browse(res_user_id.id)
        super_user = request.env['res.users'].sudo().browse([SUPERUSER_ID])
        mail_channel = request.env["mail.channel"].with_context(
            mail_create_nosubscribe=False)
        direct_message_channel = mail_channel.sudo().create({
            'channel_partner_ids': [
                (4, super_user.partner_id.id),
                (4, user_id.partner_id.id)],
            'channel_type': 'chat',
            'name': ', '.join([super_user.name, user_id.name]),
            'public': 'private',
            'email_send': False,
        })
        author = request.env['res.users'].sudo().browse(request.session.uid).partner_id
        author_id = author.id
        email_from = author.email_formatted
        body = (_(f"""<a href='{base_url}/web#id={partner_id.id}&view_type=form&
                model=res.partner'>{partner_id.name}</a> is calling"""))
        direct_message_channel.with_context(mail_create_nosubscribe=True).message_post(
            author_id=author_id,
            email_from=email_from,
            body=body,
            message_type='comment',
            subtype_xmlid='mail.mt_comment')
        _logger.info('Kazoo API Call: Success.')
        return Response('Success.', status=200)
