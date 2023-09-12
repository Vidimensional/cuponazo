import json
from botocore.exceptions import ClientError

from cuponazo.lottery import CuponazoTicket


class TicketRepositoryError(Exception):
    pass


class DynDBTable:
    def __init__(self, dyndb_table) -> None:
        self.table = dyndb_table

    @property
    def name(self) -> str:
        return self.table.name

    def get_item(self, *args, **kwargs) -> dict:
        return self.table.get_item(*args, **kwargs)

    def put_item(self, *args, **kwargs) -> dict:
        return self.table.put_item(*args, **kwargs)


class TicketRepository:
    def __init__(self, table: DynDBTable) -> None:
        self.table = table

    def get_tickets_by_id(self, ticket_id: str) -> list[CuponazoTicket]:
        try:
            response = self.table.get_item(Key={"Id": ticket_id})
        except ClientError as err:
            raise TicketRepositoryError(
                f"Problem getting tickets for '{ticket_id}' from '{self.table.name}': {err.response['Error']['Code']}: {err.response['Error']['Message']}"
            )

        try:
            db_items = response["Item"]
        except KeyError as err:
            return []
        else:
            return [
                CuponazoTicket(ticket["number"], ticket["serie"])
                for ticket in json.loads(db_items["Tickets"])
            ]

    def add_ticket_to_id(self, ticket_id: str, ticket: CuponazoTicket) -> None:
        tickets = self.get_tickets_by_id(ticket_id)
        tickets.append(ticket)
        serialized_tickets = json.dumps(
            [{"number": t.number, "serie": t.serie} for t in tickets]
        )
        try:
            self.table.put_item(Item={"Id": ticket_id, "Tickets": serialized_tickets})
        except ClientError as err:
            raise TicketRepositoryError(
                f"Problem saving tickets for '{ticket_id}' to '{self.table.name}': {err.response['Error']['Code']}: {err.response['Error']['Message']}"
            )
