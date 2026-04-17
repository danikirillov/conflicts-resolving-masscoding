// Pet Shop - Payment Processor
// Handles payment processing and validation

#include <string>
#include <map>
#include <vector>
#include <ctime>
#include <iostream>

class PaymentProcessor {
private:
    std::map<std::string, double> transactions;
    double processingFee;
    
public:
    PaymentProcessor() {
        processingFee = 0.029; // 2.9% processing fee
    }
    
    struct PaymentResult {
        bool success;
        std::string transactionId;
        std::string message;
        double amountCharged;
    };
    
    struct CardInfo {
        std::string cardNumber;
        std::string cardHolder;
        std::string expiryDate;
        std::string cvv;
    };
    
    // Process credit card payment
    PaymentResult processCardPayment(const CardInfo& card, double amount) {
        PaymentResult result;
        
        // Validate card information
        if (!validateCard(card)) {
            result.success = false;
            result.message = "Invalid card information";
            result.amountCharged = 0.0;
            return result;
        }
        
        // Validate amount
        if (amount <= 0) {
            result.success = false;
            result.message = "Invalid amount";
            result.amountCharged = 0.0;
            return result;
        }
        
        // Calculate total with processing fee
        double fee = amount * processingFee;
        double total = amount + fee;
        
        // Generate transaction ID
        std::string transactionId = generateTransactionId();
        
        // Process payment (simulated)
        transactions[transactionId] = total;
        
        result.success = true;
        result.transactionId = transactionId;
        result.message = "Payment processed successfully";
        result.amountCharged = total;
        
        return result;
    }
    
    // Validate credit card information
    bool validateCard(const CardInfo& card) {
        // Check card number length
        if (card.cardNumber.length() < 13 || card.cardNumber.length() > 19) {
            return false;
        }
        
        // Check if card number contains only digits
        for (char c : card.cardNumber) {
            if (!isdigit(c)) {
                return false;
            }
        }
        
        // Check CVV
        if (card.cvv.length() < 3 || card.cvv.length() > 4) {
            return false;
        }
        
        // Check expiry date format (MM/YY)
        if (card.expiryDate.length() != 5 || card.expiryDate[2] != '/') {
            return false;
        }
        
        return true;
    }
    
    // Luhn algorithm for card validation
    bool luhnCheck(const std::string& cardNumber) {
        int sum = 0;
        bool alternate = false;
        
        for (int i = cardNumber.length() - 1; i >= 0; i--) {
            int digit = cardNumber[i] - '0';
            
            if (alternate) {
                digit *= 2;
                if (digit > 9) {
                    digit -= 9;
                }
            }
            
            sum += digit;
            alternate = !alternate;
        }
        
        return (sum % 10 == 0);
    }
    
    // Refund a transaction
    PaymentResult refundTransaction(const std::string& transactionId, double amount) {
        PaymentResult result;
        
        // Check if transaction exists
        if (transactions.find(transactionId) == transactions.end()) {
            result.success = false;
            result.message = "Transaction not found";
            result.amountCharged = 0.0;
            return result;
        }
        
        double originalAmount = transactions[transactionId];
        
        if (amount > originalAmount) {
            result.success = false;
            result.message = "Refund amount exceeds original transaction";
            result.amountCharged = 0.0;
            return result;
        }
        
        result.success = true;
        result.transactionId = transactionId;
        result.message = "Refund processed successfully";
        result.amountCharged = amount;
        
        return result;
    }
    
    // Get transaction details
    double getTransaction(const std::string& transactionId) {
        if (transactions.find(transactionId) != transactions.end()) {
            return transactions[transactionId];
        }
        return -1.0;
    }
    
    // Calculate processing fee
    double calculateFee(double amount) {
        return amount * processingFee;
    }
    
    // Generate unique transaction ID
    std::string generateTransactionId() {
        std::time_t now = std::time(nullptr);
        return "TXN" + std::to_string(now) + std::to_string(rand() % 1000);
    }
    
    // Get all transactions
    std::map<std::string, double> getAllTransactions() {
        return transactions;
    }
    
    // Process PayPal payment
    PaymentResult processPayPalPayment(const std::string& email, double amount) {
        PaymentResult result;
        
        if (email.find('@') == std::string::npos) {
            result.success = false;
            result.message = "Invalid email address";
            result.amountCharged = 0.0;
            return result;
        }
        
        if (amount <= 0) {
            result.success = false;
            result.message = "Invalid amount";
            result.amountCharged = 0.0;
            return result;
        }
        
        std::string transactionId = generateTransactionId();
        transactions[transactionId] = amount;
        
        result.success = true;
        result.transactionId = transactionId;
        result.message = "PayPal payment processed successfully";
        result.amountCharged = amount;
        
        return result;
    }
};
