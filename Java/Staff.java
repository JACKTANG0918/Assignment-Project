/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package model;
import java.io.Serializable;
import java.util.Calendar;
import util.Validator;

/**
 *
 * @author honor
 */
public abstract class Staff extends Person implements Serializable {
    // Serialized version number to ensure compatibility
    private static final long serialVersionUID = 2L;

    // Employee-specific attributes
    protected String specialty;
    protected int joinYear;

    // Empty constructor
    public Staff() {}
    
    public Staff(String username, String password, String name, String ic, int age, String gender, String phone, String address, String specialty, int joinYear) {
        // Call the constructor of the super class Person (verification of username, password, IC, and phone number has been completed)
        super(username, password, name, ic, age, gender, phone, address);
        // Verify and set employee-specific attributes
        this.setSpecialty(specialty);
        this.setJoinYear(joinYear);
    }

    // Getters and Setters for Employee-Specific Properties
    public String getSpecialty() { return specialty; }
    public void setSpecialty(String specialty) {
        if (Validator.validateSpecialty(specialty)) {
            this.specialty = specialty;
        } else {
            throw new IllegalArgumentException("The format of the department name is incorrect (3-50 characters) ");
        }
    }

    public int getJoinYear() { return joinYear; }
    public void setJoinYear(int joinYear) {
        if (Validator.validateJoinYear(joinYear)) {
            this.joinYear = joinYear;
        } else {
            throw new IllegalArgumentException("Invalid year of employment (1900-" + Calendar.getInstance().get(Calendar.YEAR) + ")");
        }
    }

    @Override
    public String toString() {
        return String.format(
            "%s\nSpecialty: %s\nJoin Year: %d",
            super.toString(),
            specialty,
            joinYear
        );
    }
}
