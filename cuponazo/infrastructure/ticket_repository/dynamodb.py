import json
from botocore.exceptions import ClientError

from cuponazo.domain import ticket
from cuponazo.domain import ticket_repository


class DynDBTableWrapper:
    """Wrapper of [boto3 Table Resource](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/index.html)"""

    def __init__(self, dyndb_table) -> None:
        self.table = dyndb_table

    @property
    def name(self) -> str:
        return self.table.name

    def get_item(self, *args, **kwargs) -> dict:
        return self.table.get_item(*args, **kwargs)

    def put_item(self, *args, **kwargs) -> dict:
        return self.table.put_item(*args, **kwargs)


class TicketRepository(ticket_repository.Interface):
    """Repository for the stored Cuponazo tickets played.

    Parameters
    ----------
    `table` (`DynDBTable`)
    """

    def __init__(self, table: DynDBTableWrapper) -> None:
        self.table = table

    def get_tickets_by_id(self, ticket_id: str) -> list[ticket.Cuponazo]:
        try:
            response = self.table.get_item(Key={"Id": ticket_id})
        except ClientError as err:
            raise ticket_repository.Error(
                f"Problem getting tickets for '{ticket_id}' from '{self.table.name}': {err.response['Error']['Code']}: {err.response['Error']['Message']}"
            )

        try:
            db_items = response["Item"]
        except KeyError as err:
            return []
        else:
            return [
                ticket.Cuponazo(t["number"], t["serie"])
                for t in json.loads(db_items["Tickets"])
            ]

    def add_ticket_to_id(self, ticket_id: str, t: ticket.Cuponazo) -> None:
        tickets = self.get_tickets_by_id(ticket_id)
        tickets.append(t)
        serialized_tickets = json.dumps(
            [{"number": t.number, "serie": t.serie} for t in tickets]
        )
        try:
            self.table.put_item(Item={"Id": ticket_id, "Tickets": serialized_tickets})
        except ClientError as err:
            raise ticket_repository.Error(
                f"Problem saving tickets for '{ticket_id}' to '{self.table.name}': {err.response['Error']['Code']}: {err.response['Error']['Message']}"
            )
