import pytest
import base64
import unittest
from file2csv.Converter import Converter, Encodings

valid_columns = ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10"]
valid_offsets = [5, 12, 3, 2, 13, 7, 10, 13, 20, 13]
spec_testdata = [
    pytest.param('tests/specfile.json',
                 True,  valid_columns,
                 valid_offsets, Encodings(
                     'windows-1252'), True, Encodings('utf-8'),
                 id="valid_spec"),
    pytest.param('tests/incorrect_offset_specfile.json',
                 False,  valid_columns, [], Encodings(
                     'windows-1252'), True, Encodings('utf-8'),
                 id="invalid_offsets"),
    pytest.param('tests/specfile_doesnt_exist.json',
                 False, [], [], Encodings(
                     'windows-1252'), True, Encodings('utf-8'),
                 id="no_spec_file"),
    pytest.param(None,
                 False, [], [],  Encodings(
                     'windows-1252'), True, Encodings('utf-8'),
                 id="none_spec_file"),
    pytest.param('specfile_no_columns.json',
                 False, [], [],  Encodings(
                     'windows-1252'), True, Encodings('utf-8'),
                 id="zero_columns_spec_file"),
    pytest.param('specfile_no_offsets.json',
                 False, [], [],  Encodings(
                     'windows-1252'), True, Encodings('utf-8'),
                 id="zero_offsets_spec_file"),
    pytest.param('specfile_invalid_enc_fixed.json',
                 False, [], [],  Encodings(
                     'windows-1252'), True, Encodings('utf-8'),
                 id="junk_fixed_enc_spec_file"),
    pytest.param('specfile_invalid_enc_delimit.json',
                 False, [], [],  Encodings(
                     'windows-1252'), True, Encodings('utf-8'),
                 id="junk_delimit_enc_spec_file"),
]


@pytest.mark.parametrize('specfile, expected_result, expected_columns, expected_offsets, expected_in_encoding, expected_header_on, expected_out_encoding', spec_testdata)
class TestConverterSpec():
    def test_spec(self, specfile, expected_result, expected_columns, expected_offsets, expected_in_encoding, expected_header_on, expected_out_encoding):
        converter = Converter(specfile=specfile)
        (result, columns, offsets, fixed_with_encoding,
         included_header, delimited_encoding) = converter.encoder_spec()
        assert result == expected_result
        assert columns == expected_columns
        assert offsets == expected_offsets
        assert fixed_with_encoding == expected_in_encoding
        assert included_header == expected_header_on
        assert delimited_encoding == expected_out_encoding


encode_testdata = [
    pytest.param('tests/specfile.json', 98,
                 #          1         2         3         4         5         6         7         8         9
                 # 12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678
                 "ABCDE123456789012ABC12ABCDEFGHIJKLM1234567ABCDEFGHIJ1234567890123ABCDEFGHIJKLMNOPQRST1234567890123",
                 ["ABCDE", "123456789012", "ABC", "12", "ABCDEFGHIJKLM", "1234567", "ABCDEFGHIJ", "1234567890123", "ABCDEFGHIJKLMNOPQRST", "1234567890123"]),
]


@pytest.mark.parametrize('specfile, expected_total_offsets, input_line, expected_result', encode_testdata)
class TestConverterEncoder():

    def test_encode(self, specfile, expected_total_offsets, input_line, expected_result):
        def b64e(s):
            return base64.b64encode(s.encode()).decode()
        converter = Converter(specfile=specfile)
        total_offsets = sum(converter.offsets())
        assert converter.columns() == valid_columns
        assert converter.offsets() == valid_offsets
        assert total_offsets == expected_total_offsets
        assert total_offsets == len(input_line)
        (parsed, result) = converter.encode(input_line)
        expected_b64 = [b64e(er) for er in expected_result]
        assert result == ",".join(expected_b64)
        assert parsed


class EncoderTestSpec(unittest.TestCase):
    def test_from_type(self):
        # UTF8 = 'utf-8'
        # UTF16 = 'utf-16'
        # UTF32 = 'utf-32'
        # ASCII = 'ascii'
        # BINARY = 'binary'
        # OCTAL = 'octal'
        # HEXADECIMAL = 'hexadecimal'
        # CP1252 = 'cp1252'
        # WINDOWS1252 = 'windows-1252'
        # UNICODEESCAPE = 'unicode-escape'

        utf8_type = Encodings('utf-8')
        utf16_type = Encodings('utf-16')
        utf32_type = Encodings('utf-32')
        ascii_type = Encodings('ascii')
        binary_type = Encodings('binary')
        octal_type = Encodings('octal')
        hexadecimal_type = Encodings('hexadecimal')
        cp1252_type = Encodings('cp1252')
        window_type = Encodings('windows-1252')
        unicode_type = Encodings('windows-1252')
        assert utf8_type.is_of_type('😀')
        assert utf16_type.is_of_type('abcdé')
        assert utf32_type.is_of_type('abcdé')
        assert ascii_type.is_of_type('abcdé')
        assert binary_type.is_of_type('ABC')
        assert octal_type.is_of_type('\ue000')
        assert hexadecimal_type.is_of_type('\ue000')
        assert cp1252_type.is_of_type('ABC')
        assert window_type.is_of_type('ABC')
        assert unicode_type.is_of_type('😀')
        assert utf8_type.to_out_type('😀') == '8J+YgA=='
        

        
