/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package main;

import model.*;
import util.*;
import java.util.*;
import java.text.*;
import java.io.*;
import java.util.function.Function;
import java.util.InputMismatchException;

/**
 * Core class for hospital management system operations.
 * Handles console-based user interactions including:
 * - Patient registration/login/appointments
 * - Staff (doctors/nurses) workflows
 * - Administrator account management
 * - Data persistence via FileUtil serialization
 */
public class HospitalSystem {
    // Shared resources
    private static Scanner sc = new Scanner(System.in);
    private static final SimpleDateFormat DATE_FORMAT = new SimpleDateFormat("dd/MM/yyyy HH:mm");
    
    // Session tracking
    private static Patient currentPatient;
    private static Doctor currentDoctor;
    private static Nurse currentNurse;
    
    // Main Enttry Point
    public static void main(String[] args) {
        initializeDataFiles();
        showMainMenu();
    }
    
    // System Initialization
    // Ensure critical system files exist and creates initial admin account. Creates empty data files if not present.
    private static void initializeDataFiles() {
        FileUtil.ensureDataDirectoryExists();
        File doctorFile = new File("data/doctors.dat");

        try {
            if (!doctorFile.exists() || doctorFile.length() == 0) {
                initializeAdminAccount();
                System.out.println("Admin account initialized: ADMN/123456");
            }
        } catch (Exception e) {
            System.err.println("Initialization Failed: " + e.getMessage());
            // Force file creation
            FileUtil.saveToFile(new ArrayList<>(), "doctors.dat");
        }
    }
    
    // Creates default admin account if no doctors exist in system. Admin credentials: ADMN/123456
    private static void initializeAdminAccount() {
        List<Doctor> doctors = new ArrayList<>();
        Doctor admin = new Doctor("ADMN", "123456", "Admin", "000000-00-0000", 30, "Male", "000-0000000", "System Address", "Administration", 2023);
        doctors.add(admin);

        try {
            FileUtil.saveToFile(doctors, "doctors.dat");
            System.out.println("Admin account created: ADMN/123456");
        } catch (Exception e) {
            System.err.println("Failed to create admin account: " + e.getMessage());
        }
    }
    
    private static String getInput(String prompt) {
        System.out.print(prompt);
        return sc.nextLine();
    }
    
    public static boolean validateSpecialty(String specialty) {
        return specialty.matches("^[\\p{L} ]{3,50}$"); // Support for multilingual characters
    }
    
    private static void clearScreen() {
        System.out.println("\n".repeat(25));
    }
    
    // Main Menu System
    private static void showMainMenu() {
        while (true) {
            clearScreen();
            System.out.println("+=====================================================================================================+");
            System.out.println("|                                   B E A C H     H O S P I T A L                                     |");
            System.out.println("+=====================================================================================================+");
            System.out.println("|                       H O S P I T A L   M A N A G E M E N T   S Y S T E M                           |");
            System.out.println("+=====================================================================================================+");
            System.out.println("1. Patient Portal");
            System.out.println("2. Staff Portal");
            System.out.println("3. Administrator Portal");
            System.out.println("4. Exit");
            System.out.print("Select option: ");

            switch (getIntInput("Select option: ", 1, 4)) {
                case 1: patientPortal(); 
                        break;
                case 2: staffPortal(); 
                        break;
                case 3: adminPortal(); 
                        break;
                case 4: System.exit(0);
            }
        }
    }

    // Patient Portal
    private static void patientPortal() {
        System.out.println("\n=== Patient Portal ===");
        System.out.println("1. Register");
        System.out.println("2. Login");
        System.out.println("3. Back");
        System.out.print("Select option: ");

        switch (getIntInput("Select option: ", 1, 3)) {
            case 1: registerPatient(); 
                    break;
            case 2: loginPatient(); 
                    break;
            case 3: return;
        }
    }

