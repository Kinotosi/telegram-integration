from odoo import api, fields, models, _

class SalesModifier(models.Model):
    _inherit = "sale.order"

    def action_message_telegram_send(self):
        for rec in self:
            view_id = self.env.ref('telegram_integration.telegram_message_sale_form_view')
            return {
                'name': _('Send Message Telegram Sale'),
                'res_model': 'telegram.message.sale',
                'context': {
                    'default_sale_id': rec.id
                },
                'type': 'ir.actions.act_window',
                'view_id': False,
                'views': [(view_id.id, 'form')],
                'view_mode': 'form',
                'target': 'new',
                'view_type': 'form',
                'res_id': False
            }
