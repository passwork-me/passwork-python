#!/usr/bin/env python3
import json

from .api_command import ApiCallStrategy
from .base import PassworkCommand


class RefreshCommandStrategy(ApiCallStrategy):
    """Refresh the access token using the configured refresh token."""

    def execute(self, client, args):
        args.endpoint = "v1/sessions/refresh"
        args.params = json.dumps({"refreshToken": client.refresh_token})
        args.method = "POST"
        args.field = None
        return super().execute(client, args)

    @staticmethod
    def add_command(subparsers):
        params = PassworkCommand.base_params()

        parser = subparsers.add_parser(
            "refresh", help="Refresh access token using the refresh token"
        )
        for key, value in params.items():
            parser.add_argument(key, **value)
