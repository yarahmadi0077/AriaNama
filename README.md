# **AriaNama Construction Accounting System**  

## **Professional Accounting Solution for Construction Material Management**  

This **Streamlit-based web application** was custom-developed for **AriaNama Construction Company**, a leading construction firm based in Western Iran specializing in building construction and facade design for commercial buildings, offices, and banks.  

---

## **About AriaNama Company**  
AriaNama is a reputable construction company operating in Western Iran, with expertise in:  
- 🏗️ **Building construction**  
- 🏢 **Facade design and implementation** (for offices, banks, and commercial buildings)  
- 🧱 **High-quality material sourcing** (cement, gypsum, bricks, and other construction materials)  

The company required a **custom accounting solution** to efficiently track material purchases, payments, and financial balances - leading to the development of this specialized system.  

---

## **Core Features**  

✔ **Material-Specific Accounting**  
- Dedicated tracking for cement (regular/white), gypsum, bricks, and other construction materials  
- Custom material type creation ("Other" category)  

✔ **Persian Financial Management**  
- Full **Jalali (Shamsi) calendar** integration  
- RTL (right-to-left) interface in Persian  
- Persian number formatting (e.g., ۱,۰۰۰,۰۰۰)  

✔ **Automated Financial Controls**  
- Real-time calculation of:  
  - Total material costs (quantity × unit price)  
  - Debt/Credit balances  
  - Running totals  
- Visual status indicators (🟥 Debt/🟩 Credit)  

✔ **Advanced Data Management**  
- CSV database with Persian support  
- Filter transactions by:  
  - Date ranges  
  - Material types  
  - Financial status  
- Edit/delete transaction records  

✔ **Comprehensive Reporting**  
- Financial summaries:  
  - Total material costs  
  - Payments  
  - Current balances  

---

## **How to Run the Application**  

### **Prerequisites**  
- Python 3.8+  
- pip package manager  

### **Installation**  
1. Clone the repository:  
   ```bash
   git clone https://github.com/yarahmadi0077/AriaNama.git
   cd accounting/src
   ```

2. Install required packages:  
   ```bash
   pip install streamlit pandas jdatetime
   ```

3. Run the application:  
   ```bash
   streamlit run main.py
   ```

4. Access the app in your browser at:  
   `http://localhost:8501`

### **Usage Instructions**  
1. **Add Transactions**:  
   - Select date (Jalali calendar)  
   - Enter material details (type, quantity, price)  
   - Input payment/balance information  

2. **View/Edit Data**:  
   - Filter transactions using the sidebar  
   - Edit directly in the data table  
   - Click "Save Changes" to update  

3. **Generate Reports**:  
   - View automatic financial summaries  
   - Export data via CSV  

---

## **Technical Details**  
- **Frontend**: Streamlit  
- **Data Handling**: Pandas  
- **Persian Date**: jdatetime  
- **Data Storage**: CSV (compatible with Excel)  

---
