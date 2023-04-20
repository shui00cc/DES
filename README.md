# DES

项目说明：
    本项目为四川大学应用密码学课程的课程实践，包含了两个实验：

1. 分别实现 ECB、CBC、CFB、OFB 这四种操作模式的 DES。每种操作模式都有一组对应的测试数据，以便检查程序的正确性。其中，CFB 操作模式为 32 位 CFB 操作模式，OFB 操作模式为 32 位 OFB 操作模式。

2. 要求以命令行的形式，指定明文文件、密钥文件、初始化向量文件的位置和名称、加密的 操作模式以及加密完成后密文文件的位置和名称。加密时先分别从指定的明文文件、密钥 文件和初始化向量文件中读取有关信息，然后按指定的操作模式进行加密，最后将密文 （用 16 进制表示）写入指定的密文文件。

3. 分别实现对每种操作模式下加密及解密速度的测试，要求在程序中生成 5MB 的随机测试数据，连续加密、解密 10 次，记录并报告每种模式的加密和解密的总时间（毫秒）和 速度（MByte/秒）。 
4. 额外输出每个加密分组中第𝑛轮加密的输出，其中𝑛 = 学号 𝑚𝑜𝑑 16,例如如果同学的学号 是 12345678，那么需要输出第𝑛 = 14轮 Feistel 加密的输出。

文件说明：
    util.py中实现DES算法中的基本操作以及实验中所需的类型转换
    DES.py中实现了DES算法的具体结构（函数调用部分）并定义了一个DES加密器类以及一个DES解密器类用于实现四种模式对文件的加密和解密
    test.py中为加密、解密及其速度测试部分代码

**命令行输入格式**

```shell
DES.py -p des_plain.txt -k des_key.txt -v des_key.txt -m ECB -c des_cipher.txt
```



项目参考[GitHub：jackfromeast/DES_algorithm]([jackfromeast/DES_algorithm: 使用DES加密算法通过四种操作模式（ECB\CBC\CFB\OFB）实现对文件的加密；Using DES algorithm encode files through four different patterns (github.com)](https://github.com/jackfromeast/DES_algorithm))