# -*- coding: UTF-8 -*-
import os

from util import *
import argparse


def cipher(message, key, mode='encrypt'):
    subkeys = CreateSubKeys(key) if mode == 'encrypt' else CreateSubKeys(key)[::-1]  # 顺序相反取密钥
    text = IpPermutation(message)

    for i in range(16):
        l, r = text[:32], text[32:]
        r_extend = ExtendPermutation(r)
        xor1 = xor(r_extend, subkeys[i])
        s_box_result = SBoxPermutation(xor1)
        p_box_result = PBoxPermutation(s_box_result)
        xor2 = xor(l, p_box_result)
        text = r + xor2
        # # 实现学号对应轮加密结果记录
        # if i == (2021141530127%16):
        #     mytext = text[32:] + text[:32]
        #     myoutput = InverseIpPermutation(mytext)
        #     print(f'第{2021141530127%16}轮加密的输出为：{myoutput}')

    text = text[32:] + text[:32]
    return InverseIpPermutation(text)


def fill(message):
    '''
    填充函数，若字符分组长度不为16的倍数，使用默认字符“0”补全为16的整数倍。
    '''
    try:
        mod = len(message) % 64
        space = 64 - mod
        while (space > 0):
            message = message.append("0")
            space -= 1
        return message
    except AttributeError:
        print(message)


class DES_encrypter:
    """
       DES加密器
       message：字符串类型表示的16进制明文
       key:加密密钥,字符串类型表示的16进制
       mode:操作方式（ECB, CBC, CFB, OFB）
       iv:字符串类型表示的16进制的初始化向量
    """

    def __init__(self, message, key, mode, iv):
        self.message = string2bin(message)
        self.key = string2bin(key)
        self.mode = mode
        self.iv = string2bin(iv)

    @property
    # 将ciphertext修饰为属性
    def ciphertext(self):
        if (self.mode == "ECB"):
            return bin2string(self.__ECBencrypt())
        if (self.mode == "CBC"):
            return bin2string(self.__CBCencrypt())
        if (self.mode == "CFB"):
            return bin2string(self.__CFBencrypt())
        else:
            return bin2string(self.__OFBencrypt())

    def __ECBencrypt(self):
        """密码本模式"""
        output = []
        length = len(self.message)
        times, mod = length // 64, length % 64

        if mod:
            self.message = fill(self.message)
            times += 1

        for i in range(times):
            result = cipher(self.message[i * 64:i * 64 + 64], self.key, 'encrypt')
            output.extend(result)

        return output

    def __CBCencrypt(self):
        """密码块链接模式"""
        output = []
        length = len(self.message)
        times, mod = length // 64, length % 64

        if mod:
            self.message = fill(self.message)
            times += 1

        lastrecord = self.iv
        for i in range(times):
            submessage = self.message[i * 64:i * 64 + 64]
            submessage = xor(submessage, lastrecord)
            result = cipher(submessage, self.key, 'encrypt')
            output.extend(result)
            lastrecord = result

        return output

    def __CFBencrypt(self):
        """密码反馈模式
           这里采用1字节反馈模式即一次仅加密明文8位，并更新寄存器中保存的密码流8位
        """
        output = []
        length = len(self.message)
        times, mod = length // 32, length % 32
        if mod:
            space = 32 - mod
            while (space > 0):
                self.message = self.message.append("0")
                space -= 1
            times += 1

        register = self.iv
        for i in range(times):
            submessage = self.message[i * 32:i * 32 + 32]
            code = cipher(register, self.key, 'encrypt')
            result = xor(code[0:32], submessage)
            register = register[32:] + result[0:32]
            output.extend(result)

        return output
    def __OFBencrypt(self):
        """输出反馈模式
           与CFB相似，只不过密码流不再依赖明文或者生成的密文
           同样采用1字节反馈模式
        """
        output = []
        length = len(self.message)
        times, mod = length // 32, length % 32
        if mod:
            space = 32 - mod
            while (space > 0):
                self.message = self.message.append("0")
                space -= 1
            times += 1

        register = self.iv
        for i in range(times):
            submessage = self.message[i * 32:i * 32 + 32]
            code = cipher(register, self.key, 'encrypt')
            result = xor(code[0:32], submessage)
            register = register[32:] + code[0:32]
            output.extend(result)

        return output


