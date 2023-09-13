from unittest import TestCase

from cuponazo.lottery import CuponazoTicket, InvalidTicketFormatError, TicketChecker


class Test_CuponazoTicket(TestCase):
    def test_init_valid_ticket_values(self):
        number = "12345"
        serie = "123"

        ticket = CuponazoTicket(number, serie)

        self.assertEqual(ticket.number, number)
        self.assertEqual(ticket.serie, serie)

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
                InvalidTicketFormatError,
                msg=f"Case -> number '{number}', serie '{serie}'",
            ) as cm:
                CuponazoTicket(number, serie)

    def test_eq_equal_tickets(self):
        self.assertTrue(
            CuponazoTicket("12345", "123") == CuponazoTicket("12345", "123")
        )

    def test_eq_different_tickets(self):
        self.assertTrue(
            CuponazoTicket("12345", "123") != CuponazoTicket("54321", "321")
        )


class Test_TicketChecker(TestCase):
    def test_check_ticket(self):
        test_cases = [
            {
                "case_name": "5 numbers + serie",
                "ticket": CuponazoTicket("12345", "321"),
                "expected": 6,
            },
            {
                "case_name": "5 numbers",
                "ticket": CuponazoTicket("12345", "000"),
                "expected": 5,
            },
            {
                "case_name": "4 numbers",
                "ticket": CuponazoTicket("02345", "000"),
                "expected": 4,
            },
            {
                "case_name": "3 numbers",
                "ticket": CuponazoTicket("00345", "000"),
                "expected": 3,
            },
            {
                "case_name": "2 numbers",
                "ticket": CuponazoTicket("00045", "000"),
                "expected": 2,
            },
            {
                "case_name": "1 numbers",
                "ticket": CuponazoTicket("00005", "000"),
                "expected": 1,
            },
            {
                "case_name": "4 reversed numbers",
                "ticket": CuponazoTicket("12340", "000"),
                "expected": 4,
            },
            {
                "case_name": "3 reversed numbers",
                "ticket": CuponazoTicket("12300", "000"),
                "expected": 3,
            },
            {
                "case_name": "2 reversed numbers",
                "ticket": CuponazoTicket("12000", "000"),
                "expected": 2,
            },
            {
                "case_name": "1 reversed numbers",
                "ticket": CuponazoTicket("10000", "000"),
                "expected": 1,
            },
            {
                "case_name": "0 numbers",
                "ticket": CuponazoTicket("00000", "000"),
                "expected": 0,
            },
            {
                "case_name": "in case of prize in both ways, return the bigger",
                "ticket": CuponazoTicket("10345", "000"),
                "expected": 3,
            },
        ]
        checker = TicketChecker(result=CuponazoTicket("12345", "321"))

        for case in test_cases:
            results = checker.check_ticket(case["ticket"])

            self.assertEqual(
                results,
                case["expected"],
                msg=f"failed at case '{case['case_name']}'",
            )
