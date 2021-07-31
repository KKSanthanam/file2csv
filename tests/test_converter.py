import pytest
import sys
from file2csv.Converter import Converter


# Converter(fixedfile=None, csvfile=None, specfile=None)

@pytest.mark.parametrize('fixedfile, csvfile, specfile', [('fixedfile.txt', 'csvfile.csv', 'specfile.json')])     
class TestConverter():
    def test_trig(self, fixedfile, csvfile, specfile):
        converter = Converter(fixedfile=fixedfile, csvfile=csvfile, specfile=specfile)
        (result, _,_,_,_, _) = converter.encoder_spec() 
        assert result
        