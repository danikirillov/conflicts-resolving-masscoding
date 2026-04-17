package com.petshop.service;

import java.util.List;
import java.util.ArrayList;
import java.util.Date;
import java.util.Optional;

/**
 * Pet Shop - Order Service
 * Handles order processing and management
 */
public class OrderService {
    private List<Order> orders;
    private int nextOrderId;
    private double shippingCost;

    public OrderService() {
        this.orders = new ArrayList<>();
        this.nextOrderId = 1000;
        this.shippingCost = 10.0;
    }

    /**
     * Create a new order
     */
    public Order createOrder(int customerId, List<OrderItem> items) {
        double subtotal = calculateSubtotal(items);
        double tax = subtotal * 0.08;
        double total = subtotal + tax + shippingCost;

        Order order = new Order(
            nextOrderId++,
            customerId,
            new Date(),
            items,
            subtotal,
            tax,
            shippingCost,
            total,
            "PENDING"
        );

        orders.add(order);
        return order;
    }

    /**
     * Get order by ID
     */
    public Optional<Order> getOrderById(int orderId) {
        return orders.stream()
                .filter(order -> order.getOrderId() == orderId)
                .findFirst();
    }

    /**
     * Get all orders for a customer
     */
    public List<Order> getOrdersByCustomerId(int customerId) {
        List<Order> customerOrders = new ArrayList<>();
        for (Order order : orders) {
            if (order.getCustomerId() == customerId) {
                customerOrders.add(order);
            }
        }
        return customerOrders;
    }

    /**
     * Update order status
     */
    public boolean updateOrderStatus(int orderId, String status) {
        Optional<Order> orderOpt = getOrderById(orderId);
        if (orderOpt.isPresent()) {
            orderOpt.get().setStatus(status);
            return true;
        }
        return false;
    }

    /**
     * Cancel an order
     */
    public boolean cancelOrder(int orderId) {
        Optional<Order> orderOpt = getOrderById(orderId);
        if (orderOpt.isPresent()) {
            Order order = orderOpt.get();
            if ("PENDING".equals(order.getStatus())) {
                order.setStatus("CANCELLED");
                return true;
            }
        }
        return false;
    }

    /**
     * Calculate subtotal from order items
     */
    private double calculateSubtotal(List<OrderItem> items) {
        double subtotal = 0.0;
        for (OrderItem item : items) {
            subtotal += item.getPrice() * item.getQuantity();
        }
        return subtotal;
    }

    /**
     * Order class
     */
    public static class Order {
        private int orderId;
        private int customerId;
        private Date orderDate;
        private List<OrderItem> items;
        private double subtotal;
        private double tax;
        private double shipping;
        private double total;
        private String status;

        public Order(int orderId, int customerId, Date orderDate, List<OrderItem> items,
                     double subtotal, double tax, double shipping, double total, String status) {
            this.orderId = orderId;
            this.customerId = customerId;
            this.orderDate = orderDate;
            this.items = items;
            this.subtotal = subtotal;
            this.tax = tax;
            this.shipping = shipping;
            this.total = total;
            this.status = status;
        }

        // Getters and setters
        public int getOrderId() { return orderId; }
        public int getCustomerId() { return customerId; }
        public Date getOrderDate() { return orderDate; }
        public List<OrderItem> getItems() { return items; }
        public double getSubtotal() { return subtotal; }
        public double getTax() { return tax; }
        public double getShipping() { return shipping; }
        public double getTotal() { return total; }
        public String getStatus() { return status; }
        public void setStatus(String status) { this.status = status; }
    }

    /**
     * OrderItem class
     */
    public static class OrderItem {
        private int productId;
        private String productName;
        private int quantity;
        private double price;

        public OrderItem(int productId, String productName, int quantity, double price) {
            this.productId = productId;
            this.productName = productName;
            this.quantity = quantity;
            this.price = price;
        }

        public int getProductId() { return productId; }
        public String getProductName() { return productName; }
        public int getQuantity() { return quantity; }
        public double getPrice() { return price; }
    }
}
