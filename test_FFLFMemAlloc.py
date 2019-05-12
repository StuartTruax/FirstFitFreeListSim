from FFLFMemAlloc import *
import numpy as np
import matplotlib.pyplot as plt
import pytest


class TestClass(object):
    """docstring for ."""


    def test_nibble_request(self):

        fl = FreeList(1024,4)

        break_size = 32

        address0 = fl.malloc(break_size)

        assert address0==0

        assert str(fl) == "[ 0,32,False ]->[ 32,992,True ]->"


    def test_geometric_alloc_dealloc(self):

        fl = FreeList(1024,4)

        break_size = 512

        addresses = list()

        while break_size > 1:
            address = fl.malloc(break_size)
            assert isinstance(address, int)
            addresses.append(address)
            break_size = break_size/2

        for i in range(0,len(addresses)):
            assert fl.free(addresses[i])

    def test_pre_merge1(self):

        fl = FreeList(1024,256)

        break_size = 512

        address0 = fl.malloc(break_size)

        assert address0 == 0

        break_size = 256

        address1 = fl.malloc(break_size)

        assert address1 == 512


        break_size = 256

        address2 = fl.malloc(break_size)

        assert address2 == 768

        assert fl.free(address1)

        assert np.array_equal(fl.asMatrix(),np.matrix([[0, 0], [1, 0]]))

        assert fl.free(address2)

        assert np.array_equal(fl.asMatrix(), np.matrix([[0, 0], [1, 1]]))

        assert str(fl) == "[ 0,512,False ]->[ 512,512,True ]->"



    def test_pre_merge2(self):

        fl = FreeList(1024,256)

        break_size = 512

        address0 = fl.malloc(break_size)

        assert address0 == 0

        break_size = 256

        address1 = fl.malloc(break_size)

        assert address1 == 512


        break_size = 256

        address2 = fl.malloc(break_size)

        assert address2 == 768

        assert fl.free(address0)

        assert np.array_equal(fl.asMatrix(),np.matrix([[1, 1], [0, 0]]))

        assert fl.free(address1)

        assert np.array_equal(fl.asMatrix(), np.matrix([[1,1], [1, 0]]))

        assert str(fl) == "[ 0,768,True ]->[ 768,256,False ]->"


    def test_post_merge1(self):

        fl = FreeList(1024,256)

        break_size = 512

        address0 = fl.malloc(break_size)

        assert address0 == 0

        break_size = 256

        address1 = fl.malloc(break_size)

        assert address1 == 512


        break_size = 256

        address2 = fl.malloc(break_size)

        assert address2 == 768

        assert fl.free(address1)

        assert np.array_equal(fl.asMatrix(),np.matrix([[0, 0], [1, 0]]))

        assert fl.free(address0)

        assert np.array_equal(fl.asMatrix(), np.matrix([[1, 1], [1, 0]]))

        assert str(fl) == "[ 0,768,True ]->[ 768,256,False ]->"



######FreeList Test Cases################
#    plt.imshow(fl.asMatrix())
#    plt.gray()
#    plt.show()
#    print(str(fl))



#    plt.imshow(fl.asMatrix())
#    plt.gray()
#    plt.show()
