# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError,AccessDenied, Warning
from odoo import exceptions


class SaleOrderLine(models.Model):
    _inherit = 'sale.order'

    order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)
    duplicate_product= fields.Boolean(string= "Product Dupliqué ", compute= "_check_exist_product_in_line")
    name_pr = fields.Char(string="Nom du produit dupliqué")

    @api.depends("duplicate_product")
    def _check_exist_product_in_line(self):
        for order in self:
            products_in_lines = order.mapped('order_line.product_id')
            list = []
            name=''
            duplicate_product = False
            for product in products_in_lines:
                print("product",product.name)
                lines_count = len(order.order_line.filtered(lambda line: line.product_id == product))
                print("lines_count",lines_count)

                if lines_count > 1:
                    duplicate_product = True
                    print("product",product.name)
                    name=product.name
                    print("duplicate_product", duplicate_product)
                    break
                duplicate_product = duplicate_product
            order.name_pr=name
            order.duplicate_product=duplicate_product
            print(order.duplicate_product)
        return True
