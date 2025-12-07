#include <iostream>
#include <iomanip>
#include <limits>

using namespace std;

// Global variables to store daily totals
double dailyTotalSales = 0;
int dailyTotalCustomers = 0;

// Define the max number of items
const int max_items = 100;

struct salesData {
    string brand;
    string series;
    string model;
    int totalUnits;
    double totalPrice;
};

// Array to store sales data for each item sold
salesData dailySales[max_items];
int dailySalesCount = 0;

// Arrays to store order details
string codes[max_items];
string models[max_items];
double prices[max_items];

int main() {
    int ms_choice, b_choice, model, quantity, cust_no = 0;
    int bil_order = 0;
    char more_order = 'Y', more_cust = 'Y';
	double subtotal = 0, discount = 0, serviceCharge = 0, tax = 0, total = 0, price;

	// Initialize quantities array
    int quantities[max_items] = {0}; 

    // Constants for pricing
    const double IPS = 5899.99;
    const double IPP = 6899.99;
	const double SFD = 7299.99;
	const double SFP = 4999.00;
	const double STF = 3799.00;
	const double STFU = 5999.00;
	const double SFF = 1999.00;
	const double SWF = 1699.00;
	const double HPS = 2999.00;
	const double HPSP = 3999.00;
	const double HPSU = 6599.00;
	const double HMF = 3699.00;
	const double HMFP = 5299.00;
	const double HNTI = 1299.00;
	const double HNTSE = 1099.00;

    // Main loop to display the main menu after each customer
    do {
        // Display function choice for user
        cout << "FOX ENTERPRISE" << endl;
        cout << "FUNCTION" << endl;
        cout << "1. ORDER ENTRY" << endl;
        cout << "2. DAILY REPORT" << endl;
        cout << "3. EXIT" << endl;
        cout << "Enter your choice: ";
        cin >> ms_choice;
        if (cin.fail()) {
			cin.clear(); // Clears the error flag
			cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Ignores the rest of the line
			cout << "Invalid input. Please enter a number.\n";
			continue; // Skip to the next iteration of the loop
		}
		cout << "You selected: " << ms_choice << endl;
		cout << endl;

        if (ms_choice == 3) {
            cout << "Exiting the system. Thank you!\n";
            break;
        }

        if (ms_choice == 2) {
            // Generate Daily Report
            cout << "Daily Sales Report\n";
            cout << "====================\n";
            cout << "Total Customers: " << dailyTotalCustomers << endl;
            cout << "Total Sales: RM" << dailyTotalSales << endl;

            cout << "\nSales Breakdown:\n";
            cout << left << setw(9) << "Brand" << setw(20) << "Series" << setw(20) << "Model" << right << setw(12) << "Units Sold" << setw(20) << "Total Sales (RM)" << endl;
            cout << left << setw(9) << "-----" << setw(20) << "------" << setw(20) << "-----" << right << setw(12) << "----------" << setw(20) << "---------------" << endl;

            for (int i = 0; i < dailySalesCount; i++) {
                cout << left << setw(9) << dailySales[i].brand << setw(20) << dailySales[i].series << setw(20) << dailySales[i].model << right << setw(12) << dailySales[i].totalUnits << setw(20) << dailySales[i].totalPrice << endl;
            }
            cout << endl;
			
			// Clear the input buffer to handle further inputs correctly
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
            continue; // Go back to main menu after displaying report
        }

        if (ms_choice == 1) {
            // Loop to handle multiple customers
            while (more_cust == 'Y' || more_cust == 'y') {
                subtotal = 0; // Reset for each customer
                total = 0;
                bil_order = 0;
                cust_no++;
                more_order = 'Y';
                dailyTotalCustomers++;

                cout << "\nCustomer " << cust_no << endl;

                // Loop to handle multiple orders
                while (more_order == 'Y' || more_order == 'y') {
					cout << "BRAND" << endl;
					cout << "1. ALL BRAND" << endl;
					cout << "2. APPLE" << endl;
					cout << "3. SAMSUNG" << endl;
					cout << "4. HUAWEI" << endl;
					cout << "Enter your choice: ";
					cin >> b_choice;
					cout << endl;

                    switch (b_choice) {
                        case 1:
							// Display all brand & series phone menu
							cout << "ALL" << endl;
							cout << left << setw(8) << "+------+" << left << setw(9) << "--------+" << left << setw(7) << "------+" << right << setw(12) << "-----------+" << right << setw(27) << "--------------------------+" << setw(15) << "--------------+" << endl;
                            cout << left << setw(8) << "| BIL. |" << left << setw(9) << "| BRAND |" << left << setw(7) << " CODE |" << right << setw(12) << "  SERIES |" << right << setw(27) << "MODEL |" << setw(15) << "PRICE |" << endl;
                            cout << left << setw(8) << "+------+" << left << setw(9) << "--------+" << left << setw(7) << "------+" << right << setw(12) << "-----------+" << right << setw(27) << "--------------------------+" << setw(15) << "--------------+" << endl;
                            cout << left << setw(8) << "|1.    |" << right << setw(9) << "APPLE |" << right << setw(7) << "A01  |" << right << setw(12) << "IPHONE 15 |" << right << setw(27) << "     - 512GB|" << setw(15) << "RM 5899.99 |" << endl;
                            cout << left << setw(8) << "|2.    |" << right << setw(9) << "APPLE |" << right << setw(7) << "A02  |" << right << setw(12) << "IPHONE 15 |" << right << setw(27) << "   PRO 512GB|" << setw(15) << "RM 6899.99 |" << endl;
                            cout << left << setw(8) << "|3.    |" << right << setw(9) << "SAMSUNG |" << right << setw(7) << "SZ1  |" << right << setw(12) << " GALAXY Z |" << right << setw(27) << "       Fold6|" << setw(15) << "RM 7299.00 |" << endl;
							cout << left << setw(8) << "|4.    |" << right << setw(9) << "SAMSUNG |" << right << setw(7) << "SZ2  |" << right << setw(12) << " GALAXY Z |" << right << setw(27) << "       Flip6|" << setw(15) << "RM 4999.00 |" << endl;
							cout << left << setw(8) << "|5.    |" << right << setw(9) << "SAMSUNG |" << right << setw(7) << "SS1  |" << right << setw(12) << " GALAXY S |" << right << setw(27) << "          24|" << setw(15) << "RM 3799.00 |" << endl;
							cout << left << setw(8) << "|6.    |" << right << setw(9) << "SAMSUNG |" << right << setw(7) << "SS2  |" << right << setw(12) << " GALAXY S |" << right << setw(27) << "    24 ULTRA|" << setw(15) << "RM 5999.00 |" << endl;
							cout << left << setw(8) << "|7.    |" << right << setw(9) << "SAMSUNG |" << right << setw(7) << "SA1  |" << right << setw(12) << " GALAXY A |" << right << setw(27) << "          55|" << setw(15) << "RM 1999.00 |" << endl;
							cout << left << setw(8) << "|8.    |" << right << setw(9) << "SAMSUNG |" << right << setw(7) << "SA2  |" << right << setw(12) << " GALAXY A |" << right << setw(27) << "          35|" << setw(15) << "RM 1699.00 |" << endl;
							cout << left << setw(8) << "|9.    |" << right << setw(9) << "HUAWEI |" << right << setw(7) << "HP1  |" << right << setw(12) << "     PURE |" << right << setw(27) << "          70|" << setw(15) << "RM 2999.00 |" << endl;
							cout << left << setw(8) << "|10.   |" << right << setw(9) << "HUAWEI |" << right << setw(7) << "HP2  |" << right << setw(12) << "     PURE |" << right << setw(27) << "      70 PRO|" << setw(15) << "RM 3999.00 |" << endl;
							cout << left << setw(8) << "|11.   |" << right << setw(9) << "HUAWEI |" << right << setw(7) << "HP3  |" << right << setw(12) << "     PURE |" << right << setw(27) << "    70 ULTRA|" << setw(15) << "RM 6599.00 |" << endl;
							cout << left << setw(8) << "|12.   |" << right << setw(9) << "HUAWEI |" << right << setw(7) << "HM1  |" << right << setw(12) << "     MATE |" << right << setw(27) << "          50|" << setw(15) << "RM 3699.00 |" << endl;
							cout << left << setw(8) << "|13.   |" << right << setw(9) << "HUAWEI |" << right << setw(7) << "HM2  |" << right << setw(12) << "     MATE |" << right << setw(27) << "      50 PRO|" << setw(15) << "RM 5299.00 |" << endl;
							cout << left << setw(8) << "|14.   |" << right << setw(9) << "HUAWEI |" << right << setw(7) << "HN1  |" << right << setw(12) << "     NOVA |" << right << setw(27) << "        12 I|" << setw(15) << "RM 1299.00 |" << endl;
							cout << left << setw(8) << "|15.   |" << right << setw(9) << "HUAWEI |" << right << setw(7) << "HN2  |" << right << setw(12) << "     NOVA |" << right << setw(27) << "       12 SE|" << setw(15) << "RM 1099.00 |" << endl;
							cout << left << setw(8) << "+------+" << left << setw(9) << "--------+" << left << setw(7) << "------+" << right << setw(12) << "-----------+" << right << setw(27) << "--------------------------+" << setw(15) << "--------------+" << endl;
							cout << "Enter your choice: ";
                            cin >> model;
                            cout << endl;

                            if (model == 1 || model == 2 || model == 3 || model == 4 || model == 5 || model == 6 || model == 7 || model == 8 || model == 9 || model == 10 || model == 11 || model == 12 || model == 13 || model == 14 || model == 15) {
								string selectedBrand, selectedSeries, selectedModel, code;
								double selectedPrice;

								if (model == 1) {
									selectedBrand = "APPLE";
									selectedSeries = "IPHONE 15";
									selectedModel = "STANDARD 512GB";
									selectedPrice = IPS;
									code = "A01";
								} else if (model == 2) {
									selectedBrand = "APPLE";
									selectedSeries = "IPHONE 15";
									selectedModel = "PRO 512GB";
									selectedPrice = IPP;
									code = "A02";
								} else if (model == 3) {
									selectedBrand = "SAMSUNG";
									selectedSeries = "GALAXY Z";
									selectedModel = "Fold 6";
									selectedPrice = SFD;
									code = "SZ1";
								}else if (model == 4) {
									selectedBrand = "SAMSUNG";
									selectedSeries = "GALAXY Z";
									selectedModel = "Flip 6";
									selectedPrice = SFP;
									code = "SZ2";
								}else if (model == 5) {
									selectedBrand = "SAMSUNG";
									selectedSeries = "GALAXY S";
									selectedModel = "24";
									selectedPrice = STF;
									code = "SS1";
								}else if (model == 6) {
									selectedBrand = "SAMSUNG";
									selectedSeries = "GALAXY S";
									selectedModel = "24 ULTRA";
									selectedPrice = STFU;
									code = "SS2";
								}else if (model == 7) {
									selectedBrand = "SAMSUNG";
									selectedSeries = "GALAXY A";
									selectedModel = "55";
									selectedPrice = SFF;
									code = "SA1";
								}else if (model == 8) {
									selectedBrand = "SAMSUNG";
									selectedSeries = "GALAXY A";
									selectedModel = "35";
									selectedPrice = SWF;
									code = "SA2";
								}else if (model == 9) {
									selectedBrand = "HUAWEI";
									selectedSeries = "PURE";
									selectedModel = "70";
									selectedPrice = HPS;
									code = "HP1";
								}else if (model == 10) {
									selectedBrand = "HUAWEI";
									selectedSeries = "PURE";
									selectedModel = "70  PRO";
									selectedPrice = HPSP;
									code = "HP2";
								}else if (model == 11) {
									selectedBrand = "HUAWEI";
									selectedSeries = "PURE";
									selectedModel = "70 ULTRA";
									selectedPrice = HPSU;
									code = "HP3";
								}else if (model == 12) {
									selectedBrand = "HUAWEI";
									selectedSeries = "MATE";
									selectedModel = "50";
									selectedPrice = HMF;
									code = "HM1";
								}else if (model == 13) {
									selectedBrand = "HUAWEI";
									selectedSeries = "MATE";
									selectedModel = "50 PRO";
									selectedPrice = HMFP;
									code = "HM2";
								}else if (model == 14) {
									selectedBrand = "HUAWEI";
									selectedSeries = "NOVA";
									selectedModel = "12 I";
									selectedPrice = HNTI;
									code = "HN1";
								}else if (model == 15) {
									selectedBrand = "HUAWEI";
									selectedSeries = "NOVA";
									selectedModel = "12 SE";
									selectedPrice = HNTSE;
									code = "HN2";
								}

								cout << left << setw(11) << "+---------+" << right << setw(20) << "-------------------+" << right << setw(20) << "-------------------+" << right << setw(15) << "--------------+" << endl;
                                cout << left << setw(11) << "|  BRAND  |" << right << setw(20) << " SERIES |" << right << setw(20) << " MODEL |" << right << setw(15) << "PRICE |" << endl;
                                cout << left << setw(11) << "+---------+" << right << setw(20) << "-------------------+" << right << setw(20) << "-------------------+" << right << setw(15) << "--------------+" << endl;
                                cout << setw(2) << "| " << left << setw(7) << selectedBrand << " |" << right << setw(18) << selectedSeries << setw(2)  << "|" << right << setw(18) << selectedModel << setw(2)  << " |" << right << setw(9) << " RM " << selectedPrice << setw(2) << " |" << endl;
								cout << left << setw(11) << "+---------+" << right << setw(20) << "-------------------+" << right << setw(20) << "-------------------+" << right << setw(15) << "--------------+" << endl;

								cout << "Quantity: ";
								cin >> quantities[bil_order];
								
								codes[bil_order] = code;
                                models[bil_order] = selectedSeries + " - " + selectedModel;
                                prices[bil_order] = selectedPrice;  // Assuming selectedPrice is set based on the model chosen
								double currentOrderTotal = selectedPrice * quantities[bil_order];

								// Add current order total to subtotal
								subtotal += currentOrderTotal;

                                // Track daily sales details
                                bool found = false;
								for (int i = 0; i < dailySalesCount; i++) {
									if (dailySales[i].brand == selectedBrand && dailySales[i].series == selectedSeries && dailySales[i].model == selectedModel) {
										dailySales[i].totalUnits += quantities[bil_order];
										dailySales[i].totalPrice += currentOrderTotal;
										found = true;
										break;
									}
								}
								if (!found) {
									dailySales[dailySalesCount].brand = selectedBrand;
									dailySales[dailySalesCount].series = selectedSeries;
									dailySales[dailySalesCount].model = selectedModel;
									dailySales[dailySalesCount].totalUnits = quantities[bil_order];
									dailySales[dailySalesCount].totalPrice = currentOrderTotal;
									dailySalesCount++;
								}

								bil_order++;
								
								cout << "Any more order (Y/N)? ";
								cin >> more_order;
								cout << endl;
                            } else {
                                cout << "Invalid model selection." << endl;
                            }
							
                            break;
                        case 2: {
                            // Display Apple menu
                            cout << "APPLE" << endl;
                            cout << left << setw(8) << "+------+" << left << setw(9) << "--------+" << left << setw(7) << "------+" << right << setw(12) << "-----------+" << right << setw(27) << "--------------------------+" << setw(15) << "--------------+" << endl;
                            cout << left << setw(8) << "| BIL. |" << left << setw(9) << "| BRAND |" << left << setw(7) << " CODE |" << right << setw(12) << "  SERIES |" << right << setw(27) << "MODEL |" << setw(15) << "PRICE |" << endl;
                            cout << left << setw(8) << "+------+" << left << setw(9) << "--------+" << left << setw(7) << "------+" << right << setw(12) << "-----------+" << right << setw(27) << "--------------------------+" << setw(15) << "--------------+" << endl;
                            cout << left << setw(8) << "1.     |" << right << setw(9) << "APPLE |" << right << setw(7) << "A01  |" << right << setw(12) << "IPHONE 15 |" << right << setw(27) << "     - 512GB|" << setw(15) << "RM 5899.99 |" << endl;
                            cout << left << setw(8) << "2.     |" << right << setw(9) << "APPLE |" << right << setw(7) << "A02  |" << right << setw(12) << "IPHONE 15 |" << right << setw(27) << "   PRO 512GB|" << setw(15) << "RM 6899.99 |" << endl;
							cout << left << setw(8) << "+------+" << left << setw(9) << "--------+" << left << setw(7) << "------+" << right << setw(12) << "-----------+" << right << setw(27) << "--------------------------+" << setw(15) << "--------------+" << endl;
                            cout << "Enter your choice: ";
                            cin >> model;
                            cout << endl;

                            if (model == 1 || model == 2 || model == 3) {
								string selectedBrand, selectedSeries, selectedModel, code;
								double selectedPrice;

								if (model == 1) {
									selectedBrand = "APPLE";
									selectedSeries = "IPHONE 15";
									selectedModel = "STANDARD 512GB";
									selectedPrice = IPS;
									code = "A01";
								} else if (model == 2) {
									selectedBrand = "APPLE";
									selectedSeries = "IPHONE 15";
									selectedModel = "PRO 512GB";
									selectedPrice = IPP;
									code = "A02";
								}

                                cout << left << setw(11) << "+---------+" << right << setw(20) << "-------------------+" << right << setw(20) << "-------------------+" << right << setw(15) << "--------------+" << endl;
                                cout << left << setw(11) << "|  BRAND  |" << right << setw(20) << " SERIES |" << right << setw(20) << " MODEL |" << right << setw(15) << "PRICE |" << endl;
                                cout << left << setw(11) << "+---------+" << right << setw(20) << "-------------------+" << right << setw(20) << "-------------------+" << right << setw(15) << "--------------+" << endl;
                                cout << setw(2) << "| " << left << setw(7) << selectedBrand << " |" << right << setw(18) << selectedSeries << setw(2)  << "|" << right << setw(18) << selectedModel << setw(2)  << " |" << right << setw(9) << " RM " << selectedPrice << setw(2) << " |" << endl;
								cout << left << setw(11) << "+---------+" << right << setw(20) << "-------------------+" << right << setw(20) << "-------------------+" << right << setw(15) << "--------------+" << endl;

                                cout << "Quantity: ";
                                cin >> quantities[bil_order];
								
								codes[bil_order] = code;
                                models[bil_order] = selectedSeries + " - " + selectedModel;
                                prices[bil_order] = selectedPrice;  // Assuming selectedPrice is set based on the model chosen
								double currentOrderTotal = selectedPrice * quantities[bil_order];

								// Add current order total to subtotal
								subtotal += currentOrderTotal;

                                // Track daily sales details
                                bool found = false;
								for (int i = 0; i < dailySalesCount; i++) {
									if (dailySales[i].brand == selectedBrand && dailySales[i].series == selectedSeries && dailySales[i].model == selectedModel) {
										dailySales[i].totalUnits += quantities[bil_order];
										dailySales[i].totalPrice += currentOrderTotal;
										found = true;
										break;
									}
								}
								if (!found) {
									dailySales[dailySalesCount].brand = selectedBrand;
									dailySales[dailySalesCount].series = selectedSeries;
									dailySales[dailySalesCount].model = selectedModel;
									dailySales[dailySalesCount].totalUnits = quantities[bil_order];
									dailySales[dailySalesCount].totalPrice = currentOrderTotal;
									dailySalesCount++;
								}

								bil_order++;
								
								cout << "Any more order (Y/N)? ";
								cin >> more_order;
								cout << endl;
                            } else {
                                cout << "Invalid model selection." << endl;
                            }
                            break;
                        }
                        case 3: {
							// Display Samsung menu
                            cout << "SAMSUNG" << endl;
							cout << left << setw(8) << "+------+" << left << setw(9) << "--------+" << left << setw(7) << "------+" << right << setw(12) << "-----------+" << right << setw(27) << "--------------------------+" << setw(15) << "--------------+" << endl;
                            cout << left << setw(8) << "| BIL. |" << left << setw(9) << "| BRAND |" << left << setw(7) << " CODE |" << right << setw(12) << "  SERIES |" << right << setw(27) << "MODEL |" << setw(15) << "PRICE |" << endl;
                            cout << left << setw(8) << "+------+" << left << setw(9) << "--------+" << left << setw(7) << "------+" << right << setw(12) << "-----------+" << right << setw(27) << "--------------------------+" << setw(15) << "--------------+" << endl;
                            cout << left << setw(8) << "1.     |" << right << setw(9) << "SAMSUNG |" << right << setw(7) << "SZ1  |" << right << setw(12) << " GALAXY Z |" << right << setw(27) << "       Fold6|" << setw(15) << "RM 7299.00 |" << endl;
							cout << left << setw(8) << "2.     |" << right << setw(9) << "SAMSUNG |" << right << setw(7) << "SZ2  |" << right << setw(12) << " GALAXY Z |" << right << setw(27) << "       Flip6|" << setw(15) << "RM 4999.00 |" << endl;
							cout << left << setw(8) << "3.     |" << right << setw(9) << "SAMSUNG |" << right << setw(7) << "SS1  |" << right << setw(12) << " GALAXY S |" << right << setw(27) << "          24|" << setw(15) << "RM 3799.00 |" << endl;
							cout << left << setw(8) << "4.     |" << right << setw(9) << "SAMSUNG |" << right << setw(7) << "SS2  |" << right << setw(12) << " GALAXY S |" << right << setw(27) << "    24 ULTRA|" << setw(15) << "RM 5999.00 |" << endl;
							cout << left << setw(8) << "5.     |" << right << setw(9) << "SAMSUNG |" << right << setw(7) << "SA1  |" << right << setw(12) << " GALAXY A |" << right << setw(27) << "          55|" << setw(15) << "RM 1999.00 |" << endl;
							cout << left << setw(8) << "6.     |" << right << setw(9) << "SAMSUNG |" << right << setw(7) << "SA2  |" << right << setw(12) << " GALAXY A |" << right << setw(27) << "          35|" << setw(15) << "RM 1699.00 |" << endl;
							cout << left << setw(8) << "+------+" << left << setw(9) << "--------+" << left << setw(7) << "------+" << right << setw(12) << "-----------+" << right << setw(27) << "--------------------------+" << setw(15) << "--------------+" << endl;
                            cout << "Enter your choice: ";
                            cin >> model;
                            cout << endl;

                            if (model == 1 || model == 2 || model == 3 || model == 4 || model == 5 || model == 6) {
								string selectedBrand, selectedSeries, selectedModel, code;
								double selectedPrice;

								if (model == 1) {
									selectedBrand = "SAMSUNG";
									selectedSeries = "GALAXY Z";
									selectedModel = "Fold 6";
									selectedPrice = SFD;
									code = "SZ1";
								} else if (model == 2) {
									selectedBrand = "SAMSUNG";
									selectedSeries = "GALAXY Z";
									selectedModel = "Flip 6";
									selectedPrice = SFP;
									code = "SZ2";
								} else if (model == 3) {
									selectedBrand = "SAMSUNG";
									selectedSeries = "GALAXY S";
									selectedModel = "24";
									selectedPrice = STF;
									code = "SS1";
								}else if (model == 4) {
									selectedBrand = "SAMSUNG";
									selectedSeries = "GALAXY S";
									selectedModel = "24 ULTRA";
									selectedPrice = STFU;
									code = "SS2";
								}else if (model == 5) {
									selectedBrand = "SAMSUNG";
									selectedSeries = "GALAXY A";
									selectedModel = "55";
									selectedPrice = SFF;
									code = "SA1";
								}else if (model == 6) {
									selectedBrand = "SAMSUNG";
									selectedSeries = "GALAXY A";
									selectedModel = "35";
									selectedPrice = SWF;
									code = "SA2";
								}

                                cout << left << setw(11) << "+---------+" << right << setw(20) << "-------------------+" << right << setw(20) << "-------------------+" << right << setw(15) << "--------------+" << endl;
                                cout << left << setw(11) << "|  BRAND  |" << right << setw(20) << " SERIES |" << right << setw(20) << " MODEL |" << right << setw(15) << "PRICE |" << endl;
                                cout << left << setw(11) << "+---------+" << right << setw(20) << "-------------------+" << right << setw(20) << "-------------------+" << right << setw(15) << "--------------+" << endl;
                                cout << setw(2) << "| " << left << setw(7) << selectedBrand << " |" << right << setw(18) << selectedSeries << setw(2)  << "|" << right << setw(18) << selectedModel << setw(2)  << " |" << right << setw(9) << " RM " << selectedPrice << setw(2) << " |" << endl;
								cout << left << setw(11) << "+---------+" << right << setw(20) << "-------------------+" << right << setw(20) << "-------------------+" << right << setw(15) << "--------------+" << endl;

                                cout << "Quantity: ";
                                cin >> quantities[bil_order];
								
								codes[bil_order] = code;
                                models[bil_order] = selectedSeries + " - " + selectedModel;
                                prices[bil_order] = selectedPrice;  // Assuming selectedPrice is set based on the model chosen
								double currentOrderTotal = selectedPrice * quantities[bil_order];

								// Add current order total to subtotal
								subtotal += currentOrderTotal;

                                // Track daily sales details
                                bool found = false;
								for (int i = 0; i < dailySalesCount; i++) {
									if (dailySales[i].brand == selectedBrand && dailySales[i].series == selectedSeries && dailySales[i].model == selectedModel) {
										dailySales[i].totalUnits += quantities[bil_order];
										dailySales[i].totalPrice += currentOrderTotal;
										found = true;
										break;
									}
								}
								if (!found) {
									dailySales[dailySalesCount].brand = selectedBrand;
									dailySales[dailySalesCount].series = selectedSeries;
									dailySales[dailySalesCount].model = selectedModel;
									dailySales[dailySalesCount].totalUnits = quantities[bil_order];
									dailySales[dailySalesCount].totalPrice = currentOrderTotal;
									dailySalesCount++;
								}

								bil_order++;
								
								cout << "Any more order (Y/N)? ";
								cin >> more_order;
								cout << endl;
                            } else {
                                cout << "Invalid model selection." << endl;
                            }
                            break;
                        }
                        case 4: {
                            // Display Huawei menu
                            cout << "HUAWEI" << endl;
                            cout << left << setw(8) << "+------+" << left << setw(9) << "--------+" << left << setw(7) << "------+" << right << setw(12) << "-----------+" << right << setw(27) << "--------------------------+" << setw(15) << "--------------+" << endl;
                            cout << left << setw(8) << "| BIL. |" << left << setw(9) << "| BRAND |" << left << setw(7) << " CODE |" << right << setw(12) << "  SERIES |" << right << setw(27) << "MODEL |" << setw(15) << "PRICE |" << endl;
                            cout << left << setw(8) << "+------+" << left << setw(9) << "--------+" << left << setw(7) << "------+" << right << setw(12) << "-----------+" << right << setw(27) << "--------------------------+" << setw(15) << "--------------+" << endl;
                            cout << left << setw(8) << "|1.    |" << right << setw(9) << "HUAWEI |" << right << setw(7) << "HP1  |" << right << setw(12) << "     PURE |" << right << setw(27) << "          70|" << setw(15) << "RM 2999.00 |" << endl;
							cout << left << setw(8) << "|2.    |" << right << setw(9) << "HUAWEI |" << right << setw(7) << "HP2  |" << right << setw(12) << "     PURE |" << right << setw(27) << "      70 PRO|" << setw(15) << "RM 3999.00 |" << endl;
							cout << left << setw(8) << "|3.    |" << right << setw(9) << "HUAWEI |" << right << setw(7) << "HP3  |" << right << setw(12) << "     PURE |" << right << setw(27) << "    70 ULTRA|" << setw(15) << "RM 6599.00 |" << endl;
							cout << left << setw(8) << "|4.    |" << right << setw(9) << "HUAWEI |" << right << setw(7) << "HM1  |" << right << setw(12) << "     MATE |" << right << setw(27) << "          50|" << setw(15) << "RM 3699.00 |" << endl;
							cout << left << setw(8) << "|5.    |" << right << setw(9) << "HUAWEI |" << right << setw(7) << "HM2  |" << right << setw(12) << "     MATE |" << right << setw(27) << "      50 PRO|" << setw(15) << "RM 5299.00 |" << endl;
							cout << left << setw(8) << "|6.    |" << right << setw(9) << "HUAWEI |" << right << setw(7) << "HN1  |" << right << setw(12) << "     NOVA |" << right << setw(27) << "        12 I|" << setw(15) << "RM 1299.00 |" << endl;
							cout << left << setw(8) << "|6.    |" << right << setw(9) << "HUAWEI |" << right << setw(7) << "HN1  |" << right << setw(12) << "     NOVA |" << right << setw(27) << "       12 SE|" << setw(15) << "RM 1299.00 |" << endl;
							cout << left << setw(8) << "+------+" << left << setw(9) << "--------+" << left << setw(7) << "------+" << right << setw(12) << "-----------+" << right << setw(27) << "--------------------------+" << setw(15) << "--------------+" << endl;
                            cout << "Enter your choice: ";
                            cin >> model;
                            cout << endl;

                            if (model == 1 || model == 2 || model == 3 || model == 4 || model == 5 || model == 6 || model == 7) {
								string selectedBrand, selectedSeries, selectedModel, code;
								double selectedPrice;

								if (model == 1) {
									selectedBrand = "HUAWEI";
									selectedSeries = "PURE";
									selectedModel = "70";
									selectedPrice = HPS;
									code = "HP1";
								} else if (model == 2) {
									selectedBrand = "HUAWEI";
									selectedSeries = "PURE";
									selectedModel = "70 PRO";
									selectedPrice = HPSP;
									code = "HP2";
								} else if (model == 3) {
									selectedBrand = "HUAWEI";
									selectedSeries = "PURE";
									selectedModel = "70 ULTRA";
									selectedPrice = HPSU;
									code = "HP3";
								} else if (model == 4) {
									selectedBrand = "HUAWEI";
									selectedSeries = "MATE";
									selectedModel = "50";
									selectedPrice = HMF;
									code = "HM1";
								}else if (model == 5) {
									selectedBrand = "HUAWEI";
									selectedSeries = "MATE";
									selectedModel = "50 PRO";
									selectedPrice = HMFP;
									code = "HM2";
								}else if (model == 6) {
									selectedBrand = "HUAWEI";
									selectedSeries = "NOVA";
									selectedModel = "12 I";
									selectedPrice = HNTI;
									code = "HN1";
								}else if (model == 7) {
									selectedBrand = "HUAWEI";
									selectedSeries = "NOVA";
									selectedModel = "12 SE";
									selectedPrice = HNTSE;
									code = "HN2";
								}

								cout << left << setw(11) << "+---------+" << right << setw(20) << "-------------------+" << right << setw(20) << "-------------------+" << right << setw(15) << "--------------+" << endl;
                                cout << left << setw(11) << "|  BRAND  |" << right << setw(20) << " SERIES |" << right << setw(20) << " MODEL |" << right << setw(15) << "PRICE |" << endl;
                                cout << left << setw(11) << "+---------+" << right << setw(20) << "-------------------+" << right << setw(20) << "-------------------+" << right << setw(15) << "--------------+" << endl;
                                cout << setw(2) << "| " << left << setw(7) << selectedBrand << " |" << right << setw(18) << selectedSeries << setw(2)  << "|" << right << setw(18) << selectedModel << setw(2)  << " |" << right << setw(9) << " RM " << selectedPrice << setw(2) << " |" << endl;
								cout << left << setw(11) << "+---------+" << right << setw(20) << "-------------------+" << right << setw(20) << "-------------------+" << right << setw(15) << "--------------+" << endl;

                                cout << "Quantity: ";
                                cin >> quantities[bil_order];
								
								codes[bil_order] = code;
                                models[bil_order] = selectedSeries + " - " + selectedModel;
                                prices[bil_order] = selectedPrice;  // Assuming selectedPrice is set based on the model chosen
								double currentOrderTotal = selectedPrice * quantities[bil_order];

								// Add current order total to subtotal
								subtotal += currentOrderTotal;

                                // Track daily sales details
                                bool found = false;
								for (int i = 0; i < dailySalesCount; i++) {
									if (dailySales[i].brand == selectedBrand && dailySales[i].series == selectedSeries && dailySales[i].model == selectedModel) {
										dailySales[i].totalUnits += quantities[bil_order];
										dailySales[i].totalPrice += currentOrderTotal;
										found = true;
										break;
									}
								}
								if (!found) {
									dailySales[dailySalesCount].brand = selectedBrand;
									dailySales[dailySalesCount].series = selectedSeries;
									dailySales[dailySalesCount].model = selectedModel;
									dailySales[dailySalesCount].totalUnits = quantities[bil_order];
									dailySales[dailySalesCount].totalPrice = currentOrderTotal;
									dailySalesCount++;
								}

								bil_order++;
								
								cout << "Any more order (Y/N)? ";
								cin >> more_order;
								cout << endl;
                            } else {
                                cout << "Invalid model selection." << endl;
                            }
                            break;
                        }
                        default:
                            cout << "Invalid brand selection." << endl;
                            break;
                    }
                }

                // Calculate discount, service charge, and tax
                discount = subtotal * 0.10;  // Example discount of 10%
                serviceCharge = subtotal * 0.06;
                tax = subtotal * 0.08;
                total = subtotal - discount + serviceCharge + tax;

                dailyTotalSales += total;

                // Print Invoice
                cout << "\nInvoice:\n";
                cout << "FOX ENTERPRISE\nxxxxxxxxxxxxxxxxx\nTel: 09-12345678\n";
                cout << "--------------------------------------------\n";
                cout << "Code\tModel\t\tQty\tPrice\tTotal\n";
                cout << "--------------------------------------------\n";

                for (int i = 0; i < bil_order; i++) {
                    cout << codes[i] << "\t" << models[i] << "\t\t" << quantities[i] << "\tRM" << prices[i] << "\tRM" << prices[i] * quantities[i] << "\n";
                }

                cout << "--------------------------------------------\n";
                cout << "Subtotal: RM" << subtotal << "\n";
                cout << "Discount: -RM" << discount << "\n";
                cout << "Service Charge: RM" << serviceCharge << "\n";
                cout << "Tax: RM" << tax << "\n";
                cout << "Total: RM" << total << "\n";

                // Payment
                string paymentMethod;
                double paymentAmount;
                cout << "Select payment method (W=e-Wallet, CC=Credit Card, D=Debit Card, C=Cash): ";
                cin >> paymentMethod;
                cout << "Payment amount: RM";
                cin >> paymentAmount;
                
                // Payment amount
                double change = paymentAmount - total;

                if (change < 0) {
                    cout << "Insufficient payment amount. Please enter a valid amount." << endl;
                } else {
                    cout << "Change: RM" << change << "\n";
                    cout << "Payment successful. Thank you!\n";
                }

                // Ask if there's another customer
                cout << "Any more customers (Y/N)? ";
                cin >> more_cust;
				cin.ignore(numeric_limits<streamsize>::max(), '\n');  // Clear the buffer
                cout << endl;
            }
        }

    } while (ms_choice != 3); // Loop back to the main menu unless the user chooses to exit

    return 0;
}

