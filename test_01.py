
import testlib
from ddt import file_data, ddt, data, unpack

DEBUG=True
DEBUG=False

import program01 as program

@ddt
class Test(testlib.TestCase):

    def do_test(self, name, N):
        '''Implementazione del test
            - name: nome del file in cui cercare i quadrati
            TIMEOUT: 1 secondo per ciascun test
        '''
        filepng  = f"{name}.png"
        filetxt  = f"test_{name}.txt"
        expected = f"{name}.txt"
        if DEBUG:
            result = program.es1(filepng, filetxt)
        else:
            with    self.ignored_function('pprint.pprint'), \
                    self.forbidden_function('builtins.input'), \
                    self.timeout(1), \
                    self.timer(1), \
                    self.check_open(allowed_filenames_modes={
                        filepng : ['rb', 'br'],
                        filetxt : ['w', 'a', 'wt', 'tw', 'at', 'ta'],
                        }):
                result = program.es1(filepng, filetxt)
        self.assertIsInstance(result,  int, "il risultato prodotto non e' un intero")
        self.assertEqual(     result,  N,   "l'intero restituito non e' corretto")
        self.check_text_file(filetxt, expected)

    @data(  
            ("appoggiata",            5),
            ("rettangoli_5",          5),
            ("rettangoli_10",        10),
            ("rettangoli_20",        20),
            ("rettangoli_grande_5",  10),
            ("rettangoli_grande_10", 20),
            ("rettangoli_grande_20", 40),
            ("casuale_5",             5),
            ("casuale_25",           25),
            ("casuale_45",           45),
           )
    @unpack
    def test_foto(self, name, N):
        return self.do_test(name,N)

    
if __name__ == '__main__':
    Test.main()

