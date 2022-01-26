from odoo import _, api, fields, models
import requests

class SendMessage(models.Model):
    _name = 'telegram.message'
    _description = 'Send Message Telegram'

    def _get_company_domain(self):
        return [('telegram_id','!=',False)]

    contact_id = fields.Many2one('res.partner', string='To', domain="[('username','!=',False)]")
    company_id = fields.Many2one('res.company', string='From', domain=_get_company_domain)
    message = fields.Text('Message')

    def send_message_telegram(self):
        for rec in self:
            to_message = self.env['res.partner'].search([('id','=',rec.contact_id.id)]).username_id
            from_message = self.env['res.company'].search([('id','=',rec.company_id.id)]).telegram_id

            # Send Message
            url_message = 'https://api.telegram.org/bot'+from_message+'/sendMessage?chat_id='+to_message+'&parse_mode=MarkdownV2&text='+rec.message
            response = requests.get(url_message)
            response.json()
            return