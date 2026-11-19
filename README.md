
# WaitLess Print
### Online Printing and Queue Management System

## About the Project
WaitLess Print is an online printing and queue management system designed to reduce waiting time at printing shops.

Students can select a printing shop, upload documents, choose printing preferences and receive a token number. Shop administrators can manage printing orders and update their status.

## Problem Statement
Students often face:
- Long waiting queues at printing shops.
- Manual document submission.
- No proper queue management system.
- No updates about order status.
- Wastage of time during busy hours.

## Objectives
- Reduce waiting time at printing shops.
- Provide online document submission.
- Manage printing orders efficiently.
- Generate token numbers for orders.
- Provide order status tracking.

## Main Features
1. Student Registration and Login
2. Printing Shop Selection
3. Document Upload
4. Print Options Selection
5. Cost Estimation
6. Order Summary
7. Token Generation
8. Order Tracking
9. Admin Dashboard
10. Queue Management Interface

## Technology Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Database: SQLite (planned / backend integration)
- Code Editor: Visual Studio Code

## Project Structure
```text
WaitLess-Print/
│
├── app.py
├── README.md
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── shops.html
│   ├── upload.html
│   ├── print_options.html
│   ├── order_summary.html
│   ├── token.html
│   ├── track_order.html
│   └── admin_dashboard.html
│
└── static/
    ├── style.css
    └── script.js
```

## How to Run the Project

1. Install Python.
2. Install Flask:

```bash
pip install flask
```

3. Open the project folder in VS Code.
4. Run the application:

```bash
python app.py
```

5. Open your browser:

```text
http://127.0.0.1:5000/
```

## Future Scope
- Complete database integration.
- Real-time queue updates.
- Online payment facility.
- Email and SMS notifications.
- QR code based order collection.
- Priority printing option.

## Project Team
Developed as a college mini project by:
- Sakshi Chavan
- Apurva

## Conclusion
WaitLess Print aims to make the printing process faster, easier and more organized through an online platform.
