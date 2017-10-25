# IOClassifier

sudo apt-get install python-setuptools python-dev build-essential python-pip python-dev build-essential<br>

wget -O - http://llvm.org/apt/llvm-snapshot.gpg.key|sudo apt-key add -<br>
#add to  sudo vi /etc/apt/sources.list<br>
deb http://llvm.org/apt/trusty/ llvm-toolchain-trusty-3.8 main<br>
sudo apt-get update<br>
sudo apt-get install clang-3.8 lldb-3.8<br>
wget https://pypi.python.org/packages/source/c/clang/clang-3.8.tar.gz<br>
pip install clang-3.8.tar.gz<br>
sudo ln -s /usr/lib/llvm-3.8/lib/libclang.so.1 /usr/lib/libclang.so<br>
python test.py test.cpp<br>
