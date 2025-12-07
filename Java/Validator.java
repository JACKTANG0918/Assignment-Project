/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package util;
import java.util.Calendar;

/**
 *
 * @author honor
 */
public class Validator {
    // General Validation Rules
    public static boolean validateUsername(String username) {
        return username.matches("^[a-zA-Z]{4}$");
    }

    public static boolean validatePassword(String password) {
        return password.matches("^\\d{6}$");
    }

    public static boolean validateIC(String ic) {
        return ic.matches("^\\d{6}-\\d{2}-\\d{4}$");
    }

    public static boolean validatePhone(String phone) {
        return phone.matches("^\\d{3}-\\d{7}$");
    }
    
    public static boolean validateGender(String gender) {
        return gender.matches("^(Male|Female|Other)$");
    }

    // Medical related verification
    public static boolean validateDepartment(String department) {
        return department.matches("^[a-zA-Z ]{3,50}$");
    }

    public static boolean validateDiagnosis(String diagnosis) {
        return diagnosis.length() >= 10 && diagnosis.length() <= 500;
    }

    public static boolean validateJoinYear(int year) {
        int currentYear = Calendar.getInstance().get(Calendar.YEAR);
        return year >= 1900 && year <= currentYear;
    }

    public static boolean validateAge(int age) {
        return age >= 0 && age <= 150;
    }

    public static boolean validateSpecialty(String specialty) {
        return specialty.matches("^[\\p{L}0-9& ]{3,50}$");
    }

    // Appontment time verification( cannot be in the past )
    public static boolean validateAppointmentTime(long timestamp) {
        return timestamp > System.currentTimeMillis();
    }
    
}