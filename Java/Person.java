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
// Person.java
public abstract class Person implements Serializable {
    // Serialized version number to ensure compatibility
    private static final long serialVersionUID = 1L;

    // Public properties
    protected String username;
    protected String password;
    protected String name;
    protected String ic;
    protected int age;
    protected String gender;
    protected String phone;
    protected String address;

    // Empty Constructor
    public Person() {}

    public Person(String username, String password, String name, String ic, int age, String gender, String phone, String address) {
        validateCredentials(username, password); // Verify username and password
        validatePersonalInfo(ic, phone);         // Verify IC and phone
        this.username = username;
        this.password = password;
        this.name = name;
        this.ic = ic;
        this.age = age;
        this.gender = gender;
        this.phone = phone;
        this.address = address;
    }

     // Verify username and password format
    protected void validateCredentials(String username, String password) {
        if (!Validator.validateUsername(username)) {
            throw new IllegalArgumentException("Username format is incorrect (must be 4 letters)");
        }
        if (!Validator.validatePassword(password)) {
            throw new IllegalArgumentException("The password format is incorrect (must be 6 digits)");
        }
    }

    // Verify IC and phone format
    protected void validatePersonalInfo(String ic, String phone) {
        if (!Validator.validateIC(ic)) {
            throw new IllegalArgumentException("The ID format is incorrect (example: 990101-01-1234)");
        }
        if (!Validator.validatePhone(phone)) {
            throw new IllegalArgumentException("The phone number format is incorrect (example: 012-3456789)");
        }
    }

    // Setter and Getter
    public String getUsername() { return username; }
    public void setUsername(String username) {
        if (Validator.validateUsername(username)) this.username = username;
    }

    public String getPassword() { return password; }
    public void setPassword(String password) {
        if (Validator.validatePassword(password)) this.password = password;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getIc() { return ic; }
    public void setIc(String ic) {
        if (Validator.validateIC(ic)) this.ic = ic;
    }

    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }

    public String getGender() { return gender; }
    public void setGender(String gender) { this.gender = gender; }

    public String getPhone() { return phone; }
    public void setPhone(String phone) {
        if (Validator.validatePhone(phone)) this.phone = phone;
    }

    public String getAddress() { return address; }
    public void setAddress(String address) { this.address = address; }

    @Override
    public String toString() {
        return String.format(
            "[Person] Username: %s | Name: %s | IC: %s | Phone: %s",
            username, name, ic, phone
        );
    }
}