class DES_decrypter:
    """DES解密器"""

    def __init__(self, cipher, key, mean, iv):
        self.cipher = string2bin(cipher)
        self.key = string2bin(key)
        self.mean = mean
        self.iv = string2bin(iv)

    @property
    def plaintext(self):
        if (self.mean == "ECB"):
            return bin2string(self.__ECBdecrypt())
        if (self.mean == "CBC"):
            return bin2string(self.__CBCdecrypt())
        if (self.mean == "CFB"):
            return bin2string(self.__CFBdecrypt())
        else:
            return bin2string(self.__OFBdecrypt())

    def __ECBdecrypt(self):
        """密码本模式"""
        output = []
        length = len(self.cipher)
        times, mod = length // 64, length % 64

        if mod:
            self.cipher = fill(self.cipher)
            times += 1

        for i in range(times):
            result = cipher(self.cipher[i * 64:i * 64 + 64], self.key, 'decrypt')
            output.extend(result)

        return output

    def __CBCdecrypt(self):
        """密码块链接模式"""
        output = []
        length = len(self.cipher)
        times, mod = length // 64, length % 64

        if mod:
            self.cipher = fill(self.cipher)
            times += 1

        lastrecord = self.iv
        for i in range(times):
            submessage = self.cipher[i * 64:i * 64 + 64]
            submessage = cipher(submessage, self.key, 'dcrypt')
            result = xor(submessage, lastrecord)
            output.extend(result)
            lastrecord = self.cipher[(i) * 64:(i) * 64 + 64]

        return output

    def __CFBdecrypt(self):
        """密码反馈模式"""
        output = []
        length = len(self.cipher)
        times, mod = length // 32, length % 32

        if mod:
            space = 32 - mod
            while (space > 0):
                self.cipher = self.cipher.append("0")
                space -= 1
            times += 1

        register = self.iv
        for i in range(times):
            subcipher = self.cipher[i * 32:i * 32 + 32]
            code = cipher(register, self.key, 'encrypt')
            result = xor(code[0:32], subcipher)
            register = register[32:] + subcipher[0:32]
            output.extend(result)

        return output

    def __OFBdecrypt(self):
        """密码反馈模式"""
        output = []
        length = len(self.cipher)
        times, mod = length // 32, length % 32

        if mod:
            space = 32 - mod
            while (space > 0):
                self.cipher = self.cipher.append("0")
                space -= 1
            times += 1

        register = self.iv
        for i in range(times):
            subcipher = self.cipher[i * 32:i * 32 + 32]
            code = cipher(register, self.key, 'encrypt')
            result = xor(code[0:32], subcipher)
            register = register[32:] + code[0:32]
            output.extend(result)

        return output

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='test')
    parser.add_argument('-p', '--plainfile', default='des_plain.txt', help='指定明文文件的位置和名称')
    parser.add_argument('-k', '--keyfile', default='des_key.txt', help='指定密钥文件的位置和名称')
    parser.add_argument('-v', '--vifile', default='des_vi.txt', help='指定初始化向量文件的位置和名称')
    parser.add_argument('-m', '--mode', default='ECB', help='指定加密的操作模式')
    parser.add_argument('-c', '--cipherfile', default='des_cipher.txt', help='指定密文文件的位置和名称')

    args = parser.parse_args()

    global key, iv
    with open(args.keyfile) as f:
        key = f.readlines()
        key = [x.strip() for x in key if x.strip() != '']
    f.close()
    key = "".join(key)
    with open(args.vifile) as f:
        iv = f.readlines()
        iv = [x.strip() for x in iv if x.strip() != '']
    f.close()
    iv = "".join(iv)

    with open(args.plainfile) as f:
        plaintext = f.readlines()
        plaintext = [x.strip() for x in plaintext if x.strip() != '']
    f.close()
    plaintext = "".join(plaintext)

    crypter= DES_encrypter(plaintext, key, args.mode, iv)
    cipher= crypter.ciphertext

    with open(args.cipherfile, "a") as f:
        f.write(cipher.upper() + "\n")
    f.close()
    input('加密完成，密文在'+args.cipherfile)