from abc import ABC, abstractmethod

# abstract class biasa bukan abc umumnya (Java, ga bisa implement)
# jadi mungkin disini bisa implementasi fungsi umum buat algoritma AI

class AIAlgorithm(ABC): 
    @abstractmethod
    def process(self, data):
        pass