# controllers/main.py
from odoo import http
from odoo.http import request

class IoTController(http.Controller):

    @http.route('/iot/data', type='json', auth='public', methods=['POST'])
    def receive_data(self, **kwargs):
        """
        Endpoint untuk menerima data dari perangkat IoT dan menyimpannya ke Odoo.
        """
        device_id = kwargs.get('device_id')
        value = kwargs.get('value')

        if not device_id or value is None:
            return {'status': 'error', 'message': 'Missing device_id or value'}

        # Cari perangkat berdasarkan device_id
        device = request.env['iot.device'].sudo().search([('device_id', '=', device_id)], limit=1)
        if device:
            # Tentukan status berdasarkan value
            status = 'normal' if value < 70 else 'warning' if value < 90 else 'critical'

            # Simpan data perangkat IoT
            request.env['iot.data'].sudo().create({
                'device_id': device.id,
                'value': value,
                'status': status
            })

            # Update status perangkat
            if status == 'critical':
                device.status = 'offline'
            else:
                device.status = 'online'
            
            # Update nilai terakhir dari perangkat
            device.last_data = value

            return {'status': 'success', 'message': 'Data received and processed successfully'}

        return {'status': 'error', 'message': 'Device not found'}
