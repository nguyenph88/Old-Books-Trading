#############################################################
# 
# Author: Peter Nguyen
# Last Update: 07/18/2014
# Description: Unchangable things linked to the "models.py"
# 
#############################################################

#create class for quicksort that non recursive
class QSort:
    def __init__(self, lst):
        self.lst = lst
 
    def sorted(self):
        self.qsort_swap(0, len(self.lst))
        return self.lst
 
    def qsort_swap(self, begin, end):
        if (end - begin) > 1:
           pivot = self.lst[begin]
           l = begin + 1
           r = end
           while l < r:
               if self.lst[l] <= pivot:
                   l += 1
               else:
                   r -= 1
                   self.lst[l], self.lst[r] = self.lst[r], self.lst[l]
 
           l -= 1
           self.lst[begin], self.lst[l] = self.lst[l], self.lst[begin]    
           # print begin, end, self.lst
           self.qsort_swap(begin, l)
           self.qsort_swap(r, end)     
 
#call quicksort function
def do_qsort_swap(lst):
    sort = QSort(lst)
    return sort.sorted()