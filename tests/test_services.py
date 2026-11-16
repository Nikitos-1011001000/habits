from unittest.mock import patch

from django.test import TestCase

from habbits_tracker.services import send_telegram_message


class TelegramServiceTests(TestCase):
    @patch("habbits_tracker.services.requests.post")
    def test_send_message(self, mock_post):
        mock_post.return_value.raise_for_status.return_value = None

        send_telegram_message("123456789", "Проверка")

        mock_post.assert_called_once()
