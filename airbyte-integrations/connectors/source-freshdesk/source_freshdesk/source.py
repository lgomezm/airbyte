#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

import logging
import requests
from typing import Any, List, Mapping, Optional, Tuple
from requests.auth import AuthBase, HTTPBasicAuth

from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from source_freshdesk.streams import Agents, Companies, Contacts, Conversations, Groups, Roles, SatisfactionRatings, Skills, Tickets, TimeEntries


class SourceFreshdesk(AbstractSource):

    def _create_authenticator(self, api_key: str) -> AuthBase:
        return HTTPBasicAuth(username=api_key, password="unused_with_api_key")

    def check_connection(self, logger: logging.Logger, config: Mapping[str, Any]) -> Tuple[bool, Optional[Any]]:
        alive = True
        error_msg = None
        try:
            url = f"https://{config['domain'].rstrip('/')}/api/v2/settings/helpdesk"
            r = requests.get(url=url, auth=self._create_authenticator(config["api_key"]))
            if not r.ok:
                alive = False
                try:
                    body = r.json()
                    error_msg = f"{body.get('code')}: {body['message']}"
                except ValueError:
                    error_msg = "Invalid credentials"
        except Exception as error:
            alive = False
            error_msg = repr(error)

        return alive, error_msg
    
    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        authenticator = self._create_authenticator(config["api_key"])
        return [
            Agents(authenticator=authenticator, config=config),
            Companies(authenticator=authenticator, config=config),
            Contacts(authenticator=authenticator, config=config),
            Conversations(authenticator=authenticator, config=config),
            Groups(authenticator=authenticator, config=config),
            Roles(authenticator=authenticator, config=config),
            Skills(authenticator=authenticator, config=config),
            TimeEntries(authenticator=authenticator, config=config),
            Tickets(authenticator=authenticator, config=config),
            SatisfactionRatings(authenticator=authenticator, config=config)
        ]
