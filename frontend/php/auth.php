<?php
// Pet Shop - Authentication Manager
// Handles user login, registration, and session management

require_once 'database.php';

class Auth {
    private $db;
    private $sessionTimeout = 7200;

    public function __construct() {
        $this->db = new Database();
        if (session_status() === PHP_SESSION_NONE) {
            session_start();
        }
    }

    public function register($email, $password, $name) {
        // Validate input
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            return ['success' => false, 'message' => 'Invalid email format'];
        }

        if (strlen($password) < 8) {
            return ['success' => false, 'message' => 'Password must be at least 8 characters'];
        }

        // Check if user already exists
        $existing = $this->db->fetchOne(
            "SELECT id FROM users WHERE email = :email",
            ['email' => $email]
        );

        if ($existing) {
            return ['success' => false, 'message' => 'Email already registered'];
        }

        // Create new user
        $hashedPassword = password_hash($password, PASSWORD_BCRYPT);
        $userId = $this->db->insert('users', [
            'email' => $email,
            'password' => $hashedPassword,
            'name' => $name,
            'created_at' => date('Y-m-d H:i:s')
        ]);

        return ['success' => true, 'userId' => $userId];
    }

    public function login($email, $password) {
        $user = $this->db->fetchOne(
            "SELECT * FROM users WHERE email = :email",
            ['email' => $email]
        );

        if (!$user || !password_verify($password, $user['password'])) {
            return ['success' => false, 'message' => 'Invalid credentials'];
        }

        // Create session
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['user_email'] = $user['email'];
        $_SESSION['user_name'] = $user['name'];
        $_SESSION['login_time'] = time();

        // Update last login
        $this->db->update(
            'users',
            ['last_login' => date('Y-m-d H:i:s')],
            'id = :id',
            ['id' => $user['id']]
        );

        return ['success' => true, 'user' => $user];
    }

    public function logout() {
        session_unset();
        session_destroy();
        return ['success' => true];
    }

    public function isLoggedIn() {
        if (!isset($_SESSION['user_id'])) {
            return false;
        }

        // Check session timeout
        if (isset($_SESSION['login_time'])) {
            if ((time() - $_SESSION['login_time']) > $this->sessionTimeout) {
                $this->logout();
                return false;
            }
        }

        return true;
    }

    public function getCurrentUser() {
        if (!$this->isLoggedIn()) {
            return null;
        }

        return [
            'id' => $_SESSION['user_id'],
            'email' => $_SESSION['user_email'],
            'name' => $_SESSION['user_name']
        ];
    }

    public function requireAuth() {
        if (!$this->isLoggedIn()) {
            http_response_code(401);
            echo json_encode(['error' => 'Authentication required']);
            exit;
        }
    }
}
?>
