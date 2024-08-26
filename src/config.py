#CONFIG FILE FOR THE COULOMB HELPER
class Config:
    k = 8.98755*10**9
    debug = False


def print_debug( *kargs, sep: str = " ", endl: str = "\n" ):
    if Config.debug is True:
        for i in kargs:
            print( i, end=sep )    
        print( end=endl )

