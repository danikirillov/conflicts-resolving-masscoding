package com.petshop.service;

import java.util.List;
import java.util.ArrayList;
import java.util.Optional;

/**
 * Pet Shop - Pet Service
 * Business logic for managing pets in the pet shop
 */
public class PetService {
    private List<Pet> pets;
    private int nextId;

    public PetService() {
        this.pets = new ArrayList<>();
        this.nextId = 1;
    }

    /**
     * Get all available pets
     */
    public List<Pet> getAllPets() {
        return new ArrayList<>(pets);
    }

    /**
     * Get pet by ID
     */
    public Optional<Pet> getPetById(int id) {
        return pets.stream()
                .filter(pet -> pet.getId() == id)
                .findFirst();
    }

    /**
     * Add a new pet to the shop
     */
    public Pet addPet(String name, String species, String breed, int age, double price) {
        Pet pet = new Pet(nextId++, name, species, breed, age, price);
        pets.add(pet);
        return pet;
    }

    /**
     * Update pet information
     */
    public boolean updatePet(int id, String name, String species, String breed, int age, double price) {
        Optional<Pet> petOpt = getPetById(id);
        if (petOpt.isPresent()) {
            Pet pet = petOpt.get();
            pet.setName(name);
            pet.setSpecies(species);
            pet.setBreed(breed);
            pet.setAge(age);
            pet.setPrice(price);
            return true;
        }
        return false;
    }

    /**
     * Remove a pet from the shop
     */
    public boolean removePet(int id) {
        return pets.removeIf(pet -> pet.getId() == id);
    }

    /**
     * Search pets by species
     */
    public List<Pet> searchBySpecies(String species) {
        List<Pet> results = new ArrayList<>();
        for (Pet pet : pets) {
            if (pet.getSpecies().equalsIgnoreCase(species)) {
                results.add(pet);
            }
        }
        return results;
    }

    /**
     * Фильтр питомцев по возрастному диапазону
     */
    public List<Pet> filterByAgeRange(int minAge, int maxAge) {
        List<Pet> results = new ArrayList<>();
        for (Pet pet : pets) {
            if (pet.getAge() >= minAge && pet.getAge() <= maxAge) {
                results.add(pet);
            }
        }
        return results;
    }

    /**
     * Filter pets by price range
     */
    public List<Pet> filterByPriceRange(double minPrice, double maxPrice) {
        List<Pet> results = new ArrayList<>();
        for (Pet pet : pets) {
            if (pet.getPrice() >= minPrice && pet.getPrice() <= maxPrice) {
                results.add(pet);
            }
        }
        return results;
    }

    /**
     * Inner class representing a Pet
     */
    public static class Pet {
        private int id;
        private String name;
        private String species;
        private String breed;
        private int age;
        private double price;

        public Pet(int id, String name, String species, String breed, int age, double price) {
            this.id = id;
            this.name = name;
            this.species = species;
            this.breed = breed;
            this.age = age;
            this.price = price;
        }

        // Getters and setters
        public int getId() { return id; }
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getSpecies() { return species; }
        public void setSpecies(String species) { this.species = species; }
        public String getBreed() { return breed; }
        public void setBreed(String breed) { this.breed = breed; }
        public int getAge() { return age; }
        public void setAge(int age) { this.age = age; }
        public double getPrice() { return price; }
        public void setPrice(double price) { this.price = price; }
    }
}
