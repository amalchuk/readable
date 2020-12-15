from errno import errorcode
from http.client import HTTPConnection
from json.decoder import JSONDecoder
from pprint import PrettyPrinter
from typing import Any, Dict

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management.base import CommandParser


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-p", "--port",
            default=9000,
            type=int,
            help="uWSGI status location.")

    def execute(self, *args: Any, **kwargs: Any) -> None:
        data: Dict[str, Any] = self.build_report(kwargs["port"])
        self.process_uwsgi_stats(data)

    def build_report(self, port: int) -> Dict[str, Any]:
        try:
            connection = HTTPConnection("127.0.0.1", port)
            connection.request("GET", "/")
            response: bytes = connection.getresponse().read()
            connection.close()

            decoder = JSONDecoder()
            return decoder.decode(response.decode("utf-8"))

        except OSError as error:
            raise CommandError(f"[{errorcode[error.errno]}] {error.strerror}") from error

        except Exception as exception:
            raise CommandError(f"[{exception.__class__.__name__}] {exception!s}") from exception

    def process_uwsgi_stats(self, data: Dict[str, Any]) -> None:
        printer = PrettyPrinter(indent=2)
        printer.pprint(data)
