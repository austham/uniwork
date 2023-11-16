DROP TABLE IF EXISTS Clients;
CREATE TABLE Clients (
    clientId TEXT PRIMARY KEY NOT NULL,
    clientName TEXT NOT NULL,
    clientCity TEXT NOT NULL,
    clientCompPassword TEXT NOT NULL,
    dollarsOnOrder DECIMAL(10,2) NOT NULL,
    moneyOwed DECIMAL(10,2) NOT NULL,
    clientStatus TEXT NOT NULL
);

DROP TABLE IF EXISTS Parts;
CREATE TABLE Parts (
    partNo TEXT PRIMARY KEY NOT NULL,
    partName TEXT NOT NULL,
    partDescription TEXT NOT NULL,
    currentPrice DECIMAL(10,2) NOT NULL,
    QoH INTEGER DEFAULT 0
);

DROP TABLE IF EXISTS POs;
CREATE TABLE POs (
    poNo TEXT PRIMARY KEY NOT NULL,
    clientId TEXT NOT NULL,
    dateOfPO TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (clientId) REFERENCES Clients(clientId)
);


DROP TABLE IF EXISTS Lines;
CREATE TABLE Lines (
    poNo TEXT NOT NULL,
    partNo TEXT NOT NULL,
    qty INTEGER NOT NULL,
    priceOrdered DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (poNo, partNo),
    FOREIGN KEY (poNo) REFERENCES POs(poNo),
    FOREIGN KEY (partNo) REFERENCES Parts(partNo)
);

DROP TRIGGER IF EXISTS update_moneyOwed;
CREATE TRIGGER update_moneyOwed
    AFTER INSERT ON Lines
    BEGIN
        UPDATE Clients
        SET moneyOwed = moneyOwed + (NEW.qty * (SELECT currentPrice FROM Parts WHERE NEW.partNo = partNo))
        WHERE clientId = (SELECT clientId FROM POs WHERE poNo = NEW.poNo);
    END;