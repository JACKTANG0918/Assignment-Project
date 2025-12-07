/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package model;
import java.io.Serializable;
import java.text.SimpleDateFormat;
import java.util.Date;
import util.Validator;
import java.util.List;

/**
 *
 * @author honor
 */
public class Appointment implements Serializable {
    private String patientIC;
    private String department;
    private Date appointmentTime;
    private String status = "PENDING"; // PENDING, COMPLETED, CANCELLED
    private String assignedDoctor;
    private String notes;

    // Empty Constructor
    public Appointment() {}

    public Appointment(String patientIC, String department, Date appointmentTime, String assignedDoctor) throws IllegalArgumentException {
        if (!Validator.validateIC(patientIC)) {
            throw new IllegalArgumentException("Invalid patient IC format");
        }
        this.patientIC = patientIC;
        this.department = department;
        this.appointmentTime = appointmentTime;
        this.status = "PENDING";    //Default state
        this.assignedDoctor = assignedDoctor;   // Initialize doctor assignment status
    }
    
    public static boolean hasConflict(List<Appointment> apps, Date newTime) {
        return apps.stream().anyMatch(a -> 
            Math.abs(a.getAppointmentTime().getTime() - newTime.getTime()) < 30 * 60 * 1000 // 30 minute interval
        );
    }

    public String getPatientIC() { return patientIC; }
    
    public void setPatientIC(String patientIC) {
        this.patientIC = patientIC;
    }
    
    public String getDepartment() { return department; }
    public void setDepartment(String department) {
        if (department.length() >= 3 && department.length() <= 50) {
            this.department = department;
        }
    }

    public Date getAppointmentTime() { return appointmentTime; }
    public void setAppointmentTime(Date appointmentTime) {
        if (appointmentTime.after(new Date())) {    // Cannot make reservations for past times
            this.appointmentTime = appointmentTime;
        }
    }

    public String getStatus() { return status; }
    public void setStatus(String status) {
        if (List.of("PENDING", "COMPLETED", "CANCELLED").contains(status)) {
            this.status = status;
        }
    }

    public String getAssignedDoctor() { return assignedDoctor; }
    public void setAssignedDoctor(String doctorUsername) {
        if (Validator.validateUsername(doctorUsername)) {
            this.assignedDoctor = doctorUsername;
        }
    }

    public String getNotes() { return notes; }
    public void setNotes(String notes) {
                this.notes = notes.substring(0, Math.min(notes.length(), 200)); // Limit to 200 characters
    }

    @Override
    public String toString() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");
        return String.format(
            "[Appointment] %s | Dept: %s\nPatient IC: %s\nDoctor: %s",
            sdf.format(appointmentTime),
            department,
            patientIC,
            assignedDoctor != null ? assignedDoctor : "Not assigned"
        );
    }
    
    
}
