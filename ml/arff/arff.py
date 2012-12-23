import os
import io
import csv
from collections import namedtuple



UNKNOW_REAL= -1e308
UNKNOW_CAT = '?'

COMMENT = '%'
SPECIAL = '@'
RELATION = '@relation'
ATTRIBUTE = '@attribute'
DATA = '@data'


def _str_remove_quotes(obj):
    return str(obj[1:-1])


def GenerateRowBase(field_names):
    """
    Rows should behave like so:
        * list(row) should give the values in order
        * row['class'] should get the column named 'class'
        * row[i] should get the i-th column
        * row.balls should get the column named 'balls'
    """
    class Row:
        def __init__(self, *values):
            # iter access
            self._values = list(values)
            # names access
            self._data = dict(zip(field_names, self._values))
            # numbered order access
            self._data.update(enumerate(self._values))

        def __getattr__(self, key):
            if key in self._data:
                return self._data[key]
            else:
                return object.__getattr__(self, key)

        def __getitem__(self, key):
            return self._data[key]

        def __repr__(self):
            return '<Row(%s)>' % ','.join([repr(i) for i in self._values])

        def __iter__(self):
            return iter(self._values)

        def __len__(self):
            return len(self._values)

    return Row

ARFF_TYPES = {
    'numeric': float,
    'integer': int,
    'real': float,
    'string': _str_remove_quotes,
}

PYTHON_TYPES = {
    float: 'real',
    int: 'integer',
    str: 'string',
    bool: '{True, False}'
}

DEFAULT_REPRS = {
                }


#def add_optional_types():
#    try:
#        import numpy
#        PYTHON_TYPES[numpy.float64] = 'real'
#        PYTHON_TYPES[numpy.int64] = 'integer'
#    except ImportError:
#        pass
#
#    try:
#        PYTHON_TYPES[long] = 'integer'
#        DEFAULT_REPRS[long] = str
#    except NameError:
#        pass
#
#    try:
#        PYTHON_TYPES[unicode] = 'string'
#        DEFAULT_REPRS[unicode] = lambda x: x.encode('utf-8')
#    except NameError:
#        pass
#
#add_optional_types()


# python2/3 compatible unicode
def _u(text):
    if str == bytes:
        return text.decode('utf-8')
    else:
        # python 3
        return text


def _csv_split(line):
    return next(csv.reader([line]))




class NominalType:
    '''Parses and validates the arff enum'''
    def __init__(self, name, type_text):
        self.name = name
        self.type_text = type_text
        values_str = type_text.strip('{} ')
        self.enum = _csv_split(values_str)
        self.enum = [opt.strip(', \'"') for opt in self.enum]

    def parse(self, text):
        if text.strip('\'"') in self.enum:
            return text
        else:
            #raise ValueError("'%s' is not in {%s}" % (text, self.enum))
            return UNKNOW_CAT


class SimpleType:
    def __init__(self, name, type_text):
        self.name = name
        self.type = ARFF_TYPES[type_text]

    def parse(self, text):
        try:
            return self.type(text)
        except ValueError:
            return UNKNOW_REAL


def _parse_types(row, fields):
    typed_row = []
    for i, ftype in enumerate(fields):
        typed_row.append(ftype.parse(row[i]))

    return typed_row


class _RowParser:
    def __init__(self, fields):
        self.fields = fields
        #self.tuple = namedtuple('Row', [f.name for f in fields])
        self.rowgen = GenerateRowBase([f.name for f in fields])

    def parse(self, row):
        values = []
        for f, item in zip(self.fields, row):
            values.append(f.parse(item))

        return self.rowgen(*values)


def loads(text):
    if bytes == str:
        if not isinstance(text, unicode):
            raise ValueError('arff.loads works with unicode strings only')
    else:
        if not isinstance(text, str):
            raise ValueError('arff.loads works with strings only')
    lines_iterator = io.StringIO(text)
    for item in Reader(lines_iterator):
        yield item


def load(fname):
    with open(fname, 'r') as fhand:
        for item in Reader(fhand):
            yield item

import re
class Reader:
    def __init__(self, lines_iterator):
        self.lines_iterator = lines_iterator
        self.arfftypes = dict(ARFF_TYPES)

    def __iter__(self):
        """
        The iterator does all the parsing so the user can customize the parser
        right after construction before the reader does anything.
        """
        # if we were passed a list - make sure it behaves like an iterator
        # as we have 2 for loops that expect to not restart.
        lines_iterator = iter(self.lines_iterator)
        fields = []

        for line in lines_iterator:
            if line.startswith(COMMENT):
                continue

            if line.lower().startswith(DATA):
                break

            
            if line.lower().startswith(RELATION):
                _, relation = line.split(' ', 1)
                self.relation = relation.strip('"\' ')

            if line.lower().startswith(ATTRIBUTE):                
                space_separated = re.split('\s+', line, 2)                
                name = space_separated[1]
                field_type_text = space_separated[2].strip()
                fields.append(self._field_type(name, field_type_text))
        self.fields = fields
        

        # data
        row_parser = _RowParser(fields)
        for line in lines_iterator:
            if line.startswith(COMMENT):
                continue
            row = _csv_split(line)
            typed_row = row_parser.parse(row)
            yield typed_row

    def _field_type(self, name, type_text):
        if type_text.lower() in self.arfftypes:
            return SimpleType(name, type_text.lower())

        if type_text.startswith('{'):
            return NominalType(name, type_text)

        raise ValueError("Unrecognized attribute type: %s" % type_text)

        #'date': date_format,

########################- region of interest -#####################
def _convert_row(row):
    items = [repr(item) for item in row]
    return ','.join(items)


def dumps(*args, **kwargs):
    items = []
    rows_gen = (row for row in dump_lines(*args, **kwargs))
    return _u(os.linesep).join(rows_gen)


def dump_lines(row_iterator, relation='untitled', names=None):
    w = _LineWriter(relation, names)
    for row in row_iterator:
        for line in w.generate_lines(row):
            yield line


def dump(fname, row_iterator, relation='untitled', names=None):
    w = Writer(fname, relation, names)
    for row in row_iterator:
        w.write(row)
    w.close()


class _LineWriter:
    def __init__(self, relation='untitled', names=None):
        self.relation = relation
        self.names = names
        self._first_row = True
        self.pytypes = dict(PYTHON_TYPES)

    def generate_lines(self, row):
        if self._first_row:
            self._first_row = False
            ftypes = []
            for item in row:
                item_type = type(item)
                if item_type not in self.pytypes:
                    raise ValueError("Unknown type: %s" % item_type)
                ftypes.append(self.pytypes[item_type])
            if self.names is None:
                self.names = ['attr%d' % i for i in range(len(row))]

            yield "%s %s" % (RELATION, self.relation)

            for name, ft in zip(self.names, ftypes):
                yield "%s %s %s" % (ATTRIBUTE, name, ft)

            yield DATA

        yield self._convert_row(row)

    def _convert_obj(self, obj):
        typ = type(obj)
        if typ in DEFAULT_REPRS:
            return DEFAULT_REPRS[typ](obj)
        else:
            return repr(obj)

    def _convert_row(self, row):
        items = [self._convert_obj(item) for item in row]
        return ','.join(items)


class Writer(_LineWriter):
    def __init__(self, fname, relation='untitled', names=None):
        self.fhand = open(fname, 'wb')
        _LineWriter.__init__(self, relation, names)

    def write(self, row):
        for line in self.generate_lines(row):
            line = line + os.linesep
            self.fhand.write(line.encode('utf-8'))

    def close(self):
        self.fhand.close()
