import argparse, csv, glob, time, sys
import stopit
import unittest, unittest.mock

class ForbiddenError(Exception):
    pass

class TimeoutError(Exception):
    pass

class Timer:
    def __init__(self, timeout):
        self.timeout = timeout

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *args):
        tempo = round(time.time() - self.start, 3)
        if tempo > self.timeout:
            raise TimeoutError(f"Timeout ({tempo} > {self.timeout})")


class TestCase(unittest.TestCase):
    __orig_import = __builtins__['__import__']
    __orig_open   = __builtins__['open']

    def _raise_forbidden(self, forbidden):
        # lancia una eccezione
        raise ForbiddenError(f"E' proibito usare la funzione/metodo {forbidden}")

    def forbidden_function(self, target='os.walk'):
        # torna un contesto che fa proibire l'uso della funzione target: per default 'os.walk'
        return unittest.mock.patch(target, new=lambda *x, **k: self._raise_forbidden( target ))

    def check_imports(self, allowed=[], forbidden=[]):
        # torna un contesto che fa proibire gli import non elencati in allowed o elencati in forbidden
        def _check_import(*args, **kargs):
            name = args[0]
            if name in forbidden or (not forbidden and name not in allowed):
                print(f"Importing {name} ({kargs}) (NOT allowed)")
                raise ForbiddenError(f"E' proibito importare il modulo {name}")
            else:
                #print(f"Importing {name} ({kargs}) (allowed)")
                return self.__orig_import(*args, **kargs)
        return unittest.mock.patch('builtins.__import__', new=_check_import)

    def check_open(self, allowed_filenames_modes=None):
        if not allowed_filenames_modes:
            allowed_filenames_modes = {}
        def _check_open(*args, **kargs):
            if len(args) > 1:
                mode = args[1]
            else:
                mode = kargs.get('mode','r')
            filename = args[0]
            #print(f"checking {filename} ({args}, {kargs}) against {allowed_filenames_modes}")
            if filename not in allowed_filenames_modes:
                print(f"Opening file {filename} (NOT allowed)")
                raise ForbiddenError(f"E' proibito aprire file con nome {filename}")
            if mode not in allowed_filenames_modes[filename]:
                print(f"Opening file {filename} with mode {mode} (NOT allowed)")
                raise ForbiddenError(f"E' proibito aprire il file {filename} in modo {mode}")
            #print(f"Opening file {filename} with mode {mode} (allowed)")
            return self.__orig_open(*args, **kargs)
        return unittest.mock.patch('builtins.open', new=_check_open)

    def ignored_function(self, target='builtins.print'):
        # torna un contesto che fa ignorare la funzione target: per default 'builtins.print'
        return unittest.mock.patch(target, new=lambda *x, **k: None)

    def timer(self, sec):
        '''torna un contesto di cui viene misurato il tempo di esecuzione e se necessario lanciata una eccezione per timeout alla fine'''
        return Timer(sec)

    def timeout(self, sec):
        '''torna un contesto timer.SignalTimeout che ferma il blocco alla scadenza del timeout'''
        return stopit.ThreadingTimeout(sec, swallow_exc=False)
        #return stopit.SignalTimeout(sec, swallow_exc=False)

    def check(self, value, expected, params=None, explanation=''):
        # TODO: add deepcopy of value to avoid side effects
        msg = ''
        if params:
            msg += '\twhen input={} '.format(params)
        msg += '\n\t\t%r != %r' % (value, expected)
        if explanation:
            msg += "\t<- " + explanation
        self.assertEqual(value, expected, msg)

    def check_text_file(self,a,b):
        with open(a, encoding='utf8') as f: txt_a = f.read()
        with open(b, encoding='utf8') as f: txt_b = f.read()
        lines_a = [l.strip() for l in txt_a.splitlines()]
        lines_b = [l.strip() for l in txt_b.splitlines()]
        # todo: usare una diff
        msg = 'text differ: ' + a + ' ' + b
        self.assertEqual(lines_a, lines_b, msg)

    def __image_load(self, filename):
        '''Carica l'immagine in formato PNG dal file
        filename, la converte nel formato a matrice
        di tuple e la ritorna'''
        import png
        with open(filename,'rb') as f:
            # legge l'immagine come RGB a 256 valori
            r = png.Reader(file=f)
            iw, ih, png_img, _ = r.asRGB8()
            # converte in lista di liste di tuple
            img = []
            for png_row in png_img:
                row = []
                # l'immagine PNG ha i colori in
                # un'unico array quindi li leggiamo
                # tre alla volta in una tupla
                for i in range(0,len(png_row),3):
                    row.append( ( png_row[i+0],
                                  png_row[i+1],
                                  png_row[i+2] ) )
                img.append( row )
        return img

    def check_img_file(self, a,b):
        img_a = self.__image_load(a)
        img_b = self.__image_load(b)
        wa, ha = len(img_a[0]),len(img_a)
        wb, hb = len(img_b[0]),len(img_b)
        self.assertEqual(wa, wb, "images have different widts {} != {})".format(wa,wb))
        self.assertEqual(ha, hb, "images have different heights {} != {})".format(ha,hb))
        for y in range(ha):
            for x in range(wa):
                ca, cb = img_a[y][x], img_b[y][x] 
                msg = 'images differ, starting at coordinates {},{} (colors: {} != {})'.format(x, y, ca, cb)
                self.assertEqual(ca, cb, msg)

    def check_json_file(self, a, b, msg='I due file JSON contengono strutture diverse'):
        import json
        with open(a,'r', encoding='utf8') as f1:
            A = json.load(f1)
        with open(b,'r', encoding='utf8') as f2:
            B = json.load(f2)
        self.assertEqual(A, B, msg)

    @classmethod
    def main(cls):
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(cls))
        runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
        result = runner.run(suite)
        failed = len(result.failures)
        passed = result.testsRun-failed
        print("{} test passed, {} tests failed".format(passed, failed))  

