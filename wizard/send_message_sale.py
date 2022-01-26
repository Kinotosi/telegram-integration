import base64

from odoo import _, api, fields, models
import requests

class SendMessage(models.Model):
    _name = 'telegram.message.sale'
    _description = 'Send Message Telegram'

    def _get_company_domain(self):
        return [('telegram_id','!=',False)]

    contact_id = fields.Many2one('res.partner', string='To', domain="[('username','!=',False)]")
    company_id = fields.Many2one('res.company', string='From', domain=_get_company_domain)
    sale_id = fields.Many2one('sale.order', string='Sale')
    is_report = fields.Boolean(string='PDF Report', required=False)
    message = fields.Text('Message')

    def send_message_telegram(self):
        for rec in self:
            to_message = self.env['res.partner'].search([('id','=',rec.contact_id.id)]).username_id
            from_message = self.env['res.company'].search([('id','=',rec.company_id.id)]).telegram_id

            # Send Message
            url_message = 'https://api.telegram.org/bot'+from_message+'/sendMessage?chat_id='+to_message+'&parse_mode=MarkdownV2&text='+rec.message
            response = requests.get(url_message)
            response.json()

            # Send Document
            if rec.is_report:
                report_template_id = self.env.ref('sale.action_report_saleorder')._render_qweb_pdf(rec.sale_id.id)
                data_record = base64.b64encode(report_template_id[0])
                ir_value = {
                    'name': "Sale Report - {}".format(rec.sale_id.name),
                    'type': 'binary',
                    'datas': data_record,
                    'store_fname': data_record,
                    'mimetype': 'application/x-pdf',
                }
                data_id = self.env['ir.attachment'].create(ir_value)
                base_url = self.env['ir.config_parameter'].get_param('web.base.url')

                document_id = "{}/web/content/{}?download=true".format(base_url, data_id.id)
                url_documment = 'https://api.telegram.org/bot'+from_message+'/sendDocument?chat_id='+to_message+'&document='+document_id
                send_documment = requests.get(url_documment)
                send_documment.json()
                print(document_id)
            return
