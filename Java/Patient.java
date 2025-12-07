/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package model;
import java.io.Serializable;
import util.Validator;
/**
 *
 * @author honor
 */
public class Patient extends Person implements Serializable {
    // Serialized version number to ensure compatibility
    private static final long serialVersionUID = 1L;

    // Empty Constructor
    public Patient() {}

    public Patient(String username, String password, String name, String ic, int age, String gender, String phone, String address) {
        // Call the super class constructor（ Verify in person class)
        super(username, password, name, ic, age, gender, phone, address);
    }

    // Check if teh patient meets certain age criteria
    // @return true if the user is an adult (age ≥ 18), false otherwise
    public boolean isAdult() {
        return this.age >= 18;
    }

    @Override
    public String toString() {
        return String.format(
            "Patient Information:\n" +
            "Username: %s\n" +
            "Name: %s\n" +
            "IC: %s\n" +
            "Age: %d\n" +
            "Gender: %s\n" +
            "Phone: %s\n" +
            "Address: %s",
            getUsername(), getName(), getIc(), getAge(), getGender(), getPhone(), getAddress()
        );
    }
}