    private static void registerPatient() {
        System.out.println("\n--- Patient Registration ---");
        Patient p = new Patient();
        
        p.setUsername(getValidInput("Username (4 letters): ", Validator::validateUsername));
        p.setPassword(getValidInput("Password (6 digits): ", Validator::validatePassword));
        p.setName(getInput("Full Name: "));
        p.setIc(getValidInput("IC (e.g. 990101-01-1234): ", Validator::validateIC));
        p.setAge(getIntInput("Age: ", 0, 150));
        p.setGender(getValidInput("Gender (Male/Female/Other): ", Validator::validateGender));
        p.setPhone(getValidInput("Phone (e.g. 012-3456789): ", Validator::validatePhone));
        p.setAddress(getInput("Address: "));

        List<Patient> patients = FileUtil.readFromFile("patients.dat");
        patients.add(p);
        try {
            FileUtil.saveToFile(patients, "patients.dat");
            System.out.println("Registration successful!");
        } catch (Exception e) {
            System.err.println("Registration failed: " + e.getMessage());
        }
    }

    private static void loginPatient() {
        System.out.print("Username: ");
        String user = sc.next();
        System.out.print("Password: ");
        String pass = sc.next();

        List<Patient> patients = FileUtil.readFromFile("patients.dat");
        Optional<Patient> patient = patients.stream()
            .filter(p -> p.getUsername().equals(user) && p.getPassword().equals(pass))
            .findFirst();

        if (patient.isPresent()) {
            currentPatient = patient.get();
            patientDashboard();
        } else {
            System.out.println("Invalid credentials!");
        }
    }

    private static void patientDashboard() {
        while (true) {
            System.out.println("\n=== Patient Dashboard ===");
            System.out.println("1. Make Appointment");
            System.out.println("2. Manage Profile");
            System.out.println("3. View Medical Reports");
            System.out.println("4. Logout");
            System.out.print("Select option: ");

            switch (getIntInput("Select option: ", 1, 4)) {
                case 1: makeAppointment(); 
                        break;
                case 2: managePatientProfile(); 
                        break;
                case 3: viewMedicalReports(); 
                        break;
                case 4: { currentPatient = null; 
                        return; }
            }
        }
    }
    
    private static void printPatientTable(Patient patient) {
        System.out.println("+---------------------+---------------------------------------+");
        System.out.printf("| %-20s | %-35s |%n", "Field", "Current Value");
        System.out.println("+---------------------+---------------------------------------+");
        System.out.printf("| %-20s | %-35s |%n", "Username", patient.getUsername());
        System.out.printf("| %-20s | %-35s |%n", "Name", patient.getName());
        System.out.printf("| %-20s | %-35s |%n", "IC", patient.getIc());
        System.out.printf("| %-20s | %-35s |%n", "Age", patient.getAge());
        System.out.printf("| %-20s | %-35s |%n", "Gender", patient.getGender());
        System.out.printf("| %-20s | %-35s |%n", "Phone", patient.getPhone());
        System.out.printf("| %-20s | %-35s |%n", "Address", patient.getAddress());
        System.out.println("+---------------------+---------------------------------------+");
    }
    
    private static void managePatientProfile() {
        System.out.println("\n------------------- Manage Patient Profile -------------------");
        printPatientTable(currentPatient);
        System.out.println("1. Change Password");
        System.out.println("2. Update Phone Number");
        System.out.println("3. Update Address");
        System.out.println("4. Back");

        switch (getIntInput("Select option: ", 1, 4)) {
            case 1: String newPass = getValidInput("New Password (6 digits): ", Validator::validatePassword);
                    currentPatient.setPassword(newPass);
                    updatePatientData();
                    break;
            case 2: String newPhone = getValidInput("New Phone (e.g. 012-3456789): ", Validator::validatePhone);
                    currentPatient.setPhone(newPhone);
                    updatePatientData();
                    break;
            case 3: String newAddr = getInput("New Address: ");
                    currentPatient.setAddress(newAddr);
                    updatePatientData();
                    break;
        }
    }

    private static void updatePatientData() {
        List<Patient> patients = FileUtil.readFromFile("patients.dat");
        patients.removeIf(p -> p.getUsername().equals(currentPatient.getUsername()));
        patients.add(currentPatient);
        FileUtil.saveToFile(patients, "patients.dat");
        System.out.println("Profile updated!");
    }
    
