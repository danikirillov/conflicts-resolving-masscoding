// Pet Shop - Pet Details Display
// Shows detailed information about individual pets

class PetDetails {
    constructor(petId) {
        this.petId = petId;
        this.pet = null;
    }

    async loadPetDetails() {
        try {
            const response = await fetch(`/api/pets/${this.petId}`);
            this.pet = await response.json();
            this.displayDetails();
        } catch (error) {
            console.error('Error loading pet details:', error);
        }
    }

    displayDetails() {
        const container = document.getElementById('pet-details');
        
        container.innerHTML = `
            <div class="pet-gallery">
                <img src="${this.pet.mainImage}" alt="${this.pet.name}">
            </div>
            <div class="pet-info">
                <h1>${this.pet.name}</h1>
                <p class="breed">${this.pet.breed}</p>
                <p class="age">Age: ${this.pet.age} months</p>
                <p class="price">$${this.pet.price}</p>
                <p class="description">${this.pet.description}</p>
                
                <div class="specifications">
                    <h3>Specifications</h3>
                    <ul>
                        <li>Size: ${this.pet.size}</li>
                        <li>Color: ${this.pet.color}</li>
                        <li>Gender: ${this.pet.gender}</li>
                        <li>Vaccinated: ${this.pet.vaccinated ? 'Yes' : 'No'}</li>
                    </ul>
                </div>
                
                <button onclick="adoptPet(${this.petId})">Adopt Me</button>
            </div>
        `;
    }

    showImageGallery(images) {
        // Display multiple pet images
        const gallery = document.createElement('div');
        gallery.className = 'image-gallery';
        
        images.forEach(img => {
            const imgElement = document.createElement('img');
            imgElement.src = img;
            gallery.appendChild(imgElement);
        });
        
        return gallery;
    }
}
