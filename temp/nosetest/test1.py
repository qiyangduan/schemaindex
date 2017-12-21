from nose import with_setup
def setup_func():
    print("set up test fixtures")

def teardown_func():
    print("tear down test fixtures")


def multiply(x,y):
    return x*y

@with_setup(setup_func, teardown_func)
def test_numbers_3_4():
    print("1111")
    assert multiply(3, 4) == 12


def test_strings_a_3():
    print("11112222")
    assert multiply('a', 3) == 'aaa'