    private static void viewMedicalReports() {
        System.out.println("\n--------------------------------------------- View Medical Reports -----------------------------------------------");
        List<MedicalReport> reports = FileUtil.readFromFile("reports.dat");
        List<Patient> patients = FileUtil.readFromFile("patients.dat");

        System.out.println("+------------------+----------------------+-----------------+-----------------+----------------------+-----------------------------+");
        System.out.println("| Report ID        | Date                 | Patient Name    | Patient IC      | Gender               | Diagnosis                   |");
        System.out.println("+------------------+----------------------+-----------------+-----------------+----------------------+-----------------------------+");

        reports.stream()
            .filter(r -> r.getPatientIC().equals(currentPatient.getIc()))
            .forEach(report -> {
                Patient p = patients.stream()
                    .filter(patient -> patient.getIc().equals(report.getPatientIC()))
                    .findFirst()
                    .orElse(null);

                String diagnosis = report.getDiagnosis().length() > 25 ? 
                    report.getDiagnosis().substring(0, 22) + "..." : 
                    report.getDiagnosis();

                System.out.printf(
                    "| %-16s | %-20s | %-15s | %-15s | %-20s | %-27s |%n",
                    report.getReportID(),
                    new SimpleDateFormat("dd/MM/yyyy HH:mm").format(report.getReportDate()),
                    (p != null ? p.getName() : "Unknown"),
                    report.getPatientIC(),
                    (p != null ? p.getGender() : "Unknown"),
                    diagnosis
                );
            });
        System.out.println("+------------------+----------------------+-----------------+-----------------+----------------------+-----------------------------+");
    }

    private static void makeAppointment() {
        System.out.println("\n--- New Appointment ---");
        Appointment app = new Appointment();
        app.setPatientIC(currentPatient.getIc());
        app.setDepartment(getValidInput("Department: ", Validator::validateDepartment));
        app.setAppointmentTime(getDateInput("Appointment Date & Time (dd/MM/yyyy HH:mm): "));
        
        System.out.print("Assign Doctor (Username): ");
        String doctorUsername;
        do {
            doctorUsername = sc.nextLine().trim();
            if (!validateDoctorExists(doctorUsername)) {
                System.out.println("Doctor not found! Try again:");
            }
        } while (!validateDoctorExists(doctorUsername));
        app.setAssignedDoctor(doctorUsername);
        
        List<Appointment> appointments = FileUtil.readFromFile("appointments.dat");
        if (Appointment.hasConflict(appointments, app.getAppointmentTime())) {
            System.out.println("Time slot conflict!");
            return;
        }
        appointments.add(app);
        FileUtil.saveToFile(appointments, "appointments.dat");
        System.out.println("\nAppointment created:\n" + app);
    }
    
    // Staff Portal
    private static void staffPortal() {
        System.out.println("\n=== Staff Portal ===");
        System.out.println("1. Doctor Login");
        System.out.println("2. Nurse Login");
        System.out.println("3. Back");
        System.out.print("Select option: ");

        switch (getIntInput("Select option: ", 1, 3)) {
            case 1: loginDoctor(); 
                    break;
            case 2: loginNurse(); 
                    break;
            case 3: return;
        }
    }

    private static void loginDoctor() {
        System.out.print("Username: ");
        String user = sc.nextLine().trim();
        System.out.print("Password: ");
        String pass = sc.nextLine().trim();

        List<Doctor> doctors = FileUtil.readFromFile("doctors.dat");
        Optional<Doctor> doctor = doctors.stream()
            .filter(d -> d.getUsername().equals(user) && d.getPassword().equals(pass))
            .findFirst();

        if (doctor.isPresent()) {
            currentDoctor = doctor.get();
            doctorDashboard();
        } else {
            System.out.println("Invalid credentials!");
        }
    }
    
