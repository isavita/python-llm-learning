import unittest
from unittest.mock import patch, MagicMock
from listen import list_directory
from fastapi.responses import JSONResponse
from fastapi import status

class Config:
    workspace_base = "/mock/base/path"

class TestListDirectory(unittest.TestCase):
    
    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_list_directory_success(self, mock_isdir, mock_listdir):
        mock_listdir.return_value = ['file1', 'file2', 'dir1']
        mock_isdir.side_effect = lambda path: path.endswith('dir1')

        result = list_directory(Config, '/test/path')

        expected = ['file1', 'file2', 'dir1/']
        self.assertEqual(result, expected)

    @unittest.skip("reason for skipping")
    @patch('os.listdir', side_effect=FileNotFoundError)
    def test_list_directory_not_found(self, mock_listdir):
        response = list_directory(Config, '/non/existent/path')

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'error': 'Path not found'})

    @unittest.skip("reason for skipping")
    @patch('os.listdir', side_effect=PermissionError)
    def test_list_directory_permission_denied(self, mock_listdir):
        response = list_directory(Config, '/forbidden/path')

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'error': 'Permission denied'})

    @unittest.skip("reason for skipping")
    @patch('os.listdir', side_effect=Exception('Unexpected error'))
    def test_list_directory_internal_error(self, mock_listdir):
        response = list_directory(Config, '/some/path')

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {'error': 'Internal server error'})

if __name__ == '__main__':
    unittest.main()
