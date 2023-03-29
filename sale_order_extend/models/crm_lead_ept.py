from odoo import models, fields


class CrmLeadEpt(models.Model):
    # _name = "crm.lead"
    _inherit = "crm.lead"

    def action_new_quotation(self):
        action = super(CrmLeadEpt, self).action_new_quotation()

        tag_ids=self.env.ref('sale_order_extend.first_crm_tag').id
        action['context']['default_crm_lead_ept_id'] = self.id
        action['context']['default_tag_ids'][0][2].append(tag_ids)

        return action
