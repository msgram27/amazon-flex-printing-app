import requests
import json
import base64
import hashlib
import hmac
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class AmazonFlexClient:
    def __init__(self):
        self.simulation_mode = os.getenv('FLEX_SIMULATION_MODE', 'true').lower() == 'true'
        
    def get_flex_routes(self, start_time=None, end_time=None):
        """Get routes - simulation mode only"""
        if self.simulation_mode:
            return self._simulate_flex_routes()
        else:
            print("ERROR: Real Flex API access requires approved DSP status")
            return {'routes': []}
    
    def get_route_details(self, route_id):
        """Get detailed information for a specific route"""
        if self.simulation_mode:
            return self._simulate_route_details(route_id)
        else:
            print("ERROR: Real Flex API access requires approved DSP status")
            return None

    def acknowledge_route(self, route_id):
        """Acknowledge receipt of route - simulation only"""
        if self.simulation_mode:
            print(f"Simulated acknowledgment for route {route_id}")
            return True
        else:
            print("ERROR: Real Flex API access requires approved DSP status")
            return False
    
    def _simulate_flex_routes(self):
        """Simulate Flex route data"""
        return {
            'routes': [
                {
                    'routeId': 'SIM-ROUTE-001',
                    'driverName': 'Simulated Driver',
                    'vehicleType': 'SUV',
                    'startTime': (datetime.now() + timedelta(hours=1)).isoformat() + 'Z',
                    'endTime': (datetime.now() + timedelta(hours=5)).isoformat() + 'Z',
                    'totalStops': 8,
                    'totalPackages': 12
                }
            ]
        }
    
    def _simulate_route_details(self, route_id):
        """Simulate detailed route data"""
        return {
            'route': {
                'routeId': route_id,
                'driverName': 'Simulated Driver',
                'vehicleType': 'Medium SUV',
                'startTime': (datetime.now() + timedelta(hours=1)).isoformat() + 'Z',
                'endTime': (datetime.now() + timedelta(hours=5)).isoformat() + 'Z',
                'totalStops': 8,
                'totalPackages': 12,
                'estimatedMiles': 45.2
            },
            'stops': [
                {
                    'stopId': 'STOP-001',
                    'orderId': 'SIM-ORDER-001',
                    'customerName': 'John Smith',
                    'customerPhone': '555-0123',
                    'deliveryNotes': 'Leave at front door - Ring bell',
                    'address': {
                        'addressLine1': '123 Main Street',
                        'city': 'Seattle',
                        'state': 'WA',
                        'postalCode': '98101'
                    },
                    'packages': 2,
                    'estimatedArrival': '14:30'
                },
                {
                    'stopId': 'STOP-002',
                    'orderId': 'SIM-ORDER-002',
                    'customerName': 'Maria Garcia',
                    'customerPhone': '555-0124',
                    'deliveryNotes': 'Back porch - Beware of dog',
                    'address': {
                        'addressLine1': '456 Oak Avenue',
                        'city': 'Seattle',
                        'state': 'WA',
                        'postalCode': '98102'
                    },
                    'packages': 1,
                    'estimatedArrival': '14:45'
                },
                {
                    'stopId': 'STOP-003',
                    'orderId': 'SIM-ORDER-003',
                    'customerName': 'Robert Johnson',
                    'customerPhone': '555-0125',
                    'deliveryNotes': 'Front desk reception',
                    'address': {
                        'addressLine1': '789 Pine Road',
                        'city': 'Bellevue',
                        'state': 'WA',
                        'postalCode': '98004'
                    },
                    'packages': 3,
                    'estimatedArrival': '15:15'
                }
            ]
        }