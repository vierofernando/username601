import gc
from PIL import Image
from io import BytesIO

class Oreo:
    def __init__(self, oreo_cupboard: str, oreo_text: str) -> None:
        """ The Oreo class. Not sponsored. """
        
        O_t = Image.open(f"{oreo_cupboard}/oreo-top.png")
        O_m = Image.open(f"{oreo_cupboard}/oreo-mid.png")
        O_b = Image.open(f"{oreo_cupboard}/oreo-bottom.png")
        
        text = str(oreo_text).lower()
        self.im_arr = []
        assert text.replace("re", "").replace("o", "") == "", f"SyntaxError: Text has something other than just 'O' and 'RE'.\n[See this YouTube video for some reference](https://www.youtube.com/watch?v=EGF9d0nM5Z0)"
        
        self.i = []
        for h in list(text):
            if h == "e": continue
            elif h == "o":
                self.i.append("o")
                continue
            self.i.append("re")
        self.i = self.i[0:13][::-1]
        
        for h in range(len(self.i)):
            if self.i[h] == "o":
                if ((h+1) == len(self.i)):
                    self.im_arr.append(O_t.copy())
                else:
                    self.im_arr.append(O_b.copy())
                continue
            self.im_arr.append(O_m.copy())
        
        del O_b, O_m, O_t
    
    def _gv(self, h: int) -> int:
        """ h """
    
        try:
            if self.i[h] == "re" and self.i[h - 1] == "re":
                return 10
            elif self.i[h] == "re" and self.i[h - 1] == "o":
                return 5
            elif self.i[h] == "o" and self.i[h - 1] == "o":
                return 25
            else:
                return 33
        except:
            return 0
    
    def meme(self) -> BytesIO:
        """ Turn the oreo to a meme. """
        
        if not self.im_arr: return
        m = Image.new("RGB", (500, 430), color=(255, 255, 255))
        
        c = 300
        for h in range(len(self.im_arr)):
            c -= self._gv(h)
            m.paste(self.im_arr[h], (161, c), self.im_arr[h])
        
        self.b = BytesIO()
        m.save(self.b, format="png")
        m.close()
        self.b.seek(0)
        del m, c
        return self.b
    
    def eat(self) -> None:
        """ Eats the oreo. Yum! """
        
        del (
            self.im_arr,
            self.i,
            self.b
        )
        
        gc.collect()