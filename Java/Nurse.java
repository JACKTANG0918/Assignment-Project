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
public class Nurse extends Staff implements Serializable {
    // Serialized version number to ensure compatibility
    private static final long serialVersionUID = 4L;

    // Empty constructor
    public Nurse() {}

    public Nurse(String username, String password, String name, String ic, int age, String gender, String phone, String address, String specialty, int joinYear) {
        // Call the Staff parent class constructor (all level validations completed)
        super(username, password, name, ic, age, gender, phone, address, specialty, joinYear);
    }

    // Check if the nurse works in a specified department (example method)
    // ​@param targetSpecialty target department
    // @return returns true if the nurse's department matches the target
    public boolean isAssignedTo(String targetSpecialty) {
        return this.specialty.equalsIgnoreCase(targetSpecialty.trim());
    }

    @Override
    public String toString() {
        return String.format(
            "[Nurse]\n" +
            "Name: Nurse %s\n" +
            "Username: %s\n" +
            "Specialty: %s\n" +
            "Join Year: %d\n" +
            "Contact: %s | IC: %s",
            getName(), getUsername(), getSpecialty(), getJoinYear(), getPhone(), getIc()
        );
    }
}