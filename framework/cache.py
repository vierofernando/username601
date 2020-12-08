from numpy import array, where, append

class CacheManager:
    def __init__(self):
        self.v = array([])
        self.i = array([])
    
    def add(self, name, value):
        self.i = append(self.i, name)
        self.v = append(self.v, value)
    
    def exists(self, name):
        try:
            t = where(self.i == name)[0][0]
            del t
            return True
        except:
            return False
    
    def get(self, name):
        try:
            i = where(self.i == name)[0][0]
            return self.v[i]
        except:
            return None
    
    def clear(self, dont_restore=False):
        del self.v, self.i
        if dont_restore: return
        self.v = array([])
        self.i = array([])