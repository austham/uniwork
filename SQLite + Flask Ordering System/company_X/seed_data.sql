INSERT INTO Clients VALUES ('C1', 'Client 1', 'City 1', 'password', 0.0, 0.0, 'Active');
INSERT INTO Clients VALUES ('C2', 'Client 2', 'City 2', 'password', 0.0, 0.0, 'Active');
INSERT INTO Clients VALUES ('C3', 'Client 3', 'City 3', 'password', 0.0, 0.0, 'Active');

INSERT INTO Parts VALUES ('P1', 'Part 1', 'Part 1 Description', 1.00, 100);
INSERT INTO Parts VALUES ('P2', 'Part 2', 'Part 2 Description', 2.00, 200);
INSERT INTO Parts VALUES ('P3', 'Part 3', 'Part 3 Description', 3.00, 300);

INSERT INTO POs VALUES ('PO1', 'C1', '2020-01-01', 'Fulfilled');
INSERT INTO POs VALUES ('PO2', 'C2', '2020-02-02', 'Ordered');
INSERT INTO POs VALUES ('PO3', 'C3', '2020-03-03', 'Ordered');

INSERT INTO Lines VALUES ('PO1', 'P1', '10', 1);
INSERT INTO Lines VALUES ('PO1', 'P2', '20', 2);
INSERT INTO Lines VALUES ('PO2', 'P3', '30', 3);
INSERT INTO Lines VALUES ('PO2', 'P1', '10', 1);
INSERT INTO Lines VALUES ('PO3', 'P2', '20', 2);
INSERT INTO Lines VALUES ('PO3', 'P3', '30', 3);