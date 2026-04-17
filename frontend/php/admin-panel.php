<?php
// Pet Shop - Admin Panel
// Administrative functions and dashboard

require_once 'database.php';
require_once 'auth.php';

class AdminPanel {
    private $db;
    private $auth;

    public function __construct() {
        $this->db = new Database();
        $this->auth = new Auth();
    }

    private function isAdmin() {
        $user = $this->auth->getCurrentUser();
        if (!$user) {
            return false;
        }

        $userData = $this->db->fetchOne(
            "SELECT role FROM users WHERE id = :id",
            ['id' => $user['id']]
        );

        return $userData && $userData['role'] === 'admin';
    }

    private function requireAdmin() {
        $this->auth->requireAuth();
        if (!$this->isAdmin()) {
            http_response_code(403);
            echo json_encode(['error' => 'Admin access required']);
            exit;
        }
    }

    public function getDashboardStats() {
        $this->requireAdmin();

        $stats = [];

        // Total products
        $result = $this->db->fetchOne("SELECT COUNT(*) as count FROM products WHERE status = 'active'");
        $stats['total_products'] = $result['count'];

        // Total orders
        $result = $this->db->fetchOne("SELECT COUNT(*) as count FROM orders");
        $stats['total_orders'] = $result['count'];

        // Total revenue
        $result = $this->db->fetchOne("SELECT SUM(total) as revenue FROM orders WHERE status = 'delivered'");
        $stats['total_revenue'] = $result['revenue'] ?? 0;

        // Total users
        $result = $this->db->fetchOne("SELECT COUNT(*) as count FROM users");
        $stats['total_users'] = $result['count'];

        // Pending orders
        $result = $this->db->fetchOne("SELECT COUNT(*) as count FROM orders WHERE status = 'pending'");
        $stats['pending_orders'] = $result['count'];

        // Low stock products
        $result = $this->db->fetchOne("SELECT COUNT(*) as count FROM products WHERE stock < 10 AND status = 'active'");
        $stats['low_stock_products'] = $result['count'];

        return $stats;
    }

    public function getRecentOrders($limit = 10) {
        $this->requireAdmin();

        return $this->db->fetchAll(
            "SELECT o.*, u.name as user_name, u.email as user_email 
             FROM orders o 
             JOIN users u ON o.user_id = u.id 
             ORDER BY o.created_at DESC 
             LIMIT :limit",
            ['limit' => $limit]
        );
    }

    public function getTopSellingProducts($limit = 10) {
        $this->requireAdmin();

        return $this->db->fetchAll(
            "SELECT p.id, p.name, p.price, SUM(oi.quantity) as total_sold 
             FROM products p 
             JOIN order_items oi ON p.id = oi.product_id 
             GROUP BY p.id 
             ORDER BY total_sold DESC 
             LIMIT :limit",
            ['limit' => $limit]
        );
    }

    public function getSalesReport($startDate, $endDate) {
        $this->requireAdmin();

        $sql = "SELECT 
                    DATE(created_at) as date,
                    COUNT(*) as order_count,
                    SUM(total) as daily_revenue
                FROM orders 
                WHERE created_at BETWEEN :start_date AND :end_date
                GROUP BY DATE(created_at)
                ORDER BY date DESC";

        return $this->db->fetchAll($sql, [
            'start_date' => $startDate,
            'end_date' => $endDate
        ]);
    }

    public function getAllUsers($page = 1, $perPage = 20) {
        $this->requireAdmin();

        $offset = ($page - 1) * $perPage;

        return $this->db->fetchAll(
            "SELECT id, name, email, created_at, last_login 
             FROM users 
             ORDER BY created_at DESC 
             LIMIT :limit OFFSET :offset",
            ['limit' => $perPage, 'offset' => $offset]
        );
    }
}
?>
