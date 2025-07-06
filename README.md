# 🔍 NetProbe

**NetProbe** is a modern, cross-platform **network scanning and monitoring tool** built with a beautiful and responsive graphical interface using Python and Ruby. Designed to provide detailed information about devices connected to your local network, NetProbe is perfect for cybersecurity professionals, penetration testers, IT administrators, and curious power users.

---

## 📌 Overview

NetProbe performs real-time scanning of devices within your LAN (Local Area Network), gathers key metadata such as:

- **Device Type** (Router, Hotspot, Bluetooth)
- **IP Address**
- **MAC Address**
- **Open Ports**
- **Protocol**
- **IPv4 / IPv6**
- **Location** (future geolocation module planned)

All results are displayed in a modern GUI and can be saved in structured `.json` files for analysis or reporting.

---

## 🚀 Features

✅ Modern GUI built with `CustomTkinter`  
✅ Real-time network device scanning  
✅ Automated IP ping & MAC address resolution  
✅ Dynamic color-coded device list  
✅ JSON export of scan results  
✅ Multi-threaded scanning with GUI responsiveness  
✅ Dark mode themed interface  
✅ Cross-platform: **Windows, macOS, Linux**

---

## ⚙️ Technologies Used

| Layer              | Technology               |
|-------------------|--------------------------|
| **Frontend GUI**   | Python + CustomTkinter   |
| **Backend Scanner**| Ruby (ARP & ping logic)  |
| **Styling**        | Treeview (Themed via `ttk`) |
| **Data Export**    | Python `json` module     |
| **Multithreading** | Python `threading`       |

---

## 🧠 How It Works

1. **Python GUI** launches with a clean interface.
2. Clicking the **"Scan Network"** button executes a **Ruby script**:
   - It detects the subnet (e.g. `192.168.1.*`)
   - Pings each IP from `.1` to `.254`
   - For alive hosts, retrieves their MAC address
3. The result is returned to Python as CSV
4. Python parses, displays, and color-tags the results
5. Optional: Save the scan to `.json` with one click

---

## 📁 Project Structure
🐱‍👤 NyxVaultX by NetProbe

