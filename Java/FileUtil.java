/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package util;
import java.io.*;
import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author honor
 */
public class FileUtil {
    // General file saving method
    public static <T> void saveToFile(List<T> list, String filename) {
        ensureDataDirectoryExists();
        File file = new File("data/" + filename);

        try {
            if (!file.exists()) {
                file.createNewFile();
            }

            try (ObjectOutputStream oos = new ObjectOutputStream(
                new FileOutputStream(file))) {
                oos.writeObject(list);
            }
        } catch (IOException e) {
            System.err.println("Error saving data: " + e.getMessage());
        }
    }

    // General file reading method
    @SuppressWarnings("unchecked")
        public static <T> List<T> readFromFile(String filename) {
        File file = new File("data/" + filename);
        if (!file.exists() || file.length() == 0) {
            return new ArrayList<>();
        }
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(file))) {
            return (List<T>) ois.readObject();
        } catch (Exception e) {
            System.err.println("Error reading " + filename + ": " + e.getMessage());
            return new ArrayList<>();
        }
    }

    // Make sure the data directory exists
    public static void ensureDataDirectoryExists() {
        File dataDir = new File("data");
        if (!dataDir.exists()) {
            dataDir.mkdir();
        }
    }

    // Special method: append a single object to a file
    public static <T> void appendToFile(T object, String filename) {
        List<T> existingData = readFromFile(filename);
        existingData.add(object);
        updateInFile(existingData, filename);
    }

    // Special method: update object
    public static <T> void updateInFile(List<T> list, String filename) {
        saveToFile(list, filename);
    }
}
