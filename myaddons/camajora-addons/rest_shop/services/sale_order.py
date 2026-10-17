import logging
from odoo.addons.component.core import Component
from odoo.exceptions import MissingError

log = logging.getLogger(__name__)


class SaleOrderService(Component):
    _inherit = 'base.rest.private.service'
    _name = "saleorder.service"
    _usage = "saleorder"
    _collection = "base.rest.private.shop.services"

    def get(self, _id):
        partner_id = self.env.user.partner_id
        parent_id = partner_id.parent_id

        sale_order = (
            self.env["sale.order"]
            .sudo()
            .search([("id", "=", _id), ("partner_id", "in", [parent_id.id, partner_id.id])])
        )
        if sale_order:
            return self._to_json(sale_order)
        raise MissingError("Sale Order not found")

    def search(self, **params):
        sale_order_ids = self._retrieve_sale_orders(**params)
        return self._to_json(sale_order_ids, many=True)

    def _get_object_schema(self):
        return {
            "id": {"type": "integer", "required": True, "empty": False, "nullable": False},
            "state": {"type": "string", "required": True, "empty": False, "nullable": False},
            "invoice_status": {"type": "string", "required": True, "empty": False, "nullable": False},
            "name": {"type": "string", "required": True, "empty": False, "nullable": False},
            "date": {"type": "date", "required": True, "empty": False, "nullable": False},
            "note": {"type": "string", "required": False, "empty": True, "nullable": True},
            "invoices": {
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "name": {"type": "string", "required": False},
                        "state": {"type": "string", "required": False},
                        "date_invoice": {"type": "date", "required": False},
                        "due_date": {"type": "date", "required": False},
                        "attachment": {"type": "string", "required": True},
                    },
                },
            },
            "amount": {
                "type": "dict",
                "schema": {
                    "tax": {"type": "float", "required": False, "empty": True, "nullable": True},
                    "untaxed": {"type": "float", "required": False, "empty": True, "nullable": True},
                    "total": {"type": "float", "required": False, "empty": True, "nullable": True},
                }
            },
            "lines": {
                "type": "dict",
                "schema": {
                    "amount": {
                        "type": "dict",
                        "schema": {
                            "tax": {"type": "float", "required": False, "empty": True, "nullable": True},
                            "untaxed": {"type": "float", "required": False, "empty": True, "nullable": True},
                            "total": {"type": "float", "required": False, "empty": True, "nullable": True},
                        }
                    },
                    "count": {"type": "float", "required": False, "empty": True, "nullable": True},
                    "items": {
                        "type": "list",
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "id": {"type": "integer", "required": True, "empty": False, "nullable": False},
                                "product": {"type": "string", "required": True, "empty": False, "nullable": False},
                                "image": {"type": "string", "required": False, "empty": True, "nullable": True},
                                "variant": {"type": "string", "required": True, "empty": True, "nullable": True},
                                "qty": {"type": "float", "required": False, "empty": True, "nullable": True},
                                "amount": {
                                    "type": "dict",
                                    "schema": {
                                        "price": {"type": "float", "required": False, "empty": True, "nullable": True},
                                        "tax": {"type": "float", "required": False, "empty": True, "nullable": True},
                                        "untaxed": {"type": "float", "required": False, "empty": True, "nullable": True},
                                        "total": {"type": "float", "required": False, "empty": True, "nullable": True},
                                    }
                                },
                            }
                        }
                    }
                }
            }
        }

    def _serialize_invoice(self, invoice):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")

        data = {}
        attachment_id = (
            self.env["ir.attachment"]
            .sudo()
            .search([("res_id", "=", invoice.id), ("res_model", "=", "account.invoice")])
        )
        data["id"] = invoice.id
        data["name"] = invoice.number
        data["state"] = invoice.state
        data["date_invoice"] = invoice.date_invoice
        data["date_due"] = invoice.date_due
        data["attachment"] = (
            "%s/web/content/%s/download=true?access_token=" % (base_url, attachment_id.id) + ''.join(attachment_id.generate_access_token())
            if attachment_id
            else None
        )

        return data

    def _serialize_product(self, order_line):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")

        data = {}

        data["name"] = order_line.name
        data["product_uom_qty"] = order_line.product_uom_qty
        data["price"] = order_line.price_unit * order_line.product_uom_qty
        data["discount"] = order_line.discount
        data["image"] = "%s/website/image/product.product/%s/image/500x0" % (
            base_url,
            order_line.product_id.id,
        )
        data["image_small"] = "%s/website/image/product.product/%s/image/200x0" % (
            base_url,
            order_line.product_id.id,
        )
        return data

    def _serialize(self, record):
        data = {}
        data["id"] = record.id
        data["state"] = record.state
        data["name"] = record.name
        data["date"] = record.date_order
        data["note"] = record.note
        data["lines"] = self._serialize_lines(record)
        data["amount"] = {
            "tax": record.amount_tax,
            "untaxed": record.amount_untaxed,
            "total": record.amount_total,
        }
        data["invoice_status"] = record.invoice_status
        data["invoices"] = []
        for invoice in record.invoice_ids:
            data["invoices"].append(self._serialize_invoice(invoice))
        return data

    def _serialize_lines(self, cart):
        items = []
        for line in cart.order_line:
            items.append(self._serialize_one_line(line))
        return {
            "items": items,
            "count": sum([item["qty"] for item in items]) if items else 0,
            "amount": {
                "tax": sum([item["amount"]["tax"] for item in items]),
                "untaxed": sum([item["amount"]["untaxed"] for item in items]),
                "total": sum([item["amount"]["total"] for item in items]),
            },
        }

    def _serialize_one_line(self, line):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")

        data = {
            "id": line.id,
            "product": line.sudo().name,
            "image": "%s/website/image/product.product/%s/image/200x0" % (base_url, line.sudo().product_id.id),
            "variant": ",".join([a.name for a in line.sudo().product_id.attribute_value_ids]),
            "amount": {
                "price": line.price_unit,
                "untaxed": line.price_subtotal,
                "tax": line.price_tax,
                "total": line.price_total,
            },
            "qty": line.product_uom_qty
        }

        return data

    def _retrieve_sale_orders(self, **params):
        """
            Return sale orders
            If the partner is associated with an LPI Partner,
            it returns the sale orders of both,
            otherwise only those that belong to it
        """

        partner_id = self.env.user.partner_id
        parent_id = partner_id.parent_id
        if parent_id:
            sale_order = (
                self.env["sale.order"]
                .sudo()
                .search([("partner_id", "in", [parent_id.id, partner_id.id])])
            )
        else:
            sale_order = self.env["sale.order"].sudo().search([("partner_id", "=", partner_id.id)])
        return sale_order
