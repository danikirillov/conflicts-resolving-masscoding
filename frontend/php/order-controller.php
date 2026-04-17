<?php
// Pet Shop - Order Controller
// Manages customer orders and order processing

require_once 'database.php';
require_once 'auth.php';

class OrderController {
    private $db;
    private $auth;

    public function __construct() {
        $this->db = new Database();
        $this->auth = new Auth();
    }

    public function createOrder($orderData) {
        $this->auth->requireAuth();
        $user = $this->auth->getCurrentUser();

        // Validate order items
        if (!isset($orderData['items']) || empty($orderData['items'])) {
            http_response_code(400);
            return ['error' => 'Order must contain at least one item'];
        }

        // Calculate total
        $subtotal = 0;
        foreach ($orderData['items'] as $item) {
            $product = $this->db->fetchOne(
                "SELECT price, stock FROM products WHERE id = :id",
                ['id' => $item['product_id']]
            );

            if (!$product) {
                http_response_code(400);
                return ['error' => "Product not found: {$item['product_id']}"];
            }

            if ($product['stock'] < $item['quantity']) {
                http_response_code(400);
                return ['error' => "Insufficient stock for product {$item['product_id']}"];
            }

            $subtotal += $product['price'] * $item['quantity'];
        }

        $taxRate = 0.08;
        $tax = $subtotal * $taxRate;
        $total = $subtotal + $tax;

        // Create order
        $orderId = $this->db->insert('orders', [
            'user_id' => $user['id'],
            'subtotal' => $subtotal,
            'tax' => $tax,
            'total' => $total,
            'status' => 'pending',
            'created_at' => date('Y-m-d H:i:s')
        ]);

        // Create order items
        foreach ($orderData['items'] as $item) {
            $product = $this->db->fetchOne(
                "SELECT price FROM products WHERE id = :id",
                ['id' => $item['product_id']]
            );

            $this->db->insert('order_items', [
                'order_id' => $orderId,
                'product_id' => $item['product_id'],
                'quantity' => $item['quantity'],
                'price' => $product['price']
            ]);

            // Update stock
            $this->db->query(
                "UPDATE products SET stock = stock - :quantity WHERE id = :id",
                ['quantity' => $item['quantity'], 'id' => $item['product_id']]
            );
        }

        return [
            'success' => true,
            'order_id' => $orderId,
            'total' => $total
        ];
    }

    public function getOrderById($orderId) {
        $this->auth->requireAuth();
        $user = $this->auth->getCurrentUser();

        $order = $this->db->fetchOne(
            "SELECT * FROM orders WHERE id = :id AND user_id = :user_id",
            ['id' => $orderId, 'user_id' => $user['id']]
        );

        if (!$order) {
            http_response_code(404);
            return ['error' => 'Order not found'];
        }

        // Get order items
        $items = $this->db->fetchAll(
            "SELECT oi.*, p.name, p.image_url 
             FROM order_items oi 
             JOIN products p ON oi.product_id = p.id 
             WHERE oi.order_id = :order_id",
            ['order_id' => $orderId]
        );

        $order['items'] = $items;

        return $order;
    }

    public function getUserOrders($userId) {
        $this->auth->requireAuth();

        return $this->db->fetchAll(
            "SELECT * FROM orders 
             WHERE user_id = :user_id 
             ORDER BY created_at DESC",
            ['user_id' => $userId]
        );
    }

    public function updateOrderStatus($orderId, $status) {
        $this->auth->requireAuth();

        $validStatuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled'];
        if (!in_array($status, $validStatuses)) {
            http_response_code(400);
            return ['error' => 'Invalid status'];
        }

        $this->db->update(
            'orders',
            ['status' => $status, 'updated_at' => date('Y-m-d H:i:s')],
            'id = :id',
            ['id' => $orderId]
        );

        return ['success' => true];
    }

    public function cancelOrder($orderId) {
        $this->auth->requireAuth();
        $user = $this->auth->getCurrentUser();

        $order = $this->db->fetchOne(
            "SELECT * FROM orders WHERE id = :id AND user_id = :user_id",
            ['id' => $orderId, 'user_id' => $user['id']]
        );

        if (!$order) {
            http_response_code(404);
            return ['error' => 'Order not found'];
        }

        if ($order['status'] !== 'pending') {
            http_response_code(400);
            return ['error' => 'Can only cancel pending orders'];
        }

        // Restore stock
        $items = $this->db->fetchAll(
            "SELECT product_id, quantity FROM order_items WHERE order_id = :order_id",
            ['order_id' => $orderId]
        );

        foreach ($items as $item) {
            $this->db->query(
                "UPDATE products SET stock = stock + :quantity WHERE id = :id",
                ['quantity' => $item['quantity'], 'id' => $item['product_id']]
            );
        }

        // Update order status
        $this->updateOrderStatus($orderId, 'cancelled');

        return ['success' => true];
    }
}
?>
