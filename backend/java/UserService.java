package com.petshop.service;

import java.util.List;
import java.util.ArrayList;
import java.util.Optional;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/**
 * Pet Shop - User Service
 * Manages user accounts and authentication
 */
public class UserService {
    private List<User> users;
    private int nextUserId;

    public UserService() {
        this.users = new ArrayList<>();
        this.nextUserId = 1;
    }

    /**
     * Register a new user
     */
    public User registerUser(String email, String password, String name) {
        // Check if email already exists
        if (getUserByEmail(email).isPresent()) {
            throw new IllegalArgumentException("Email already registered");
        }

        String hashedPassword = hashPassword(password);
        User user = new User(nextUserId++, email, hashedPassword, name);
        users.add(user);
        return user;
    }

    /**
     * Authenticate user
     */
    public Optional<User> authenticateUser(String email, String password) {
        String hashedPassword = hashPassword(password);
        return users.stream()
                .filter(user -> user.getEmail().equals(email) && 
                               user.getPasswordHash().equals(hashedPassword))
                .findFirst();
    }

    /**
     * Get user by ID
     */
    public Optional<User> getUserById(int userId) {
        return users.stream()
                .filter(user -> user.getUserId() == userId)
                .findFirst();
    }

    /**
     * Get user by email
     */
    public Optional<User> getUserByEmail(String email) {
        return users.stream()
                .filter(user -> user.getEmail().equals(email))
                .findFirst();
    }

    /**
     * Update user profile
     */
    public boolean updateUserProfile(int userId, String name, String phone) {
        Optional<User> userOpt = getUserById(userId);
        if (userOpt.isPresent()) {
            User user = userOpt.get();
            user.setName(name);
            user.setPhone(phone);
            return true;
        }
        return false;
    }

    /**
     * Change user password
     */
    public boolean changePassword(int userId, String oldPassword, String newPassword) {
        Optional<User> userOpt = getUserById(userId);
        if (userOpt.isPresent()) {
            User user = userOpt.get();
            String oldHash = hashPassword(oldPassword);
            if (user.getPasswordHash().equals(oldHash)) {
                user.setPasswordHash(hashPassword(newPassword));
                return true;
            }
        }
        return false;
    }

    /**
     * Delete user account
     */
    public boolean deleteUser(int userId) {
        return users.removeIf(user -> user.getUserId() == userId);
    }

    /**
     * Hash password using SHA-256
     */
    private String hashPassword(String password) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(password.getBytes());
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("Error hashing password", e);
        }
    }

    /**
     * User class
     */
    public static class User {
        private int userId;
        private String email;
        private String passwordHash;
        private String name;
        private String phone;
        private boolean isActive;

        public User(int userId, String email, String passwordHash, String name) {
            this.userId = userId;
            this.email = email;
            this.passwordHash = passwordHash;
            this.name = name;
            this.phone = "";
            this.isActive = true;
        }

        // Getters and setters
        public int getUserId() { return userId; }
        public String getEmail() { return email; }
        public String getPasswordHash() { return passwordHash; }
        public void setPasswordHash(String passwordHash) { this.passwordHash = passwordHash; }
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getPhone() { return phone; }
        public void setPhone(String phone) { this.phone = phone; }
        public boolean isActive() { return isActive; }
        public void setActive(boolean active) { isActive = active; }
    }
}
