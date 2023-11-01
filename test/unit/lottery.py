from unittest import TestCase

from cuponazo.application import ticket_checker
from cuponazo.domain import ticket


class Test_CuponazoTicket(TestCase):
    def test_init_valid_ticket_values(self):
        number = "12345"
        serie = "123"

        t = ticket.Cuponazo(number, serie)

        self.assertEqual(t.number, number)
        self.assertEqual(t.serie, serie)

    def test_init_invalid_ticket_values(self):
        test_cases = [
            ["a", "123"],
            ["1", "123"],
            ["qqqqq", "123"],
            ["1234", "123"],
            ["123456", "123"],
            ["12345", "1"],
            ["12345", "a"],
            ["12345", "qwe"],
            ["12345", "1234"],
        ]

        for number, serie in test_cases:
            with self.assertRaises(
                ticket.InvalidFormatError,
                msg=f"Case -> number '{number}', serie '{serie}'",
            ) as cm:
                ticket.Cuponazo(number, serie)

    def test_eq_equal_tickets(self):
        self.assertTrue(
            ticket.Cuponazo("12345", "123") == ticket.Cuponazo("12345", "123")
        )

    def test_eq_different_tickets(self):
        self.assertTrue(
            ticket.Cuponazo("12345", "123") != ticket.Cuponazo("54321", "321")
        )


class Test_TicketChecker(TestCase):
    def test_check_ticket(self):
        test_cases = [
            {
                "case_name": "5 numbers + serie",
                "ticket": ticket.Cuponazo("12345", "321"),
                "expected": 6,
            },
            {
                "case_name": "5 numbers",
                "ticket": ticket.Cuponazo("12345", "000"),
                "expected": 5,
            },
            {
                "case_name": "4 numbers",
                "ticket": ticket.Cuponazo("02345", "000"),
                "expected": 4,
            },
            {
                "case_name": "3 numbers",
                "ticket": ticket.Cuponazo("00345", "000"),
                "expected": 3,
            },
            {
                "case_name": "2 numbers",
                "ticket": ticket.Cuponazo("00045", "000"),
                "expected": 2,
            },
            {
                "case_name": "1 numbers",
                "ticket": ticket.Cuponazo("00005", "000"),
                "expected": 1,
            },
            {
                "case_name": "4 reversed numbers",
                "ticket": ticket.Cuponazo("12340", "000"),
                "expected": 4,
            },
            {
                "case_name": "3 reversed numbers",
                "ticket": ticket.Cuponazo("12300", "000"),
                "expected": 3,
            },
            {
                "case_name": "2 reversed numbers",
                "ticket": ticket.Cuponazo("12000", "000"),
                "expected": 2,
            },
            {
                "case_name": "1 reversed numbers",
                "ticket": ticket.Cuponazo("10000", "000"),
                "expected": 1,
            },
            {
                "case_name": "0 numbers",
                "ticket": ticket.Cuponazo("00000", "000"),
                "expected": 0,
            },
            {
                "case_name": "in case of prize in both ways, return the bigger",
                "ticket": ticket.Cuponazo("10345", "000"),
                "expected": 3,
            },
        ]
        checker = ticket_checker.TicketChecker(result=ticket.Cuponazo("12345", "321"))

        for case in test_cases:
            results = checker.check_ticket(case["ticket"])

            self.assertEqual(
                results,
                case["expected"],
                msg=f"failed at case '{case['case_name']}'",
            )