    private static void loginNurse() {
        System.out.print("Username: ");
        String user = sc.nextLine().trim();
        System.out.print("Password: ");
        String pass = sc.nextLine().trim();

        List<Nurse> nurses = FileUtil.readFromFile("nurses.dat");
        Optional<Nurse> nurse = nurses.stream()
            .filter(n -> n.getUsername().equals(user) && n.getPassword().equals(pass))
            .findFirst();

        if (nurse.isPresent()) {
            currentNurse = nurse.get();
            nurseDashboard();
        } else {
            System.out.println("Invalid credentials!");
        }
    }

    private static void doctorDashboard() {
        while (true) {
            System.out.println("\n=== Doctor Dashboard ===");
            System.out.println("1. Manage Profile");
            System.out.println("2. View Schedule");
            System.out.println("3. Manage Medical Reports");
            System.out.println("4. Logout");
            System.out.print("Select option: ");

            switch (getIntInput("Select option: ", 1, 4)) {
                case 1: manageDoctorProfile(); 
                        break;
                case 2: viewDoctorSchedule(); 
                        break;
                case 3: manageMedicalReports(); 
                        break;
                case 4: { currentDoctor = null; 
                        return; }
            }
        }
    }
    
    private static void nurseDashboard() {
        while (true) {
            System.out.println("\n=== Nurse Dashboard ===");
            System.out.println("1. Manage Profile");
            System.out.println("2. Logout");
            System.out.print("Select option: ");

            switch (getIntInput("Select option: ", 1, 2)) {
                case 1: manageNurseProfile(); 
                        break;
                case 2: { currentNurse = null; 
                        return; }
            }
        }
    }
    
    private static void printDoctorTable(Doctor doctor) {
        System.out.println("+---------------------+---------------------------------------+");
        System.out.printf("| %-20s | %-35s |%n", "Field", "Current Value");
        System.out.println("+---------------------+---------------------------------------+");
        System.out.printf("| %-20s | %-35s |%n", "Username", doctor.getUsername());
        System.out.printf("| %-20s | %-35s |%n", "Name", doctor.getName());
        System.out.printf("| %-20s | %-35s |%n", "IC", doctor.getIc());
        System.out.printf("| %-20s | %-35s |%n", "Age", doctor.getAge());
        System.out.printf("| %-20s | %-35s |%n", "Gender", doctor.getGender());
        System.out.printf("| %-20s | %-35s |%n", "Phone", doctor.getPhone());
        System.out.printf("| %-20s | %-35s |%n", "Address", doctor.getAddress());
        System.out.printf("| %-20s | %-35s |%n", "Specialty", doctor.getSpecialty());
        System.out.printf("| %-20s | %-35s |%n", "Join Year", doctor.getJoinYear());
        System.out.println("+---------------------+---------------------------------------+");
    }
    
    private static void manageDoctorProfile() {
        while(true) {
            System.out.println("\n-------------------- Manage Doctor Profile --------------------");
            printDoctorTable(currentDoctor);
            System.out.println("1. Change Password");
            System.out.println("2. Update Phone Number");
            System.out.println("3. Update Address");
            System.out.println("4. Update Specialty");
            System.out.println("5. Back");

            switch(getIntInput("Select option: ", 1, 5)) {
                case 1: String newPass = getValidInput("New Password (6 digits): ", Validator::validatePassword);
                        currentDoctor.setPassword(newPass);
                        updateDoctorData();
                        break;
                case 2: String newPhone = getValidInput("New Phone (e.g. 012-3456789): ", Validator::validatePhone);
                        currentDoctor.setPhone(newPhone);
                        updateDoctorData();
                        break;
                case 3: String newAddr = getInput("New Address: ");
                        currentDoctor.setAddress(newAddr);
                        updateDoctorData();
                        break;
                case 4: String newSpec = getValidInput("New Specialty: ", Validator::validateSpecialty);
                        currentDoctor.setSpecialty(newSpec);
                        updateDoctorData();
                        break;
                case 5: return;
            }
        }
    }

    private static void updateDoctorData() {
        List<Doctor> doctors = FileUtil.readFromFile("doctors.dat");
        doctors.removeIf(d -> d.getUsername().equals(currentDoctor.getUsername()));
        doctors.add(currentDoctor);
        FileUtil.saveToFile(doctors, "doctors.dat");
        System.out.println("Profile updated!");
    }

