from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import requests

class PartnertModifer(models.Model):
    _inherit = 'res.partner'

    username = fields.Char('Username Telegram')
    username_id = fields.Char('Telegram Id')

    def get_username_id(self, user_name, user):
        if user_name:
            company_ids = self.env['res.users'].search([('id','=',user)]).company_ids
            company_token = self.env['res.company'].search([('id','in',company_ids.ids),('telegram_id','!=',False)]).ids
            get_id = self.env['res.company'].search([('id','=',company_token[0])]).telegram_id
            url_update = 'https://api.telegram.org/bot'+get_id+'/getUpdates'
            response = requests.get(url_update)
            data_tele = response.json()
            id_tele = 0
            for rec in data_tele['result']:
                if rec['message']['from']['username'] == user_name:
                    id_tele = rec['message']['from']['id']
                    break
            if id_tele == 0:
                raise ValidationError("Chat or click start button in account telegram bot")
            return id_tele
        return 0

    def write(self, vals):
        user_id = self.env.user
        if vals.get('username'):
            vals.update({'username_id': self.get_username_id(vals.get('username'), user_id.id)})
        return super(PartnertModifer, self).write(vals)

    @api.model
    def create(self, vals):
        res = super(PartnertModifer, self).create(vals)
        user_id = self.env.user
        vals.update({'username_id': self.get_username_id(vals.get('username'), user_id.id)})
        return res