import socket
import os
from datetime import datetime  # ← ADD THIS IMPORT
from dotenv import load_dotenv

load_dotenv()

class FlexPrinterService:
    def __init__(self):
        self.printer_ip = os.getenv('PRINTER_IP', '192.168.1.100')
        self.printer_port = int(os.getenv('PRINTER_PORT', 9100))
        self.printer_model = os.getenv('PRINTER_MODEL', 'ZPL')
    
    def print_zpl_label(self, zpl_code):
        """Print ZPL code to network printer"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.printer_ip, self.printer_port))
                sock.sendall(zpl_code.encode())
                return True
        except Exception as e:
            print(f"Printing error: {e}")
            return False
    
    def generate_route_summary_zpl(self, route_data):
        """Generate ZPL for route summary sheet"""
        route = route_data.get('route', {})
        stops = route_data.get('stops', [])
        
        zpl_template = f"""
^XA
^FO50,30^A0N,60,60^FDFLEX ROUTE SUMMARY^FS
^FO50,100^A0N,30,30^FDRoute ID: {route.get('routeId', 'N/A')}^FS
^FO50,140^A0N,30,30^FDDriver: {route.get('driverName', 'N/A')}^FS
^FO50,180^A0N,30,30^FDVehicle: {route.get('vehicleType', 'N/A')}^FS
^FO50,220^A0N,30,30^FDStops: {len(stops)}^FS
^FO50,260^A0N,30,30^FDStart: {route.get('startTime', 'N/A')}^FS
^FO50,300^A0N,30,30^FDEnd: {route.get('endTime', 'N/A')}^FS
^FO50,340^GB700,3,3^FS
^FO50,360^A0N,25,25^FDStop Overview:^FS
"""
        
        y_position = 400
        for i, stop in enumerate(stops[:5]):  # First 5 stops
            zpl_template += f"^FO50,{y_position}^A0N,25,25^FD{i+1}. {stop.get('address', {}).get('addressLine1', 'N/A')}^FS\n"
            y_position += 40
        
        if len(stops) > 5:
            zpl_template += f"^FO50,{y_position}^A0N,25,25^FD... and {len(stops)-5} more stops^FS\n"
            y_position += 40
        
        zpl_template += f"^FO50,{y_position + 40}^A0N,20,20^FDGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}^FS"
        zpl_template += "^XZ"
        
        return zpl_template
    
    def generate_stop_label_zpl(self, stop_data, stop_number, total_stops):
        """Generate ZPL for individual stop label"""
        address = stop_data.get('address', {})
        
        zpl_template = f"""
^XA
^FO50,30^A0N,40,40^FDAMAZON FLEX^FS
^FO50,80^A0N,30,30^FDStop: {stop_number}/{total_stops}^FS
^FO50,120^A0N,25,25^FDOrder: {stop_data.get('orderId', 'N/A')}^FS
^FO50,160^A0N,25,25^FDCustomer: {stop_data.get('customerName', 'N/A')}^FS
^FO50,200^A0N,25,25^FDPhone: {stop_data.get('customerPhone', 'N/A')}^FS
^FO50,240^GB700,3,3^FS
^FO50,260^A0N,25,25^FDAddress:^FS
^FO50,300^A0N,25,25^FD{address.get('addressLine1', 'N/A')}^FS
^FO50,340^A0N,25,25^FD{address.get('city', 'N/A')}, {address.get('state', 'N/A')}^FS
^FO50,380^A0N,25,25^FD{address.get('postalCode', 'N/A')}^FS
^FO50,420^GB700,3,3^FS
^FO50,440^A0N,20,20^FDNotes: {stop_data.get('deliveryNotes', 'None')}^FS
^FO50,480^B3N,N,80,Y,N^FD{stop_data.get('orderId', 'STOP')}^FS
^XZ
"""
        return zpl_template
    
    def print_route_documents(self, route_data):
        """Print all documents for a route"""
        success = True
        
        # Print route summary
        summary_zpl = self.generate_route_summary_zpl(route_data)
        success &= self.print_zpl_label(summary_zpl)
        
        # Print individual stop labels
        stops = route_data.get('stops', [])
        for i, stop in enumerate(stops):
            stop_zpl = self.generate_stop_label_zpl(stop, i+1, len(stops))
            success &= self.print_zpl_label(stop_zpl)
            # Add page break between stops
            success &= self.print_zpl_label("^XA^XZ")
        
        return success