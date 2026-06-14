from random import choice




def valinta(manageri: object, kaikki: list ):
    
    #siivotaan listat siltä varalta, että "kaikki"-listaa on muutettu
    manageri.arvonta_vaihtoehdot = [x for x in manageri.arvonta_vaihtoehdot if x in kaikki]
    manageri.arvonta_estetyt = [x for x in manageri.arvonta_estetyt if x in kaikki]
