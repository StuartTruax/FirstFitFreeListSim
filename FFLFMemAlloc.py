import numpy as np

class LLNode(object):
  def __init__(self, val, next):
      self.val = val
      self.next = next

  def __str__(self):
      return "[ "+str(self.val)+" ]->"


class LL:
    @staticmethod
    def searchLL(head, val):
        if not head:
            return None

        if head.val == val:
            return head
        else:
            return LL.searchLL(head.next, val)

    @staticmethod
    def insertVal(head, val):
        node = LLNode(val,head)
        return node

    @staticmethod
    def deleteVal(head, val):
        targetNode = LL.searchLL(head,val)

        if targetNode:

            pred = LL.getPredecessorList(head,val)

            if not pred:
                head = targetNode.next
            else:
                pred.next = targetNode.next
            return head


    @staticmethod
    def getPredecessorList(head,val):
        if not head or not head.next:
            return None

        if head.next.val == val:
            return head
        else:
            return LL.getPredecessorList(head.next,val)

    @staticmethod
    def arrayToLL(array):

        head = None
        prev = None

        for i in range(0,len(array)):
            if i ==0:
                head = LLNode(array[i],None)
                prev = head
            else:
                cur = LLNode(array[i], None)
                prev.next = cur
                prev = cur

        return head


    @staticmethod
    def toString(head):
        if not head:
            return ""

        ret = str(head)

        return ret+LL.toString(head.next)



class FreeListNode(LLNode):
    def __init__(self,address,size,next):
        super(FreeListNode,self).__init__(address,next)
        self.size = size
        self.free = True

    def __str__(self):
        return "[ "+str(self.val)+","+str(self.size)+","+str(self.free)+" ]->"



class FreeList:
    def __init__(self,allocation, page_size):
        self.allocation = allocation
        self.head = FreeListNode(0,allocation,None)
        self.page_size = page_size

    def __str__(self):
        return self.__str_rec(self.head)

    def __str_rec(self,node):
        if not node:
            return ""

        ret = str(node)

        return ret+self.__str_rec(node.next)


    def malloc(self,size):
        #search the free list for a node with size > allocation
        if size <= 0:
            return -1
        elif size < self.page_size:
            size = self.page_size

        block = self.__findMemBlock(self.head, size)

        if not block:
            return None
        else:
            #once found, split if remainder exists
            if block.size > size:
                self.__split(block,size)
            # mark as free=False
            block.free = False
            return block.val

    def __findMemBlock(self,node,minSize):
        if not node:
            return None

        if node.size >= minSize and node.free:
            return node
        else:
            return self.__findMemBlock(node.next, minSize)


    def free(self, address):
        #find address
        block = LL.searchLL(self.head,address)

        if not block:
            return False
        else:
            # mark free=True
            block.free = True
            # perform merge operation
            self.__merge(block)
            self.head = self.__mergesort(self.head)
            return True


    def __split(self,block,size):
        split_address = block.val+size
        split_size = block.size-size

        block.size = size

        split_block = FreeListNode(split_address,split_size,None)
        self.__insert(split_block)

    def __merge(self,block):

        #merge with any free block directly after the freed block
        post_address =  block.val + block.size

        post_block = LL.searchLL(self.head,post_address)

        merge_node = None

        if post_block and post_block.free:
            post_merge_size = block.size+post_block.size
            post_merge_address = block.val

            merge_node = FreeListNode(post_merge_address,post_merge_size, None)
            self.head = LL.deleteVal(self.head,post_address)
            self.head = LL.deleteVal(self.head,block.val)
            self.__insert(merge_node)

        #merge with any free block directly before the freed block
        #(requires a custom search method)
        pre_block = self.__searchPreBlock(self.head,block.val)

        if pre_block and pre_block.free:
            if post_block and merge_node:
                pre_merge_size = merge_node.size+pre_block.size
            else:
                pre_merge_size = block.size+pre_block.size

            pre_merge_address = pre_block.val

            merge_node = FreeListNode(pre_merge_address,pre_merge_size,None)
            self.head = LL.deleteVal(self.head,pre_merge_address)
            self.head = LL.deleteVal(self.head,block.val)
            self.__insert(merge_node)

    def __searchPreBlock(self,node,targetAddress):
        if not node:
            return None

        if node.val+node.size == targetAddress:
            return node
        else:
            return self.__searchPreBlock(node.next,targetAddress)


    def __insert(self, node):
        node.next = self.head
        self.head = node


    def __mergesort(self,headNode):
        if not headNode:
            return None
        elif not headNode.next:
            return headNode
        else:
            (a,b) = self.__frontBackSplit(headNode)
            a = self.__mergesort(a)
            b = self.__mergesort(b)
            return self.__sortedMerge(a,b)


    def __frontBackSplit(self,headNode):

        if not headNode:
            return (None,None)

        cur=headNode
        count=1

        while cur.next:
            count+=1
            cur=cur.next

        halfIndex = int(count/2)

        #assign b list at the split point

        cur = headNode
        count=0
        while cur.next and count <= halfIndex:
            count+=1
            cur=cur.next

        a = headNode
        b = cur

        #split the a list from b list

        cur = headNode
        while cur.next != b:
            cur = cur.next

        cur.next = None

        return (a,b)

    def __sortedMerge(self,a,b):
        #recursive implementation, not suitable for production
        temp = None

        if not a:
            return b

        if not b:
            return a

        if a.val <= b.val:
            temp  = a
            temp.next = self.__sortedMerge(a.next, b)

        else:
            temp = b
            temp.next = self.__sortedMerge(a, b.next)

        return temp



    def asMatrix(self):
        N = self.allocation/self.page_size

        #make the matrix square through padding
        while not np.equal(np.mod(np.sqrt(N), 1), 0):
                N+=1

        side_length = np.sqrt(N).astype(int)
        matrix = np.ones((side_length,side_length))

        #traverse free list, filling in allocated spaces by flNode.free == False

        cur = self.head

        while cur:
            if not cur.free:
                start = cur.val/self.page_size
                end = (cur.val+cur.size)/self.page_size

                for i in range(start,end):
                    r = np.floor(i/side_length).astype(int)
                    c = np.mod(i,side_length).astype(int)
                    matrix[r,c] = 0.0

            cur = cur.next


        return matrix
