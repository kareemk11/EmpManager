-- Drop old tables if they exist
DROP TABLE IF EXISTS api_log;
DROP TABLE IF EXISTS salaries;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    national_number TEXT NOT NULL UNIQUE,
    email TEXT,
    phone TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1
);

-- Create salaries table
CREATE TABLE salaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    salary REAL NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create api_log table (SQLite doesn’t have JSONB or timezone-aware timestamp)
CREATE TABLE api_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    level TEXT,
    message TEXT,
    extra TEXT
);

-- Sample Users
INSERT INTO users (id, username, national_number, email, phone, is_active) VALUES
(1, 'jdoe', 'NAT1001', 'jdoe@example.com', '0791111111', 1),
(2, 'asalem', 'NAT1002', 'asalem@example.com', '0792222222', 1),
(3, 'rhamdan', 'NAT1003', 'rhamdan@example.com', '0793333333', 0),
(4, 'lbarakat', 'NAT1004', 'lbarakat@example.com', '0794444444', 1),
(5, 'mfaris', 'NAT1005', 'mfaris@example.com', '0795555555', 1),
(6, 'nsaleh', 'NAT1006', 'nsaleh@example.com', '0796666666', 0),
(7, 'zobeidat', 'NAT1007', 'zobeidat@example.com', '0797777777', 1),
(8, 'ahalaseh', 'NAT1008', 'ahalaseh@example.com', '0798888888', 1),
(9, 'tkhalaf', 'NAT1009', 'tkhalaf@example.com', '0799999999', 0),
(10, 'sshaheen', 'NAT1010', 'sshaheen@example.com', '0781010101', 1),
(11, 'tmart', 'NAT1011', 'tmart@example.com', '0781099101', 0),
(12, 'aali', 'NAT1012', 'aali@example.com', '0781088101', 1);

-- Sample Salaries
INSERT INTO salaries (id, year, month, salary, user_id) VALUES
(1,2025,1,1200,1),
(2,2025,2,1300,1),
(3,2025,3,1400,1),
(4,2025,5,1500,1),
(5,2025,6,1600,1),
(6,2025,1,900,2),
(7,2025,2,950,2),
(8,2025,3,980,2),
(9,2025,4,1100,2),
(10,2025,5,1150,2),
(11,2025,1,400,3),
(15,2025,5,800,3),
(16,2025,1,2000,4),
(17,2025,2,2050,4),
(18,2025,3,2100,4),
(19,2025,4,2200,4),
(20,2025,5,2300,4),
(21,2025,1,600,5),
(22,2025,2,700,5),
(23,2025,3,750,5),
(25,2025,5,850,5),
(26,2025,11,1500,6),
(27,2025,12,1550,6),
(28,2025,1,1600,6),
(29,2025,2,1650,6),
(30,2025,3,1700,6),
(31,2025,1,1000,7),
(32,2025,2,1100,7),
(33,2025,3,1150,7),
(34,2025,4,1200,7),
(35,2025,5,1250,7),
(36,2025,6,1350,7),
(37,2025,7,1500,7),
(38,2025,10,2200,8),
(39,2025,11,2300,8),
(40,2025,12,2400,8),
(41,2025,1,2500,8),
(42,2025,2,2600,8),
(43,2025,3,2800,8),
(44,2025,1,1700,9),
(45,2025,2,1750,9),
(46,2025,6,1800,9),
(47,2025,7,1850,9),
(48,2025,8,1900,9),
(49,2025,1,800,10),
(50,2025,2,850,10),
(51,2025,3,900,10),
(52,2025,8,950,10),
(53,2025,9,1000,10),
(54,2025,10,1200,10);
