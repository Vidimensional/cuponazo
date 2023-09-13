from unittest import TestCase

from cuponazo.lottery import CuponazoTicket, InvalidTicketFormatError


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
