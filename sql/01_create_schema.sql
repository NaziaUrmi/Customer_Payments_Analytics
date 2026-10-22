/*
Phase 2 SQL Server schema.
Run in a dedicated learning database, e.g. CustomerPaymentsAnalytics.
This creates empty tables only; import generated CSV files separately.
*/
IF DB_ID(N'CustomerPaymentsAnalytics') IS NULL
    CREATE DATABASE CustomerPaymentsAnalytics;
GO
USE CustomerPaymentsAnalytics;
GO

IF OBJECT_ID('dbo.Payments', 'U') IS NOT NULL DROP TABLE dbo.Payments;
IF OBJECT_ID('dbo.Invoices', 'U') IS NOT NULL DROP TABLE dbo.Invoices;
IF OBJECT_ID('dbo.Customers', 'U') IS NOT NULL DROP TABLE dbo.Customers;
GO

CREATE TABLE dbo.Customers (
    customer_id VARCHAR(16) NOT NULL PRIMARY KEY,
    customer_name NVARCHAR(100) NOT NULL,
    segment NVARCHAR(40) NULL,
    region NVARCHAR(50) NULL,
    customer_since DATE NULL,
    payment_terms_days INT NULL
);
GO

CREATE TABLE dbo.Invoices (
    invoice_id VARCHAR(16) NOT NULL PRIMARY KEY,
    customer_id VARCHAR(16) NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    invoice_amount DECIMAL(12,2) NOT NULL,
    currency CHAR(3) NOT NULL,
    invoice_category NVARCHAR(50) NULL,
    source_status NVARCHAR(30) NULL,
    CONSTRAINT FK_Invoices_Customers FOREIGN KEY (customer_id) REFERENCES dbo.Customers(customer_id)
);
GO

CREATE TABLE dbo.Payments (
    payment_id VARCHAR(16) NOT NULL PRIMARY KEY,
    invoice_id VARCHAR(16) NOT NULL,
    payment_date DATE NOT NULL,
    payment_amount DECIMAL(12,2) NOT NULL,
    payment_method NVARCHAR(40) NULL,
    CONSTRAINT FK_Payments_Invoices FOREIGN KEY (invoice_id) REFERENCES dbo.Invoices(invoice_id)
);
GO
