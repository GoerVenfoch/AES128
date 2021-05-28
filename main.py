if __name__ == '__main__':

    import os
    import time

    import aes128
    
    print('Шаг 1:')
    while True:
        print('Введите 1, чтобы зашифровать данные\nВведите 2, чтобы расшифровать данные')
        way = input()
        if way not in ['1', '2']:
            print('Доступ запрещен. Попробуйте ещё раз')
            continue
        else:
            break
    print()

    print('Шаг 2:')
    while True:
        print('Введите имя файла')
        input_path = os.path.abspath(input())

        if os.path.isfile(input_path):
            break
        else:
            print('Ой, извините, но это не файл!')
            continue
    print()

    print('Шаг 3:')
    while True:
        print('Введите свой ключ для шифрования/дешифрования. Ключ должен быть меньше 16 символов!')
        key = input()
        
        if len(key) > 16:
            print('Блин, слишком много. Давай меньше 16 символов!')
            continue
        
        for symbol in key:
            if ord(symbol) > 0xff:
                print('Этот ключ не сработает. Попробуйте другой. Используйте только латинский алфавит и цифры!')
                continue
        
        break

    time_before = time.time()

    with open(input_path, 'rb') as f:
        data = f.read()

    if way == '1':
        crypted_data = []
        temp = []
        for byte in data:
            temp.append(byte)
            if len(temp) == 16:
                crypted_part = aes128.encrypt(temp, key)
                crypted_data.extend(crypted_part)
                del temp[:]
        else:
            if 0 < len(temp) < 16:
                empty_spaces = 16 - len(temp)
                for i in range(empty_spaces - 1):
                    temp.append(0)
                temp.append(1)
                crypted_part = aes128.encrypt(temp, key)
                crypted_data.extend(crypted_part)

        out_path = os.path.join(os.path.dirname(input_path) , 'crypted_' + os.path.basename(input_path))

        # Ounput data
        with open(out_path, 'xb') as ff:
            ff.write(bytes(crypted_data))

    else: # if way == '2'
        decrypted_data = []
        temp = []
        for byte in data:
            temp.append(byte)
            if len(temp) == 16:
                decrypted_part = aes128.decrypt(temp, key)
                decrypted_data.extend(decrypted_part)
                del temp[:] 
        else:
            if 0 < len(temp) < 16:
                empty_spaces = 16 - len(temp)
                for i in range(empty_spaces - 1):
                    temp.append(0)
                temp.append(1)
                decrypted_part = aes128.encrypt(temp, key)
                decrypted_data.extend(crypted_part) 

        out_path = os.path.join(os.path.dirname(input_path) , 'decrypted_' + os.path.basename(input_path))

        # Ounput data
        with open(out_path, 'xb') as ff:
            ff.write(bytes(decrypted_data))

    time_after = time.time()
    
print('Новый файл лeжит здесь:', out_path)
print('Операция выполнена за ', time_after - time_before, ' секунд')
print('Если что то не так, проверьте ключ который вы ввели')
time.sleep(10)