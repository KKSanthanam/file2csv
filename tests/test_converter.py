import pytest
import sys
from file2csv.Converter import Converter, Encodings

valid_columns = ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10"]
valid_offsets = [5, 12, 3, 2, 13, 7, 10, 13, 20, 13]
testdata = [
    pytest.param('fixedfile.txt', 'csvfile.csv', 'tests/specfile.json',
                 True,  valid_columns,
                 valid_offsets, 'windows-1252', True, 'utf-8',
                 id="valid_spec"),
    pytest.param('fixedfile.txt', 'csvfile.csv', 'tests/incorrect_offset_specfile.json',
                 False,  valid_columns, [], 'windows-1252', True, 'utf-8',
                 id="invalid_offsets"),
    pytest.param('fixedfile.txt', 'csvfile.csv', 'tests/specfile_doesnt_exist.json',
                 False, [], [], 'windows-1252', True, 'utf-8',
                 id="no_spec_file"),
    pytest.param('fixedfile.txt', 'csvfile.csv', None,
                 False, [], [],  'windows-1252', True, 'utf-8',
                 id="none_spec_file"),
    pytest.param('fixedfile.txt', 'csvfile.csv', 'specfile_no_columns.json',
                 False, [], [],  'windows-1252', True, 'utf-8',
                 id="zero_columns_spec_file"),
    pytest.param('fixedfile.txt', 'csvfile.csv', 'specfile_no_offsets.json',
                 False, [], [],  'windows-1252', True, 'utf-8',
                 id="zero_offsets_spec_file"),
]


@pytest.mark.parametrize('fixedfile, csvfile, specfile, expected_result, expected_columns, expected_offsets, expected_in_encoding, expected_header_on, expected_out_encoding', testdata)
class TestConverter():
    def test_spec(self, fixedfile, csvfile, specfile, expected_result, expected_columns, expected_offsets, expected_in_encoding, expected_header_on, expected_out_encoding):
        converter = Converter(fixedfile=fixedfile,
                              csvfile=csvfile, specfile=specfile)
        (result, columns, offsets, fixed_with_encoding,
         included_header, delimited_encoding) = converter.encoder_spec()
        assert result == expected_result
        assert columns == expected_columns
        assert offsets == expected_offsets
        assert fixed_with_encoding == expected_in_encoding
        assert included_header == expected_header_on
        assert delimited_encoding == expected_out_encoding
