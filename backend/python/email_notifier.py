"""
Pet Shop - Email Notifier
Sends email notifications for orders, promotions, and updates
"""

from typing import List, Dict, Optional
from datetime import datetime
import json


class EmailNotifier:
    def __init__(self):
        self.smtp_server = "smtp.petshop.com"
        self.smtp_port = 587
        self.sender_email = "noreply@petshop.com"
        self.email_queue: List[dict] = []

    def send_order_confirmation(self, customer_email: str, order_id: int, 
                               order_details: dict) -> bool:
        """Send order confirmation email"""
        subject = f"Order Confirmation #{order_id}"
        
        body = f"""
        Dear Customer,
        
        Thank you for your order!
        
        Order ID: {order_id}
        Order Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        Total: ${order_details.get('total', 0.0):.2f}
        
        Your order is being processed and will ship soon.
        
        Best regards,
        Pet Shop Team
        """
        
        return self._queue_email(customer_email, subject, body, 'order_confirmation')

    def send_shipping_notification(self, customer_email: str, order_id: int, 
                                   tracking_number: str) -> bool:
        """Send shipping notification email"""
        subject = f"Your Order #{order_id} Has Shipped!"
        
        body = f"""
        Dear Customer,
        
        Great news! Your order has been shipped.
        
        Order ID: {order_id}
        Tracking Number: {tracking_number}
        
        You can track your package at: https://tracking.petshop.com/{tracking_number}
        
        Best regards,
        Pet Shop Team
        """
        
        return self._queue_email(customer_email, subject, body, 'shipping')

    def send_welcome_email(self, customer_email: str, customer_name: str) -> bool:
        """Send welcome email to new customers"""
        subject = "Welcome to Pet Shop!"
        
        body = f"""
        Hello {customer_name},
        
        Welcome to Pet Shop! We're excited to have you as part of our community.
        
        As a thank you, here's a special discount code for your first order:
        WELCOME10 - 10% off your first purchase
        
        Happy shopping!
        
        Best regards,
        Pet Shop Team
        """
        
        return self._queue_email(customer_email, subject, body, 'welcome')

    def send_promotional_email(self, customer_emails: List[str], 
                              promotion_details: dict) -> int:
        """Send promotional email to multiple customers"""
        subject = promotion_details.get('subject', 'Special Offer from Pet Shop')
        body = promotion_details.get('body', '')
        
        sent_count = 0
        for email in customer_emails:
            if self._queue_email(email, subject, body, 'promotional'):
                sent_count += 1
        
        return sent_count

    def send_password_reset(self, customer_email: str, reset_token: str) -> bool:
        """Send password reset email"""
        subject = "Password Reset Request"
        
        reset_link = f"https://petshop.com/reset-password?token={reset_token}"
        
        body = f"""
        Dear Customer,
        
        We received a request to reset your password.
        
        Click the link below to reset your password:
        {reset_link}
        
        This link will expire in 24 hours.
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        Pet Shop Team
        """
        
        return self._queue_email(customer_email, subject, body, 'password_reset')

    def send_low_stock_alert(self, admin_email: str, products: List[dict]) -> bool:
        """Send low stock alert to administrators"""
        subject = "Low Stock Alert - Action Required"
        
        product_list = "\n".join([
            f"- {p['name']}: {p['quantity']} remaining"
            for p in products
        ])
        
        body = f"""
        Administrator,
        
        The following products are running low on stock:
        
        {product_list}
        
        Please reorder these items to avoid stockouts.
        
        Pet Shop System
        """
        
        return self._queue_email(admin_email, subject, body, 'low_stock_alert')

    def _queue_email(self, recipient: str, subject: str, body: str, 
                    email_type: str) -> bool:
        """Add email to queue for sending"""
        email = {
            'recipient': recipient,
            'subject': subject,
            'body': body,
            'type': email_type,
            'queued_at': datetime.now(),
            'status': 'pending'
        }
        
        self.email_queue.append(email)
        return True

    def get_queue_status(self) -> dict:
        """Get status of email queue"""
        return {
            'total': len(self.email_queue),
            'pending': len([e for e in self.email_queue if e['status'] == 'pending']),
            'sent': len([e for e in self.email_queue if e['status'] == 'sent']),
            'failed': len([e for e in self.email_queue if e['status'] == 'failed'])
        }

    def clear_queue(self):
        """Clear all emails from queue"""
        self.email_queue.clear()
