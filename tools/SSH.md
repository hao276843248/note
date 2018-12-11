Ubuntu安装SSH服务
sudo apt-get install openssh-server
生成秘钥
ssh-keygen
首先选择存储位置，默认是~/.ssh目录
然后要求输入口令，可以为空
存储目录下有一对以id_dsa或id_rsa命名的文件
后缀.pub是公钥，另一个是私钥

