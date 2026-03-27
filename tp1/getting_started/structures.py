my_tuple = (1,)
my_list = []
my_set = set()
my_dico = {}

# duck typing

class SuperTropCool:
    
    def append(self, super_element):
        pass
    
def add_to_my_list(my_list:list, my_item:str):
    my_list.append(my_item)
    
if __name__ == '__main__':
    add_to_my_list([], 'chaine')
    add_to_my_list(SuperTropCool(), 12)
    