    private static void viewDoctorSchedule() {
        List<Appointment> appointments = FileUtil.readFromFile("appointments.dat");
        System.out.println("\n--- Doctor Schedule ---");

        appointments.stream()
            .filter(a -> 
                a.getAssignedDoctor() != null && 
                a.getAssignedDoctor().equals(currentDoctor.getUsername())
            )
            .forEach(a -> {
                Patient patient = findPatientByIC(a.getPatientIC());
                String patientName = (patient != null) ? patient.getName() : "Unknown";
                System.out.println(
                    "Time: " + DATE_FORMAT.format(a.getAppointmentTime()) + " | Patient Name: " + patientName + " | Patient IC: " + a.getPatientIC() + " | Dept: " + a.getDepartment());
            });

        if (appointments.isEmpty()) {
            System.out.println("No appointments scheduled.");
        }
    }
    
    private static Patient findPatientByIC(String ic) {
        List<Patient> patients = FileUtil.readFromFile("patients.dat");
        return patients.stream()
                .filter(p -> p.getIc().equals(ic))
                .findFirst()
                .orElse(null);
    }
    
    private static void printNurseTable(Nurse nurse) {
        System.out.println("\n+---------------------+---------------------------------------+");
        System.out.printf("| %-20s | %-35s |%n", "Field", "Current Value");
        System.out.println("+---------------------+---------------------------------------+");
        System.out.printf("| %-20s | %-35s |%n", "Username", nurse.getUsername());
        System.out.printf("| %-20s | %-35s |%n", "Name", nurse.getName()); 
        System.out.printf("| %-20s | %-35s |%n", "IC", nurse.getIc());
        System.out.printf("| %-20s | %-35s |%n", "Age", nurse.getAge());
        System.out.printf("| %-20s | %-35s |%n", "Gender", nurse.getGender());
        System.out.printf("| %-20s | %-35s |%n", "Phone", nurse.getPhone());
        System.out.printf("| %-20s | %-35s |%n", "Address", nurse.getAddress());
        System.out.printf("| %-20s | %-35s |%n", "Specialty", nurse.getSpecialty());
        System.out.printf("| %-20s | %-35s |%n", "Join Year", nurse.getJoinYear());
        System.out.println("+---------------------+---------------------------------------+");
    }
    
    private static void manageNurseProfile() {
        while(true) {
            System.out.println("+---------------------+---------------------------------------+");
            System.out.println("\n-------------------- Manage Nurse Profile --------------------");
            printNurseTable(currentNurse);
            System.out.println("1. Change Password");
            System.out.println("2. Update Phone Number");
            System.out.println("3. Update Address");
            System.out.println("4. Update Specialty");
            System.out.println("5. Back");

            switch(getIntInput("Select option: ", 1, 5)) {
                case 1: String newPass = getValidInput("New Password (6 digits): ", Validator::validatePassword);
                        currentNurse.setPassword(newPass);
                        updateNurseData();
                        break;
                case 2: String newPhone = getValidInput("New Phone (e.g. 012-3456789): ", Validator::validatePhone);
                        currentNurse.setPhone(newPhone);
                        updateNurseData();
                        break;
                case 3: String newAddr = getInput("New Address: ");
                        currentNurse.setAddress(newAddr);
                        updateNurseData();
                        break;
                case 4: String newSpec = getValidInput("New Specialty: ", Validator::validateSpecialty);
                        currentNurse.setSpecialty(newSpec);
                        updateNurseData();
                        break;
                case 5: return;
            }
        }
    }

    private static void updateNurseData() {
        List<Nurse> nurses = FileUtil.readFromFile("nurses.dat");
        nurses.removeIf(n -> n.getUsername().equals(currentNurse.getUsername()));
        nurses.add(currentNurse);
        FileUtil.saveToFile(nurses, "nurses.dat");
        System.out.println("Profile updated!");
    }

