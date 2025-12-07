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
import util.FileUtil;

/**
 *
 * @author honor
 */
public class MedicalReport implements Serializable {
    private String reportID;
    private String patientIC;
    private String doctorUsername;
    private String diagnosis;
    private Date reportDate;
    private String treatmentPlan;
    private String medications;
    private String testResults;

    // Empty Constructor
    public MedicalReport() {}

    public MedicalReport(String patientIC, String doctorUsername, String diagnosis) throws IllegalArgumentException {
        if (!Validator.validateIC(patientIC)) {
            throw new IllegalArgumentException("Invalid patient IC");
        }
        if (!Validator.validateUsername(doctorUsername)) {
            throw new IllegalArgumentException("Invalid doctor username");
        }
        
        this.reportID = generateReportID();
        this.patientIC = patientIC;
        this.doctorUsername = doctorUsername;
        this.diagnosis = diagnosis;
        this.reportDate = new Date();
    }

    // Generate a unique report ID（Example：REP-20231025-001）
    private String generateReportID() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMdd");
        String datePart = sdf.format(new Date());

        List<MedicalReport> allReports = FileUtil.readFromFile("reports.dat");
        int sequence = (int) allReports.stream()
            .filter(r -> r.getReportID() != null && r.getReportID().startsWith("REP-" + datePart))
            .count() + 1;

        return String.format("REP-%s-%03d", datePart, sequence);
    }

    public String getReportID() { return reportID; }

    public String getPatientIC() { return patientIC; }

    public String getDoctorUsername() { return doctorUsername; }

    public String getDiagnosis() { return diagnosis; }
    public void setDiagnosis(String diagnosis) {
        this.diagnosis = diagnosis.substring(0, Math.min(diagnosis.length(), 500));
    }

    public Date getReportDate() { return reportDate; }

    public String getTreatmentPlan() { return treatmentPlan; }
    public void setTreatmentPlan(String plan) {
        this.treatmentPlan = plan.substring(0, Math.min(plan.length(), 1000));
    }

    public String getMedications() { return medications; }
    public void setMedications(String meds) {
        this.medications = meds.substring(0, Math.min(meds.length(), 500));
    }

    public String getTestResults() { return testResults; }
    public void setTestResults(String results) {
        this.testResults = results.substring(0, Math.min(results.length(), 1000));
    }

    @Override
    public String toString() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");
        return String.format(
            "Medical Report %s\nDate: %s\nPatient IC: %s\nDoctor: %s\nDiagnosis: %s",
            reportID,
            sdf.format(reportDate),
            patientIC,
            doctorUsername,
            diagnosis
        );
    }
}
