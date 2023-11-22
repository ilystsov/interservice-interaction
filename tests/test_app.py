from unittest.mock import MagicMock
from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pydantic import ValidationError, BaseModel

import clients
from server.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    'mocked_response_data, expected',
    [
        (b'{"in_list":false}', {"created": True}),
        (b'{"in_list":true}', {"created": False}),
    ],
)
def test_create_user(
    mocker: Any, mocked_response_data: bytes, expected: dict[str, bool]
) -> None:
    mocked_response = MagicMock()
    mocked_response.status = status.HTTP_200_OK
    mocked_response.data = mocked_response_data
    mocked_response.getheader = lambda _: 'application/json'
    mocker.patch(
        'clients.black_list.api_client.ApiClient.request',
        return_value=mocked_response,
    )

    mocker.patch('server.main.SessionLocal', MagicMock())
    mocker.patch('db.users.UsersRepo', MagicMock())

    response = client.post("/users", json={'name': 'Name Surname'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected


@pytest.mark.parametrize(
    'exception, reason',
    [
        (clients.black_list.exceptions.BadRequestException, 'Bad request'),
        (ValidationError(model=BaseModel, errors=[]), 'Validation error'),
    ],
)
def test_create_user_blacklist_error(
    mocker: Any, exception: Exception, reason: str
) -> None:
    mocker.patch(
        'server.main.api.is_in_list_check_post', side_effect=exception
    )
    response = client.post("/users", json={'name': 'Name Surname'})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == f'Black list error occurred: {reason}'
