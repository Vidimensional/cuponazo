import json
import logging

from unittest import TestCase
from unittest.mock import Mock

from botocore.exceptions import ClientError

from cuponazo.domain import ticket, ticket_repository
from cuponazo.infrastructure.ticket_repository import dynamodb

table_name = "some_table"
ticket_id = "2023-02-11"
ticket_number = "12345"
ticket_serie = "321"
db_item = {
    "Item": {
        "Tickets": json.dumps(
            [
                {
                    "type": "cuponazo",
                    "number": ticket_number,
                    "serie": ticket_serie,
                }
            ]
        ),
        "Id": ticket_id,
    }
}
client_error = ClientError(
    operation_name="mocked.error",
    error_response={"Error": {"Code": "something", "Message": "mocked error"}},
)


class Test_TicketRepository_GetTicketById(TestCase):
    def test_returns_correct_list_of_tickets(self):
        mocked_dyndb = build_mocked_dyndb(get_item_returns=db_item)

        repo = dynamodb.TicketRepository(mocked_dyndb)
        resp = repo.get_tickets_by_id(ticket_id)

        self.assertEqual(resp, [ticket.Cuponazo(ticket_number, ticket_serie)])
        mocked_dyndb.get_item.assert_called_once_with(Key={"Id": ticket_id})
        mocked_dyndb.put_item.assert_not_called()

    def test_specified_ticket_id_does_not_exist(self):
        mocked_dyndb = build_mocked_dyndb(get_item_returns={})

        repo = dynamodb.TicketRepository(mocked_dyndb)
        resp = repo.get_tickets_by_id(ticket_id)

        self.assertEqual(resp, [])
        mocked_dyndb.get_item.assert_called_once_with(Key={"Id": ticket_id})
        mocked_dyndb.put_item.assert_not_called()

    def test_aws_sdk_raises_client_error(self):
        mocked_dyndb = build_mocked_dyndb(get_item_raises=client_error)
        repo = dynamodb.TicketRepository(mocked_dyndb)

        with self.assertRaises(ticket_repository.Error):
            repo.get_tickets_by_id(ticket_id)
        mocked_dyndb.get_item.assert_called_once_with(Key={"Id": ticket_id})
        mocked_dyndb.put_item.assert_not_called()


class Test_TicketRepository_AddTicketToId(TestCase):
    new_ticket_number = "12345"
    new_ticket_serie = "321"

    def test_adds_ticket_without_issues(self):
        mocked_dyndb = build_mocked_dyndb(get_item_returns=db_item)
        repo = dynamodb.TicketRepository(mocked_dyndb)

        repo.add_ticket_to_id(
            ticket_id, ticket.Cuponazo(self.new_ticket_number, self.new_ticket_serie)
        )

        expected_tickets = json.dumps(
            [
                {"number": ticket_number, "serie": ticket_serie},
                {"number": self.new_ticket_number, "serie": self.new_ticket_serie},
            ]
        )
        mocked_dyndb.put_item.assert_called_once_with(
            Item={"Id": ticket_id, "Tickets": expected_tickets}
        )
        mocked_dyndb.get_item.assert_called_once_with(Key={"Id": ticket_id})

    def test_aws_sdk_raises_client_error_when_getting_items(self):
        mocked_dyndb = build_mocked_dyndb(get_item_raises=client_error)
        repo = dynamodb.TicketRepository(mocked_dyndb)

        with self.assertRaises(ticket_repository.Error):
            repo.add_ticket_to_id(
                ticket_id,
                ticket.Cuponazo(self.new_ticket_number, self.new_ticket_serie),
            )
        mocked_dyndb.get_item.assert_called_once_with(Key={"Id": ticket_id})
        mocked_dyndb.put_item.assert_not_called()

    def test_aws_sdk_raises_client_error_when_putting_items(self):
        mocked_dyndb = build_mocked_dyndb(
            get_item_returns=db_item,
            put_item_raises=client_error,
        )

        repo = dynamodb.TicketRepository(mocked_dyndb)

        with self.assertRaises(ticket_repository.Error):
            repo.add_ticket_to_id(
                ticket_id,
                ticket.Cuponazo(self.new_ticket_number, self.new_ticket_serie),
            )
        mocked_dyndb.get_item.assert_called_once_with(Key={"Id": ticket_id})
        mocked_dyndb.put_item.assert_called_once_with(
            Item={
                "Id": ticket_id,
                "Tickets": json.dumps(
                    [
                        {
                            "number": ticket_number,
                            "serie": ticket_serie,
                        },
                        {
                            "number": self.new_ticket_number,
                            "serie": self.new_ticket_serie,
                        },
                    ]
                ),
            }
        )


def build_mocked_dyndb(
    get_item_returns: dict = None,
    get_item_raises: Exception = None,
    put_item_raises: Exception = None,
) -> Mock | dynamodb.DynDBTableWrapper:
    mocked_dyndb = Mock()
    mocked_dyndb.name = table_name

    if get_item_returns is not None and get_item_raises is None:
        mocked_dyndb.get_item = Mock(return_value=get_item_returns)
    elif get_item_returns is None and get_item_raises is not None:
        mocked_dyndb.get_item = Mock(side_effect=get_item_raises)
    else:
        mocked_dyndb.get_item = Mock()

    if put_item_raises is not None:
        mocked_dyndb.put_item = Mock(side_effect=put_item_raises)
    else:
        mocked_dyndb.put_item = Mock()

    return mocked_dyndb