    private static void manageMedicalReports() {
        while (true) {
            System.out.println("\n=== Manage Medical Reports ===");
            System.out.println("1. Create a New Medical Report");
            System.out.println("2. View Historical Report");
            System.out.println("3. Back");
            System.out.print("Select option: ");

            switch (getIntInput("", 1, 3)) {
                case 1: createMedicalReport();
                        break;
                case 2: viewAllReports();
                        break;
                case 3: return;
            }
        }
    }

    private static void createMedicalReport() {
        System.out.println("\n--- Create a New Medical Report ---");
        System.out.print("Enter Patient IC: ");
        String patientIC = sc.nextLine();

        List<Patient> patients = FileUtil.readFromFile("patients.dat");
        boolean patientExists = patients.stream()
            .anyMatch(p -> p.getIc().equals(patientIC));

        if (!patientExists) {
            System.out.println("Patient not found!");
            return;
        }

        String diagnosis = getValidInput("Diagnosis (10-500 chars): ", 
            s -> s.length() >= 10 && s.length() <= 500);

        MedicalReport report = new MedicalReport(
            patientIC, 
            currentDoctor.getUsername(), 
            diagnosis
        );

        List<MedicalReport> reports = FileUtil.readFromFile("reports.dat");
        reports.add(report);
        FileUtil.saveToFile(reports, "reports.dat");
        System.out.println("\nReport created!\n" + report);
    }

    private static void viewAllReports() {
        List<MedicalReport> reports = FileUtil.readFromFile("reports.dat");
        System.out.println("\n--- Historical Report ---");
        reports.forEach(r -> System.out.println(r + "\n------------"));
    }

    // Administrator Portal
    private static void adminPortal() {
        System.out.print("Admin Username: ");
        String user = sc.nextLine().trim();
        System.out.print("Password: ");
        String pass = sc.nextLine().trim();

        List<Doctor> admins = FileUtil.readFromFile("doctors.dat");

        if (admins == null || admins.isEmpty()) {
            System.out.println("The system is not intialized, please contact technicians!");
            return;
        }

        boolean isAdmin = admins.stream()
            .anyMatch(d -> 
                "ADMN".equalsIgnoreCase(d.getUsername()) &&
                d.getPassword().equals(pass)
            );

        if (isAdmin) {
            adminDashboard();
        } else {
            System.out.println("Administrator authentication failed, Username or password incorrect!");
        }
    }

    private static void adminDashboard() {
        while (true) {
            System.out.println("\n=== Admin Dashboard ===");
            System.out.println("1. Manage Staff");
            System.out.println("2. Add Staff");
            System.out.println("3. Logout");
            System.out.print("Select option: ");

            switch (getIntInput("Select option: ", 1, 3)) {
                case 1: manageStaff(); 
                        break;
                case 2: addStaff(); 
                        break;
                case 3: return;
            }
        }
    }
    
    private static void manageStaff() {
        while (true) {
            System.out.println("\n=== Manage Staff ===");
            System.out.println("1. Edit Doctor");
            System.out.println("2. Edit Nurse");
            System.out.println("3. Delete Staff");
            System.out.println("4. Back");

            switch (getIntInput("Select option: ", 1, 4)) {
                case 1: editDoctor(); 
                        break;
                case 2: editNurse(); 
                        break;
                case 3: deleteStaff(); 
                        break;
                case 4: return;
            }
        }
    }

