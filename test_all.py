import lib.maps
import lib.chorded

def test_all():
    print()
    ch = lib.chorded.Chorded('hi')
    assert(ch.handle_button_down(0) == 'e')
    
