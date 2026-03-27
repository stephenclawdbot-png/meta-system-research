#!/usr/bin/env python3
"""
Memecoin Alert Monitor
Monitors the alerts directory and sends Telegram messages when new opportunities are found
"""

import os
import time
import json
import asyncio
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AlertMonitor(FileSystemEventHandler):
    def __init__(self, telegram_bot_token=None, chat_id=None):
        self.alerts_dir = "alerts"
        self.processed_alerts = set()
        self.telegram_bot_token = telegram_bot_token
        self.chat_id = chat_id
        
        # Create alerts directory if it doesn't exist
        os.makedirs(self.alerts_dir, exist_ok=True)
    
    def on_created(self, event):
        """Called when a new alert file is created"""
        if event.is_directory:
            return
            
        if event.src_path.endswith('.txt') and 'memecoin_alert_' in event.src_path:
            # Wait a moment for file to be fully written
            time.sleep(1)
            
            if event.src_path not in self.processed_alerts:
                self.processed_alerts.add(event.src_path)
                self.process_alert_file(event.src_path)
    
    def process_alert_file(self, file_path):
        """Read alert file and send Telegram message"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Extract the alert message (content before "Token Data:")
            if 'Token Data:' in content:
                alert_message = content.split('Token Data:')[0].strip()
            else:
                alert_message = content
            
            print(f"🎯 New alert detected: {file_path}")
            print(alert_message)
            
            # Here we would send the Telegram message
            # For now, we'll write to stdout
            self.send_alert(alert_message)
            
        except Exception as e:
            print(f"Error processing alert file {file_path}: {e}")
    
    def send_alert(self, message):
        """Send alert message (placeholder for Telegram integration)"""
        print("\n" + "="*50)
        print("📱 TELEGRAM ALERT WOULD BE SENT:")
        print(message)
        print("="*50 + "\n")
        
        # TODO: Implement actual Telegram bot sending
        # if self.telegram_bot_token and self.chat_id:
        #     # Send via Telegram bot
        #     pass

def start_monitoring():
    """Start monitoring the alerts directory"""
    monitor = AlertMonitor()
    observer = Observer()
    observer.schedule(monitor, path='alerts', recursive=False)
    observer.start()
    
    print("👀 Alert monitor started - watching for new memecoin alerts...")
    print("📁 Monitoring directory: alerts/")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    start_monitoring()