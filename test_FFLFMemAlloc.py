from FFLFMemAlloc import *
import numpy as np
import matplotlib.pyplot as plt
import pytest


class TestClass(object):
    """docstring for ."""


    def test_nibble_request(self):
        """
        bite a nibble off.
        """

        fl = FreeList(1024,4)

        break_size = 32

        address0 = fl.malloc(break_size)

        assert address0==0

        assert str(fl) == "[ 32,992,True ]->[ 0,32,False ]->"


    def test_geometric_alloc_dealloc(self):
        """
        allocate geometrically as (512 K)*1/(2^i) i=0,...
        and then free in reverse order
        """

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
        """
        pre_merge
        |512|256|256|
        |XXX|XXX|XXX|
        |XXX|000|XXX|
        |XXX|0000000|
        """

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
        """
        pre_merge
        |512|256|256|
        |XXX|XXX|XXX|
        |000|XXX|XXX|
        |0000000|XXX|
        """

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
        """
        post_merge
        |512|256|256|
        |XXX|XXX|XXX|
        |XXX|000|XXX|
        |0000000|XXX|
        """

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


    def test_mid_free(self):
        """
        1024-sized heap, allocated in 32-sized blocks
        free the middle block
        """

        fl = FreeList(1024,32)

        break_size = 32

        N = 1024/32

        allocated_addresses = []

        for i in range(0,N):
            allocated_addresses.append(fl.malloc(break_size))

        assert fl.free(allocated_addresses[N/2])

        assert np.array_equal(fl.asMatrix(), np.matrix([[0, 0, 0, 0, 0, 0], \
         [0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 1, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0]\
         ,[0, 0, 1, 1, 1, 1]]))


    def test_allocate_free_allocate(self):
        """
        allocate, free, then allocate again
        """

        fl = FreeList(1024,256)

        break_size = 512

        address0 = fl.malloc(break_size)

        assert address0 == 0

        assert np.array_equal(fl.asMatrix(), np.matrix([[0, 0],[1, 1]]))

        assert str(fl) == "[ 512,512,True ]->[ 0,512,False ]->"

        assert fl.free(address0)

        address0 = fl.malloc(break_size)

        assert address0 == 0


    def test_allocate_free_allocate(self):
        """
        1024-sized heap, allocated in 32-sized blocks
        free the middle block
        """

        fl = FreeList(1024,32)

        break_size = 32

        N = 1024/32

        allocated_addresses = []

        for i in range(0,N):
            allocated_addresses.append(fl.malloc(break_size))

        assert fl.free(allocated_addresses[N/2])

        assert np.array_equal(fl.asMatrix(), np.matrix([[0, 0, 0, 0, 0, 0], \
             [0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 1, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0]\
             ,[0, 0, 1, 1, 1, 1]]))

        after_free_address = fl.malloc(break_size)

        assert after_free_address
