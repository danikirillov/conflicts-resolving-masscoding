// Pet Shop - User Profile Management
// Manages user account information and preferences

class UserProfile {
    constructor() {
        this.user = null;
        this.preferences = {};
    }

    async loadProfile(userId) {
        try {
            const response = await fetch(`/api/users/${userId}`);
            this.user = await response.json();
            this.loadPreferences();
            this.displayProfile();
        } catch (error) {
            console.error('Error loading profile:', error);
        }
    }

    displayProfile() {
        const container = document.getElementById('profile-container');
        
        container.innerHTML = `
            <div class="profile-header">
                <img src="${this.user.avatar}" alt="${this.user.name}">
                <h2>${this.user.name}</h2>
                <p>${this.user.email}</p>
            </div>
            
            <div class="profile-details">
                <h3>Account Information</h3>
                <p>Member since: ${this.formatDate(this.user.joinedDate)}</p>
                <p>Total orders: ${this.user.orderCount}</p>
                <p>Loyalty points: ${this.user.loyaltyPoints}</p>
            </div>
            
            <div class="profile-preferences">
                <h3>Preferences</h3>
                <label>
                    <input type="checkbox" id="emailNotifications"> 
                    Receive email notifications
                </label>
                <label>
                    <input type="checkbox" id="smsNotifications"> 
                    Receive SMS notifications
                </label>
            </div>
        `;
    }

    async updateProfile(data) {
        try {
            const response = await fetch(`/api/users/${this.user.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            this.user = await response.json();
            this.displayProfile();
        } catch (error) {
            console.error('Error updating profile:', error);
        }
    }

    loadPreferences() {
        const saved = localStorage.getItem('userPreferences');
        if (saved) {
            this.preferences = JSON.parse(saved);
        }
    }

    formatDate(dateString) {
        return new Date(dateString).toLocaleDateString();
    }
}
