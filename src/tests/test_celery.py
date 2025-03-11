"""
Módulo de testes para as tarefas assíncronas do Celery
"""

from unittest.mock import patch

import pytest
import requests

from src.celery_worker import fetch_data


def test_fetch_data_success(mock_url_and_headers):
    """
    Testa o caso de sucesso da função fetch_data.
    """

    expected_response = {
        'userId': 1,
        'id': 1,
        'title': 'delectus aut autem',
        'completed': False,
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected_response

        response = fetch_data(mock_url_and_headers['url'], mock_url_and_headers['headers'])

        assert response == expected_response
        mock_get.assert_called_once_with(
            mock_url_and_headers['url'],
            headers=mock_url_and_headers['headers'],
            timeout=5,
        )


def test_fetch_data_timeout(mock_url_and_headers):
    """
    Testa o tratamento de timeout na função fetch_data.
    """
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout

        with pytest.raises(Exception, match='Timeout ao acessar API externa'):
            fetch_data(mock_url_and_headers['url'], mock_url_and_headers['headers'])


def test_fetch_data_unauthorized(mock_url_and_invalid_headers):
    """
    Testa o tratamento de erro 401 (não autorizado) na função fetch_data.
    """
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 401

        with pytest.raises(Exception, match='Falha na autenticação, verifique suas credenciais'):
            fetch_data(
                mock_url_and_invalid_headers['url'],
                mock_url_and_invalid_headers['headers'],
            )


def test_fetch_data_http_error(mock_url_and_invalid_headers):
    """
    Testa o tratamento de outros erros HTTP na função fetch_data.
    """
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.HTTPError('Erro HTTP genérico')
        with pytest.raises(requests.exceptions.HTTPError, match='Erro HTTP genérico'):
            fetch_data(
                mock_url_and_invalid_headers['url'],
                mock_url_and_invalid_headers['headers'],
            )
