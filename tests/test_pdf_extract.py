import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
from pdf_extractor.pdf_extract import make_df, extract_text, main

class TestPDFExtract(unittest.TestCase):

    def test_make_df(self):
        bold_array = ["Keyword1", "Keyword2"]
        text_array = ["Description1", "Description2", "A"]
        df = make_df(bold_array, text_array)
        expected_df = pd.DataFrame({
            "Bold Text": ["Keyword1", "Keyword2"],
            "Description": ["Description1", "Description2"]
        })
        pd.testing.assert_frame_equal(df, expected_df)

    @patch('pdf_extractor.pdf_extract.pdf.open')
    def test_extract_text(self, mock_pdf_open):
        # mock the file and its contents
        mock_file = MagicMock()
        mock_page = MagicMock()
        mock_block = {
            'lines': [
                {'spans': [{'size': 12.75, 'color': -15592942, 'font': 'GuardianTextEgyptian-Bol', 'text': 'Keyword1'}]},
                {'spans': [{'size': 12.75, 'color': -15592942, 'font': 'GuardianTextEgyptian-Reg', 'text': 'Description1'}]}
            ]
        }
        mock_page.get_text.return_value = {"blocks": [mock_block]}
        mock_file.__getitem__.return_value = mock_page
        mock_file.__len__.return_value = 1
        mock_pdf_open.return_value = mock_file

        bold_array, text_array = extract_text('A')
        self.assertEqual(bold_array, ['Keyword1'])
        self.assertEqual(text_array, ['Description1'])

    @patch('pdf_extractor.pdf_extract.extract_text')
    @patch('pdf_extractor.pdf_extract.pd.DataFrame.to_csv')
    @patch('os.path.exists')
    @patch('os.mkdir')
    def test_main_script(self, mock_mkdir, mock_exists, mock_to_csv, mock_extract_text):
        mock_exists.return_value = False
        mock_extract_text.return_value = (['Keyword1'], ['Description1', 'A'])
        main()
        mock_mkdir.assert_called_once_with('csv_formatted')
        self.assertEqual(mock_to_csv.call_count, 26)  # one for each letter

if __name__ == '__main__':
    unittest.main()