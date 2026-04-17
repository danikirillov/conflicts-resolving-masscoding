<?php
// Pet Shop - Product Controller
// Manages product-related operations and API endpoints

require_once 'database.php';
require_once 'auth.php';

class ProductController {
    private $db;
    private $auth;

    public function __construct() {
        $this->db = new Database();
        $this->auth = new Auth();
    }

    public function getAllProducts($filters = []) {
        $sql = "SELECT * FROM products WHERE status = 'active'";
        $params = [];

        // Apply filters
        if (isset($filters['category']) && $filters['category'] !== 'all') {
            $sql .= " AND category = :category";
            $params['category'] = $filters['category'];
        }

        if (isset($filters['min_price'])) {
            $sql .= " AND price >= :min_price";
            $params['min_price'] = $filters['min_price'];
        }

        if (isset($filters['max_price'])) {
            $sql .= " AND price <= :max_price";
            $params['max_price'] = $filters['max_price'];
        }

        $sql .= " ORDER BY name ASC";

        return $this->db->fetchAll($sql, $params);
    }

    public function getProductById($id) {
        $product = $this->db->fetchOne(
            "SELECT * FROM products WHERE id = :id",
            ['id' => $id]
        );

        if (!$product) {
            http_response_code(404);
            return ['error' => 'Product not found'];
        }

        return $product;
    }

    public function createProduct($data) {
        $this->auth->requireAuth();

        // Validate required fields
        $required = ['name', 'price', 'category', 'description'];
        foreach ($required as $field) {
            if (!isset($data[$field]) || empty($data[$field])) {
                http_response_code(400);
                return ['error' => "Missing required field: {$field}"];
            }
        }

        // Validate price
        if (!is_numeric($data['price']) || $data['price'] < 0) {
            http_response_code(400);
            return ['error' => 'Invalid price'];
        }

        $productData = [
            'name' => $data['name'],
            'price' => $data['price'],
            'category' => $data['category'],
            'description' => $data['description'],
            'stock' => $data['stock'] ?? 0,
            'image_url' => $data['image_url'] ?? null,
            'status' => 'active',
            'created_at' => date('Y-m-d H:i:s')
        ];

        $productId = $this->db->insert('products', $productData);

        return ['success' => true, 'product_id' => $productId];
    }

    public function updateProduct($id, $data) {
        $this->auth->requireAuth();

        $existing = $this->getProductById($id);
        if (isset($existing['error'])) {
            return $existing;
        }

        $updateData = [];
        $allowedFields = ['name', 'price', 'category', 'description', 'stock', 'image_url'];

        foreach ($allowedFields as $field) {
            if (isset($data[$field])) {
                $updateData[$field] = $data[$field];
            }
        }

        if (empty($updateData)) {
            http_response_code(400);
            return ['error' => 'No valid fields to update'];
        }

        $updateData['updated_at'] = date('Y-m-d H:i:s');

        $this->db->update('products', $updateData, 'id = :id', ['id' => $id]);

        return ['success' => true];
    }

    public function deleteProduct($id) {
        $this->auth->requireAuth();

        // Soft delete by setting status to inactive
        $this->db->update(
            'products',
            ['status' => 'inactive'],
            'id = :id',
            ['id' => $id]
        );

        return ['success' => true];
    }

    public function searchProducts($query) {
        $sql = "SELECT * FROM products 
                WHERE status = 'active' 
                AND (name LIKE :query OR description LIKE :query)
                ORDER BY name ASC";

        $searchTerm = "%{$query}%";
        return $this->db->fetchAll($sql, ['query' => $searchTerm]);
    }
}
?>
