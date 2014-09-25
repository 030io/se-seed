se-seed
==========

一个 Python 工程项目模板
 
STEP.01
----------

项目顶级目录，一般称为工作目录，负责配置、组装工程的地方。我们首先装配几个东西，版本号从 SETP.01 开始：

    .gitignore  # 排除编译性文件、日志、setuptools 中间文件
    setup.py    # setuptools 装配设置
    tests/      # 单元测试目录
        __init__.py
    
其中关键部分为 **setup.py**：

    from setuptools import setup
    setup(
        name='se-seed',
        author='Chinfeng Chung',
        test_suite = 'tests',
    )
    
目前这个配置文件，除了配置一些基本信息，就是确定 tests 的 package 为单元测试目录（注意该目录中含有\_\_init\_\_.py，是一个标准的包结构。

至此空目录结构构建完毕，我们就可以使用以下命令来看系统能否正常运作：

    python setup.py test