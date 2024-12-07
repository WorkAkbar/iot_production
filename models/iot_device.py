from odoo import models, fields, api
from odoo.exceptions import ValidationError

class IoTDevice(models.Model):
    _name = 'iot.device'
    _description = 'IoT Device'

    name = fields.Char(string='Device Name', required=True)
    device_id = fields.Char(string='Device ID', required=True, unique=True)
    machine_id = fields.Many2one('mrp.workcenter', string='Linked Machine')
    status = fields.Selection(
        [('online', 'Online'), ('offline', 'Offline')],
        string='Status',
        default='offline'
    )
    last_data = fields.Float(string='Last Data')
    data_history = fields.One2many('iot.data', 'device_id', string='Data History')

    @api.model
    def create(self, vals):
        # Implement logic before creating IoT device
        # Custom logic can be added before record creation
        device = super(IoTDevice, self).create(vals)
        return device

    @api.constrains('device_id')
    def _check_device_id(self):
        for record in self:
            if len(record.device_id) < 5:
                raise ValidationError("Device ID must be at least 5 characters long.")

class IoTData(models.Model):
    _name = 'iot.data'
    _description = 'IoT Data'

    timestamp = fields.Datetime(string='Timestamp', default=fields.Datetime.now)
    device_id = fields.Many2one('iot.device', string='Device', required=True)
    value = fields.Float(string='Value')
    status = fields.Selection(
        [('normal', 'Normal'), ('warning', 'Warning'), ('critical', 'Critical')],
        string='Status',
        default='normal'
    )

    @api.model
    def create(self, vals):
        # Additional logic for IoT Data creation
        if 'value' in vals and vals['value'] < 0:
            raise ValidationError("Data value cannot be negative.")
        # Call parent class to create the record
        return super(IoTData, self).create(vals)

    @api.constrains('timestamp', 'device_id')
    def _check_data_timestamp(self):
        for record in self:
            # Ensure data for the same device has a unique timestamp
            existing_data = self.search([
                ('device_id', '=', record.device_id.id), 
                ('timestamp', '=', record.timestamp)
            ])
            if existing_data:
                raise ValidationError("Data for this device already exists for the given timestamp.")
