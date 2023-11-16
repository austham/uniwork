INSERT INTO Clients VALUES ('C4', 'Client 4', 'City 4', 'password', 0.0, 0.0, 'Active');
INSERT INTO Clients VALUES ('C5', 'Client 5', 'City 5', 'password', 0.0, 0.0, 'Active');
INSERT INTO Clients VALUES ('C6', 'Client 6', 'City 6', 'password', 0.0, 0.0, 'Active');

INSERT INTO Parts VALUES ('P4', 'Part 4', 'Part 4 Description', 4.00, 400);
INSERT INTO Parts VALUES ('P5', 'Part 5', 'Part 5 Description', 5.00, 500);
INSERT INTO Parts VALUES ('P6', 'Part 6', 'Part 6 Description', 6.00, 600);

INSERT INTO POs VALUES ('PO4', 'C4', '2020-04-04', 'Fulfilled');
INSERT INTO POs VALUES ('PO5', 'C5', '2020-05-05', 'Ordered');
INSERT INTO POs VALUES ('PO6', 'C6', '2020-06-06', 'Ordered');

INSERT INTO Lines VALUES ('PO4', 'P4', '40', 4);
INSERT INTO Lines VALUES ('PO4', 'P5', '50', 5);
INSERT INTO Lines VALUES ('PO5', 'P6', '60', 6);
INSERT INTO Lines VALUES ('PO5', 'P4', '40', 4);
INSERT INTO Lines VALUES ('PO6', 'P5', '50', 5);
INSERT INTO Lines VALUES ('PO6', 'P6', '60', 6);