    private static void editDoctor() {
        System.out.println("\n=== Edit Doctor Information ===");
        String username = getValidInput("Enter Doctor Username: ", Validator::validateUsername);
        List<Doctor> doctors = FileUtil.readFromFile("doctors.dat");

        Optional<Doctor> doctorOpt = doctors.stream()
            .filter(d -> d.getUsername().equals(username))
            .findFirst();

            Doctor doctor = doctorOpt.get();
            System.out.println("\nCurrent Information:\n" + doctor);
            printDoctorTable(doctor);

            while (true) {
            System.out.println("\nSelect field to edit:");
            System.out.println("1. Phone Number");
            System.out.println("2. Address");
            System.out.println("3. Specialty");
            System.out.println("4. Password");
            System.out.println("5. Finish Editing");

            int choice = getIntInput("Choose option (1-5): ", 1, 5);
            switch (choice) {
                case 1: String newPhone = getValidInput("New Phone (e.g. 012-3456789): ", 
                        Validator::validatePhone);
                        doctor.setPhone(newPhone);
                        break;

                case 2: String newAddress = getInput("New Address: ");
                        doctor.setAddress(newAddress);
                        break;

                case 3: String newSpecialty = getValidInput("New Specialty: ", 
                        s -> s.matches("^[\\p{L} ]{3,50}$"));
                        doctor.setSpecialty(newSpecialty);
                        break;

                case 4: String newPassword = getValidInput("New Password (6 digits): ",
                        Validator::validatePassword);
                        doctor.setPassword(newPassword);
                        break;

                case 5: doctors.removeIf(d -> d.getUsername().equals(username));
                        doctors.add(doctor);
                        FileUtil.saveToFile(doctors, "doctors.dat");
                        System.out.println("Doctor information updated successfully!");
                        return;
            }
            System.out.println("\nUpdated Information Preview:");
            printDoctorTable(doctor);
        }
    }
    
    private static void editNurse() {
        System.out.println("\n=== Edit Nurse Information ===");
        String username = getValidInput("Enter Nurse Username: ", Validator::validateUsername);
        List<Nurse> nurses = FileUtil.readFromFile("nurses.dat");

        Optional<Nurse> nurseOpt = nurses.stream()
            .filter(n -> n.getUsername().equals(username))
            .findFirst();

        Nurse nurse = nurseOpt.get();
        System.out.println("\nCurrent Information:");
        printNurseTable(nurse);

        while (true) {
            System.out.println("\nSelect field to edit:");
            System.out.println("1. Phone Number");
            System.out.println("2. Address");
            System.out.println("3. Specialty");
            System.out.println("4. Password");
            System.out.println("5. Finish Editing");

            int choice = getIntInput("Choose option (1-5): ", 1, 5);
            switch (choice) {
                case 1: String newPhone = getValidInput("New Phone (e.g. 012-3456789): ", 
                        Validator::validatePhone);
                        nurse.setPhone(newPhone);
                        break;

                case 2: String newAddress = getInput("New Address: ");
                        nurse.setAddress(newAddress);
                        break;

                case 3: String newSpecialty = getValidInput("New Specialty: ", 
                        s -> s.matches("^[\\p{L} ]{3,50}$"));
                        nurse.setSpecialty(newSpecialty);
                        break;

                case 4: String newPassword = getValidInput("New Password (6 digits): ",
                        Validator::validatePassword);
                        nurse.setPassword(newPassword);
                        break;

                case 5: nurses.removeIf(n -> n.getUsername().equals(username));
                        nurses.add(nurse);
                        FileUtil.saveToFile(nurses, "nurses.dat");
                        System.out.println("Nurse information updated successfully!");
                        return;
            }
            System.out.println("\nUpdated Information Preview:");
            printNurseTable(nurse);
        }
    }

    private static void addStaff() {
        System.out.println("\n--- Add New Staff ---");
        System.out.println("1. Add Doctor");
        System.out.println("2. Add Nurse");
        System.out.print("Select type: ");

        if (getIntInput("Select type: ", 1, 2) == 1) {
            addDoctor();
        } else {
            addNurse();
        }
    }
    
    private static void deleteStaff() {
        System.out.println("\n=== Delete Staff ===");
        System.out.println("1. Delete Doctor");
        System.out.println("2. Delete Nurse");
        int choice = getIntInput("Select type: ", 1, 2);

        String username = getValidInput("Enter Username: ", Validator::validateUsername);

        if(choice == 1) {
            List<Doctor> doctors = FileUtil.readFromFile("doctors.dat");
            boolean removed = doctors.removeIf(d -> d.getUsername().equals(username));
            if(removed) {
                FileUtil.saveToFile(doctors, "doctors.dat");
                System.out.println("Doctor deleted!");
            }
        } else {
            List<Nurse> nurses = FileUtil.readFromFile("nurses.dat");
            boolean removed = nurses.removeIf(n -> n.getUsername().equals(username));
            if (removed) {
                FileUtil.saveToFile(nurses, "nurses.dat");
                System.out.println("Nurse deleted!");
            } else {
                System.out.println("Staff not found!");
            }
        }
    }

