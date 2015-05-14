# -*- coding: utf-8 -*-
from mock import patch, MagicMock
import pytest


class TestSettings(object):

    def _patch_cmd_line(self):
        return 'argparse.ArgumentParser.parse_args'

    def _load_settings_by_cmd_line(self, module_name):
        with patch(self._patch_cmd_line()) as mock:
            mock.return_value = MagicMock(settings=module_name)
            from simple_settings.core import _Settings
            return _Settings()

    def _load_settings_by_enviroment(self, module_name):
        with patch('os.environ.get') as mock:
            mock.return_value = module_name
            from simple_settings.core import _Settings
            return _Settings()

    def test_should_load_module_by_cmd_line(self):
        expect_module = 'tests.samples.simple'
        settings = self._load_settings_by_cmd_line(expect_module)

        assert settings._settings_module == expect_module

    def test_should_load_module_by_enviroment(self):
        expect_module = 'tests.samples.complex'
        with patch(self._patch_cmd_line()) as mock:
            mock.return_value = MagicMock(settings='')
            settings = self._load_settings_by_enviroment(expect_module)

        assert settings._settings_module == expect_module

    def test_simple_settings(self):
        settings = self._load_settings_by_cmd_line('tests.samples.simple')

        assert settings.SIMPLE_STRING == u'simple'
        assert settings.SIMPLE_INTEGER == 1

    def test_should_inherit_settings(self):
        settings = self._load_settings_by_cmd_line('tests.samples.simple')

        assert settings.APPLICATION_NAME == u'Simple Settings'

    def test_complex_settings(self):
        settings = self._load_settings_by_cmd_line('tests.samples.complex')

        assert settings.COMPLEX_DICT['complex'] == 'settings'
        assert settings.COMPLEX_DICT['foo'] == 'bar'

    def test_settings_as_dict(self):
        settings = self._load_settings_by_cmd_line('tests.samples.simple')

        settings_dict = settings.as_dict()
        assert settings_dict['SIMPLE_STRING'] == u'simple'
        assert settings_dict['SIMPLE_INTEGER'] == 1

    def test_settings_override_by_enviroment(self):
        def _mock_env_side_effect(k, d=None):
            return u'simple from env' if k == 'SIMPLE_STRING' else d

        with patch('os.environ.get', side_effect=_mock_env_side_effect):
            settings = self._load_settings_by_cmd_line('tests.samples.simple')

        assert settings.SIMPLE_STRING == u'simple from env'

    def test_setting_are_not_configured(self):
        with patch(self._patch_cmd_line()) as mock:
            mock.return_value = MagicMock(settings='')
            with pytest.raises(RuntimeError):
                from simple_settings.core import _Settings
                _Settings()