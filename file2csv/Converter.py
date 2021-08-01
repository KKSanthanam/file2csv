import json
import base64
from enum import Enum, EnumMeta, unique
from os.path import abspath, exists

class EncodingEnumMeta(EnumMeta):
    def __str__(cls):
        lines = [f"Members of `{cls.__name__}` are:"]
        for member in cls:
            lines.append(f"- {member}")
        return '\n'.join(lines)

    def _contains(self, member):
        return member in self._member_map_ \
            or member in set(
                map(lambda x: x.value, self._member_map_.values()))

    def is_valid(self, member):
        if self._contains(member):
            return True
        else:
            return False


@unique
class Encodings(Enum):
    """
      Python encodings
      ascii()
      bin()
      bytes()
      chr()
      hex()
      int()
      oct()
      ord()
      str()  
    """
    UTF8 = 'utf-8'
    UTF16 = 'utf-16'
    UTF32 = 'utf-32'
    ASCII = 'ascii'
    BINARY = 'binary'
    OCTAL = 'octal'
    HEXADECIMAL = 'hexadecimal'
    CP1252 = 'cp1252'
    WINDOWS1252 = 'windows-1252'
    UNICODEESCAPE = 'unicode-escape'

    def describe(self):
        # self is the member here
        return self.name, self.value

    def __str__(self):
        return f'value of the encoding is {self.value}'

    @classmethod
    def default_delimited_enc(cls):
        # cls here is the enumeration
        return cls.UTF8

    @classmethod
    def default_fixedwidth_enc(cls):
        # cls here is the enumeration
        return cls.WINDOWS1252

    @classmethod
    def is_valid(cls, value) -> bool:
        # cls here is the enumeration
        return value.lower() in cls._value2member_map_

    @classmethod
    def to_out_type(cls, value) -> str:
        def b64e(s):
            return base64.b64encode(s.encode()).decode()
        return b64e(value)

    @classmethod
    def is_of_type(cls, value) -> bool:
        """
            Python encodings
            ascii()
            bin()
            bytes()
            chr()
            hex()
            int()
            oct()
            ord()
            str()  
        """
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

        v = None
        if cls == cls.UTF8 or cls == cls.UTF16 or cls == cls.UTF32 or cls == cls.UNICODEESCAPE:
            try:
                v = bytes(value)
            except:
                return False

        if cls == cls.ASCII:
            try:
                v = ascii(value)
            except:
                return False

        if cls == cls.BINARY:
            try:
                v = bin(value)
            except:
                return False

        if cls == cls.OCTAL:
            try:
                v = oct(value)
            except:
                return False

        if cls == cls.HEXADECIMAL:
            try:
                v = hex(value)
            except:
                return False

        if cls == cls.WINDOWS1252 or cls == cls.CP1252:
            try:
                v = str(value)
            except:
                return False
        return True

