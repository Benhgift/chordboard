from sys import modules
from importlib import reload
import sys
import traceback
import time
import test_all

while True: 
    try: 
        try:
            del sys.modules['test_all']
        except:
            pass
        import test_all
        reload(test_all)
        test_all.pretty_tst()
    except KeyboardInterrupt:
        sys.exit()
    except:
        print()
        print(time.time())
        print(traceback.format_exc())