    private static void addDoctor() {
        System.out.println("\n--- Add New Doctor ---");
        Doctor doctor = new Doctor();

        doctor.setUsername(getValidInput("Username (4 letters): ", Validator::validateUsername));
        doctor.setPassword(getValidInput("Password (6 digits): ", Validator::validatePassword));
        doctor.setName(getInput("Full Name: "));
        doctor.setIc(getValidInput("IC (e.g. 990101-01-1234): ", Validator::validateIC));
        doctor.setAge(getIntInput("Age: ", 18, 70));
        doctor.setGender(getValidInput("Gender (Male/Female/Other): ", Validator::validateGender));
        doctor.setPhone(getValidInput("Phone (e.g. 012-3456789): ", Validator::validatePhone));
        doctor.setAddress(getInput("Address: "));
        doctor.setSpecialty(getValidInput("Department: ", Validator::validateSpecialty));
        doctor.setJoinYear(getIntInput("Year of Joined: ", 1900, Calendar.getInstance().get(Calendar.YEAR)));
        
        List<Doctor> doctors = FileUtil.readFromFile("doctors.dat");
        doctors.add(doctor);
        FileUtil.saveToFile(doctors, "doctors.dat");
        System.out.println("Doctor added successfully!");
    }
    
    private static void addNurse() {
        System.out.println("\n--- Add New Nurse ---");
        Nurse nurse = new Nurse();

        nurse.setUsername(getValidInput("Username (4 letters): ", Validator::validateUsername));
        nurse.setPassword(getValidInput("Password (6 digits): ", Validator::validatePassword));
        nurse.setName(getInput("Full Name: "));
        nurse.setIc(getValidInput("IC (e.g. 990101-01-1234): ", Validator::validateIC));
        nurse.setAge(getIntInput("Age: ", 18, 70));
        nurse.setGender(getValidInput("Gender (Male/Female/Other): ", Validator::validateGender));
        nurse.setPhone(getValidInput("Phone (e.g. 012-3456789): ", Validator::validatePhone));
        nurse.setAddress(getInput("Address: "));
        nurse.setSpecialty(getValidInput("Department: ", Validator::validateSpecialty));
        nurse.setJoinYear(getIntInput("Year of Joined: ", 1900, Calendar.getInstance().get(Calendar.YEAR)));

        List<Nurse> nurses = FileUtil.readFromFile("nurses.dat");
        nurses.add(nurse);
        FileUtil.saveToFile(nurses, "nurses.dat");
        System.out.println("Nurse added successfully!");
    }

    // Utility Methods
    private static boolean validateDoctorExists(String username) {
        List<Doctor> doctors = FileUtil.readFromFile("doctors.dat");
        return doctors.stream()
            .anyMatch(d -> d.getUsername().equals(username));
    }
    
    private static int getIntInput(String prompt, int min, int max) {
        while (true) {
            try {
                System.out.print(prompt);
                int input = sc.nextInt();
                sc.nextLine();
                if (input >= min && input <= max) return input;
                System.out.println("Input must be between " + min + " and " + max);
            } catch (InputMismatchException e) {
                sc.nextLine();
                System.out.println("Please enter a number.");
            }
        }
    }

    private static String getValidInput(String prompt, Function<String, Boolean> validator) {
        String input;
        do {
            System.out.print(prompt);
            input = sc.nextLine().trim();
            if (validator.apply(input)) {
                return input;
            }
            System.out.println("Invalid input, please try again.");
        } while (true);
    }

    private static Date getDateInput(String prompt) {
        while (true) {
            try {
                System.out.print(prompt);
                Date date = DATE_FORMAT.parse(sc.nextLine());
                if (date.after(new Date())) {
                    return date;
                }
                System.out.println("Appointment time must be in the future.");
            } catch (ParseException e) {
                System.out.println("Invalid date format! Use dd/MM/yyyy HH:mm");
            }
        }
    }
}