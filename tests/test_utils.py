# -*- coding: utf-8 -*-
import sys

from mock import patch
import pytest

from simple_settings import settings
from simple_settings.utils import settings_stub


class TestSettingsUtils(object):

    @pytest.yield_fixture
    def current_settings(self):
        with patch.object(
            sys, 'argv', ['', '--settings=tests.samples.simple']
        ):
            settings.setup()
        yield settings
        self._clean_simple_settings()

    def _clean_simple_settings(self):
        settings._initialized = False
        settings._dict = {}
        settings._settings_list = []

    def test_stub_settings_with_context_manager(self, current_settings):
        with settings_stub(SIMPLE_STRING='stubed'):
            assert current_settings.SIMPLE_STRING == 'stubed'

        assert current_settings.SIMPLE_STRING == 'simple'

    def test_stub_settings_with_decorator(self, current_settings):
        @settings_stub(SIMPLE_STRING='stubed')
        def get_simple_string_from_setting():
            return current_settings.SIMPLE_STRING

        assert get_simple_string_from_setting() == 'stubed'
        assert current_settings.SIMPLE_STRING == 'simple'

    def test_stub_settings_should_raise_value_error_from_a_wrong_settings(
        self, current_settings
    ):
        with pytest.raises(ValueError) as exc:
            with settings_stub(WRONG_SETTING='ops'):
                pass

        assert 'WRONG_SETTING' in str(exc)

    def test_stub_settings_should_setup_lazy_settings_object(self):
        with patch.object(
            sys, 'argv', ['', '--settings=tests.samples.simple']
        ):
            with settings_stub(SIMPLE_STRING='stubed'):
                assert settings.SIMPLE_STRING == 'stubed'

        assert settings.SIMPLE_STRING == 'simple'
        self._clean_simple_settings()
