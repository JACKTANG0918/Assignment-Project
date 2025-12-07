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
public class Doctor extends Staff implements Serializable {
    // Serialized version number to ensure compatibility
    private static final long serialVersionUID = 3L;

    // Empty constructor
    public Doctor() {}

    public Doctor(String username, String password, String name, String ic, int age, String gender, String phone, String address, String specialty, int joinYear) {
        // Call the Staff super class constructor (all level validations completed)
        super(username, password, name, ic, age, gender, phone, address, specialty, joinYear);
    }

    // Check if the doctor is qualified for a specified department (example method)
    // ​​@param targetSpecialty target department
    // @return true if the doctor's department matches the target
    public boolean isQualifiedFor(String targetSpecialty) {
        return this.specialty.equalsIgnoreCase(targetSpecialty.trim());
    }

    @Override
    public String toString() {
        return String.format(
            "[Doctor]\n" +
            "Name: Dr.%s\n" +
            "Username: %s\n" +
            "Specialty: %s\n" +
            "Join Year: %d\n" +
            "Contact: %s | IC: %s",
            getName(), getUsername(), getSpecialty(), getJoinYear(), getPhone(), getIc()
        );
    }
}