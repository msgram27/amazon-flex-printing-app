from amazon_flex_client import AmazonFlexClient
from flex_printer_service import FlexPrinterService
import json
import time
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flex_app.log'),
        logging.StreamHandler()
    ]
)

class AmazonFlexPrintingApp:
    def __init__(self):
        self.flex_client = AmazonFlexClient()
        self.printer_service = FlexPrinterService()
        self.processed_routes = set()
    
    def load_processed_routes(self):
        """Load already processed routes from file"""
        try:
            with open('processed_routes.json', 'r') as f:
                return set(json.load(f))
        except FileNotFoundError:
            return set()
    
    def save_processed_routes(self):
        """Save processed routes to file"""
        with open('processed_routes.json', 'w') as f:
            json.dump(list(self.processed_routes), f)
    
    def process_new_routes(self):
        """Check for and process new Flex routes"""
        logging.info("Checking for new Flex routes...")
        
        try:
            # Get routes for today
            start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_time = start_time + timedelta(hours=24)
            
            routes_response = self.flex_client.get_flex_routes(start_time, end_time)
            routes = routes_response.get('routes', [])
            
            new_routes = [route for route in routes 
                         if route.get('routeId') not in self.processed_routes]
            
            logging.info(f"Found {len(new_routes)} new Flex routes to process")
            
            for route in new_routes:
                self.process_route(route)
                
        except Exception as e:
            logging.error(f"Error processing Flex routes: {e}")
    
    def process_route(self, route):
        """Process a single Flex route"""
        route_id = route.get('routeId')
        if not route_id:
            logging.error("Route has no ID")
            return
            
        logging.info(f"Processing Flex route: {route_id}")
        
        try:
            # Get detailed route information
            route_details = self.flex_client.get_route_details(route_id)
            if not route_details:
                logging.error(f"Could not get details for route {route_id}")
                return
            
            # Print route documents
            print_success = self.printer_service.print_route_documents(route_details)
            
            if print_success:
                logging.info(f"Successfully printed documents for route {route_id}")
                
                # Acknowledge route receipt
                ack_success = self.flex_client.acknowledge_route(route_id)
                if ack_success:
                    logging.info(f"Acknowledged route {route_id}")
                
                self.processed_routes.add(route_id)
                self.save_processed_routes()
            else:
                logging.error(f"Failed to print documents for route {route_id}")
                
        except Exception as e:
            logging.error(f"Error processing route {route_id}: {e}")
    
    def run_continuous(self, interval_minutes=15):
        """Run the Flex printing service continuously"""
        logging.info("Starting Amazon Flex printing service...")
        logging.info(f"Checking for new routes every {interval_minutes} minutes")
        
        while True:
            try:
                self.process_new_routes()
                time.sleep(interval_minutes * 60)
            except KeyboardInterrupt:
                logging.info("Stopping Flex printing service...")
                break
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    app = AmazonFlexPrintingApp()
    app.processed_routes = app.load_processed_routes()
    
    # Run once for testing
    app.process_new_routes()
    
    # Uncomment to run continuously (every 15 minutes for Flex)
    app.run_continuous(interval_minutes=15)