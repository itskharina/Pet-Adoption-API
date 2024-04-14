CREATE DATABASE PetAdoption;

USE PetAdoption;

-- Create the Pets table
CREATE TABLE Pets (
    `pet_id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255),
    `species` VARCHAR(50),
    `age` INT,
    `description` VARCHAR(255),
    `available` BOOLEAN
);

-- Create the Adoption table
CREATE TABLE Adoption (
    `adoption_id` INT AUTO_INCREMENT PRIMARY KEY,
    `pet_id` INT,
    `adopter_name` VARCHAR(255),
    `contact_info` VARCHAR(255),
    `adoption_date` DATE,
    FOREIGN KEY (`pet_id`) REFERENCES Pets(`pet_id`)
);

-- Insert mock data into the Pets table
INSERT INTO Pets (name, species, age, description, available)
VALUES
    ('Bella', 'Dog', 3, 'Friendly Labrador mix', true),
    ('Whiskers', 'Cat', 2, 'Playful orange tabby', true),
    ('Snowball', 'Rabbit', 1, 'Fluffy white bunny', true),
    ('Rocky', 'Dog', 5, 'Energetic Terrier', false),
    ('Mittens', 'Cat', 4, 'Shy black-and-white Munchkin', true),
	('Fluffykins', 'Cat', 2, 'Adorable long-haired Siamese mix', false),
    ('Max', 'Dog', 4, 'Loyal Golden Retriever with a playful spirit', false),
    ('Nibbles', 'Rabbit', 3, 'Curious and friendly Holland Lop', false);

-- Insert mock data into the Adoption table
INSERT INTO Adoption (pet_id, adopter_name, contact_info, adoption_date)
VALUES
    (4, 'John Smith', 'john@example.com', '2024-04-10'),
    (7, 'Emily Brown', 'emily@example.com', '2024-04-11'),
    (8, 'Alex Lee', 'alex@example.com', '2024-04-12'),
    (6, 'Sarah Clark', 'sarah@example.com', '2024-04-13');
