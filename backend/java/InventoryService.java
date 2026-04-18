package com.petshop.service;

import java.util.HashMap;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;

/**
 * Pet Shop - Inventory Service
 * Manages product inventory and stock levels
 */
public class InventoryService {
    private Map<Integer, InventoryItem> inventory;
    private int lowStockThreshold;

    public InventoryService() {
        this.inventory = new HashMap<>();
        this.lowStockThreshold = 5;
    }

    /**
     * Add item to inventory
     */
    public void addInventoryItem(int productId, String productName, int quantity, double cost) {
        if (inventory.containsKey(productId)) {
            InventoryItem item = inventory.get(productId);
            item.setQuantity(item.getQuantity() + quantity);
        } else {
            InventoryItem item = new InventoryItem(productId, productName, quantity, cost);
            inventory.put(productId, item);
        }
    }

    /**
     * Get inventory item
     */
    public InventoryItem getInventoryItem(int productId) {
        return inventory.get(productId);
    }

    /**
     * Update stock quantity
     */
    public boolean updateStock(int productId, int quantity) {
        if (inventory.containsKey(productId)) {
            inventory.get(productId).setQuantity(quantity);
            return true;
        }
        return false;
    }

    /**
     * Reduce stock when item is sold
     */
    public boolean reduceStock(int productId, int quantity) {
        if (inventory.containsKey(productId)) {
            InventoryItem item = inventory.get(productId);
            if (item.getQuantity() >= quantity) {
                item.setQuantity(item.getQuantity() - quantity);
                return true;
            }
        }
        return false;
    }

    /**
     * Increase stock when items are restocked
     */
    public boolean restockItem(int productId, int quantity) {
        if (inventory.containsKey(productId)) {
            InventoryItem item = inventory.get(productId);
            item.setQuantity(item.getQuantity() + quantity);
            return true;
        }
        return false;
    }

    /**
     * Check if item is in stock
     */
    public boolean isInStock(int productId, int requestedQuantity) {
        if (inventory.containsKey(productId)) {
            return inventory.get(productId).getQuantity() >= requestedQuantity;
        }
        return false;
    }

    /**
     * Get low stock items
     */
    public List<InventoryItem> getLowStockItems() {
        List<InventoryItem> lowStockItems = new ArrayList<>();
        for (InventoryItem item : inventory.values()) {
            if (item.getQuantity() < lowStockThreshold) {
                lowStockItems.add(item);
            }
        }
        return lowStockItems;
    }

    /**
     * Get all inventory items
     */
    public List<InventoryItem> getAllItems() {
        return new ArrayList<>(inventory.values());
    }

    /**
     * Remove item from inventory
     */
    public boolean removeItem(int productId) {
        return inventory.remove(productId) != null;
    }

    /**
     * Calculate total inventory value
     */
    public double calculateTotalValue() {
        double total = 0.0;
        for (InventoryItem item : inventory.values()) {
            total += item.getQuantity() * item.getCost();
        }
        return total;
    }

    /**
     * InventoryItem class
     */
    public static class InventoryItem {
        private int productId;
        private String productName;
        private int quantity;
        private double cost;

        public InventoryItem(int productId, String productName, int quantity, double cost) {
            this.productId = productId;
            this.productName = productName;
            this.quantity = quantity;
            this.cost = cost;
        }

        // Getters and setters
        public int getProductId() { return productId; }
        public String getProductName() { return productName; }
        public void setProductName(String productName) { this.productName = productName; }
        public int getQuantity() { return quantity; }
        public void setQuantity(int quantity) { this.quantity = quantity; }
        public double getCost() { return cost; }
        public void setCost(double cost) { this.cost = cost; }
    }
}
