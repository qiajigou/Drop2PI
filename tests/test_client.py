# -*- coding: utf-8 -*-

from tests import TestBase
from mock import patch

from d2pi.client import Client
from d2pi.cache import d2_files_list

# when upload
# file name is local file path
# as_file_name is file path in dropbox
file_name = '/watch_dir/test'
as_file_name = '/test'

# when download and delete
# file path is path in dropbox
# save_to_path is download local file path
file_path = as_file_name
save_to_path = file_name


class ClientTest(TestBase):

    @patch('d2pi.client.Client._download')
    def test_client_download(self, _mock_func):
        self.assertFalse(d2_files_list)
        _mock_func.return_value = True
        r = Client.download(file_path, save_to_path)
        self.assertTrue(r)
        self.assertTrue(d2_files_list)
        self.assertTrue(d2_files_list.has_value(save_to_path))
        r = Client.download(file_path, save_to_path)
        self.assertFalse(r)

    @patch('d2pi.client.Client._upload')
    @patch('d2pi.client.Client._download')
    def test_client_upload(self, _mock_func_download, _move_func_upload):
        self.assertFalse(d2_files_list)
        _mock_func_download.return_value = True
        _move_func_upload.return_value = True
        r = Client.download(file_path, save_to_path)
        self.assertTrue(r)
        self.assertTrue(d2_files_list.has_value(save_to_path))

        r = Client.upload(file_name, as_file_name)
        self.assertTrue(r)
        self.assertFalse(d2_files_list.has_value(save_to_path))

    @patch('d2pi.client.Client._delete')
    @patch('d2pi.client.Client._download')
    def test_client_delete(self, _mock_func_download, _move_func_delete):
        self.assertFalse(d2_files_list)
        _mock_func_download.return_value = True
        _move_func_delete.return_value = True
        r = Client.download(file_path, save_to_path)
        self.assertTrue(r)
        self.assertTrue(d2_files_list.has_value(save_to_path))

        r = Client.delete(file_name, as_file_name)
        self.assertTrue(r)
        self.assertFalse(d2_files_list.has_value(save_to_path))

    @patch('d2pi.client.Client._delete')
    @patch('d2pi.client.Client._download')
    def test_client_delete_dir(self, _mock_func_download, _move_func_delete):
        self.assertFalse(d2_files_list)
        _mock_func_download.return_value = True
        _move_func_delete.return_value = True
        r = Client.download(file_path, save_to_path)
        self.assertTrue(r)
        self.assertTrue(d2_files_list.has_value(save_to_path))

        r = Client.download(file_path, save_to_path + '/file1')
        self.assertTrue(r)
        self.assertTrue(d2_files_list.has_value(save_to_path + '/file1'))

        r = Client.delete(file_name, as_file_name)

        self.assertTrue(r)
        self.assertFalse(d2_files_list.has_value(save_to_path))
        self.assertFalse(d2_files_list)

    @patch('d2pi.client.Client._move')
    @patch('d2pi.client.Client._download')
    def test_client_move_dir(self, _mock_func_download, _move_func_move):
        self.assertFalse(d2_files_list)
        _mock_func_download.return_value = True
        _move_func_move.return_value = True

        r = Client.download(file_path, save_to_path)
        self.assertTrue(r)
        self.assertTrue(d2_files_list.has_value(save_to_path))

        r = Client.download(file_path, save_to_path + '/file1')
        self.assertTrue(r)
        self.assertTrue(d2_files_list.has_value(save_to_path + '/file1'))

        r = Client.move(file_name, file_name, as_file_name)
        self.assertTrue(r)
        self.assertFalse(d2_files_list.has_value(save_to_path))

        self.assertFalse(d2_files_list.has_value(save_to_path))
        self.assertFalse(d2_files_list)
