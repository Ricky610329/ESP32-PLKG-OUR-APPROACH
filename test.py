import serial
import time

def gbk_2_number(strsrc):

    result = []

    for i in range(0,len(strsrc),2):
        tmp = strsrc[i:i+2]       
        result.append(tmp)        
        #print(tmp, result)


    tmp1 = ''
    for i in range(len(result)):        
        if result[i]== '2e':
            tmp1 += '.'
        else:            
            tmp1 += str(int(result[i]) - 30)
            #print('tmp: ',tmp1)

    
    return tmp1


ser = serial.Serial("COM6", 115200)   # 選擇串口，並設置波特率
if ser.is_open:
    print("port open success")
    # hex(16進制)轉換爲bytes(2進制)，應注意Python3.7與Python2.7此處轉換的不同
    send_data = bytes.fromhex('65 0d 05 00 FF FF FF FF')    # 發送數據轉換爲b'\xff\x01\x00U\x00\x00V'
    ser.write(send_data)   # 發送命令
    time.sleep(0.1)        # 延時，否則len_return_data將返回0，此處易忽視！！！

    len_return_data = ser.inWaiting()
    if len_return_data:
        #print("enter receive data: ")
        return_data = ser.read(len_return_data)  # 讀取緩衝數據
        print('16hex rx: ',return_data.hex())
        
        # bytes(2進制)轉換爲hex(16進制)，應注意Python3.7與Python2.7此處轉換的不同，並轉爲字符串後截取所需數據字段，再轉爲10進制
        str_return_data = str(return_data.hex())

        #十六進制字符轉換爲漢字(str_return_data)
        rece_Chinese = bytes.fromhex(str_return_data).decode('gbk')
        print('rx: ', rece_Chinese)
        
        start_l = str_return_data.find('22')
        end_r = str_return_data.rfind('22')
        

        number_x = str_return_data[start_l+2:end_r]
        
        number_result = gbk_2_number(number_x)
        print('number_result: ',number_result)
        
       
        feedback_data = int(str_return_data[-6:-2], 16)
        #print(feedback_data)
else:
    print("port open failed")