class Converter(object):
    def __init__(self, **kwargs):
        """ Converter(specfile=None)
                The Converter class.
                Please always use *kwargs* in the constructor.
                - *specfile*: columns configuration
                """
        super(Converter, self).__init__()
        self._specfile = kwargs.get("specfile", None)
        self._parsed = False
        self._columns = []
        self._offsets = []
        self._fixed_with_encoding = Encodings.default_fixedwidth_enc()
        self._included_header = False
        self._delimited_encoding = Encodings.default_delimited_enc()
        self.encoder_spec()

    def __str__(self):
        return f'File format specification is "{self._specfile}"'

    def __repr__(self):
        return f'specfile="{self._specfile}")'

    def encoder_spec(self):
        def get_metadata(spec_file: str) -> tuple[bool, list[str], list[int], Encodings, bool, Encodings]:
            """
              spec for columns
              ----------------

              {
              "ColumnNames": [
                  "f1",
                  "f2",
                  "f3",
                  "f4",
                  "f5",
                  "f6",
                  "f7",
                  "f8",
                  "f9",
                  "f10"
              ],
              "Offsets": [
                  "5",
                  "12",
                  "3",
                  "2",
                  "13",
                  "7",
                  "10",
                  "13",
                  "20",
                  "13"
              ],
              "FixedWidthEncoding": "windows-1252",
              "IncludeHeader": "True",
              "DelimitedEncoding": "utf-8"
            }
            """
            parsed = False
            columns = []
            offsets = []
            fixed_with_encoding = Encodings("windows-1252")
            included_header = True
            delimited_encoding = Encodings("utf-8")

            def result() -> tuple[bool, list[str], list[int], str, bool, str]:
                return (parsed, columns, offsets, fixed_with_encoding, included_header, delimited_encoding)

            if spec_file == None:
                return result()

            # read spec file
            f_path = abspath(spec_file)
            if not exists(f_path):
                print(f"The spec file {f_path} does not exist")
                parsed = False
                return result()

            with open(f_path, 'r') as specfile:
                data = specfile.read()

            # parse spec file content
            obj = json.loads(data)

            try:
                columns = obj['ColumnNames']
                if len(columns) == 0:
                    parsed = False
                    return result()
            except Exception as ex:
                print(f"Error in parsing ColumnNames: {str(ex)}")
                parsed = False
                return result()

            try:
                offsets = [int(offset) for offset in obj['Offsets']]
                if len(offsets) == 0:
                    parsed = False
                    return result()
            except Exception as ex:
                print(f"Error in parsing Offsets: {str(ex)}")
                parsed = False
                return result()

            try:
                fixed_with_encoding_str = obj['FixedWidthEncoding'].lower()
                if not Encodings.is_valid(fixed_with_encoding_str):
                    print(f"{fixed_with_encoding_str} is not valid encoding")
                    parsed = False
                    return result()
                fixed_with_encoding = Encodings(fixed_with_encoding_str)
            except Exception as ex:
                print(f"Error in parsing FixedWidthEncoding: {str(ex)}")
                parsed = False
                return result()

            try:
                included_header = bool(obj['IncludeHeader'])
            except Exception as ex:
                print(f"Error in parsing IncludeHeader: {str(ex)}")
                parsed = False
                return result()

            try:
                delimited_encoding_str = obj['DelimitedEncoding'].lower()
                if not Encodings.is_valid(delimited_encoding_str):
                    print(f"{delimited_encoding_str} is not valid encoding")
                    parsed = False
                    return result()
                delimited_encoding = Encodings(delimited_encoding_str)
            except Exception as ex:
                print(f"Error in parsing DelimitedEncoding: {str(ex)}")
                parsed = False
                return result()

            parsed = True
            return result()

        (parsed, columns, offsets, fixed_with_encoding, included_header,
         delimited_encoding) = get_metadata(self._specfile)
        result = (parsed, columns, offsets, fixed_with_encoding,
                  included_header, delimited_encoding)
        if not parsed:
            return result
        self._parsed = parsed
        self._columns = columns
        self._offsets = offsets
        self._fixed_with_encoding = fixed_with_encoding
        self._included_header = included_header
        self._delimited_encoding = delimited_encoding
        return result

    def offsets(self: object) -> list[int]:
        if not self._parsed:
            return []
        return self._offsets

    def columns(self: object) -> list[str]:
        if not self._parsed:
            return []
        return self._columns

    def get_fixed_encoding(self: object) -> Encodings:
        if not self._parsed:
            return Encodings.default_fixedwidth_enc()
        return self._fixed_with_encoding

    def get_fixed_encoding_str(self: object) -> str:
        encode = self._fixed_with_encoding
        if not self._parsed:
            encode = Encodings.default_fixedwidth_enc()
        return encode.name

    def get_delimit_encoding(self: object) -> Encodings:
        if not self._parsed:
            return Encodings.default_delimited_enc()
        return self._delimited_encoding

    def get_delimit_encoding_str(self: object) -> str:
        encode = self._delimited_encoding
        if not self._parsed:
            encode = Encodings.default_delimited_enc()
        return encode.name

    def encode(self: object, line: str) -> tuple[bool, str]:
        """
        Encode Input fixed width file using specfile
        """
        if not self._parsed:
            return (False, '')
        if len(line) != sum(self.offsets()):
            return (False, '')

        values = []
        offsets = self.offsets()
        start = 0
        for offset in offsets:
            end = start + offset
            values.append(line[start:end])
            start = end
        encoder = self.get_delimit_encoding()
        enc_values = [encoder.to_out_type(v) for v in values]
        return True, ",".join(enc_values)
