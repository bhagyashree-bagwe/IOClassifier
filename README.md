# IOClassifier

sudo apt-get install python-setuptools python-dev build-essential python-pip python-dev build-essential
wget -O - http://llvm.org/apt/llvm-snapshot.gpg.key|sudo apt-key add -
#add to  sudo vi /etc/apt/sources.list
deb http://llvm.org/apt/trusty/ llvm-toolchain-trusty-3.8 main
sudo apt-get update
sudo apt-get install clang-3.8 lldb-3.8
wget https://pypi.python.org/packages/source/c/clang/clang-3.8.tar.gz
pip install clang-3.8.tar.gz
ln -s /usr/lib/llvm-3.8/lib/libclang.so.1 /usr/lib/libclang.so
python test.py test.cpp
