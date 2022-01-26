from pyexpat import model
from odoo import _, api, fields, models

class CompanyTelegram(models.Model):
    _inherit = "res.company"

    telegram_id = fields.Char('Token Telegram')