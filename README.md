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
    
STEP.02
----------

仿照 [JPMongo](http://git.xizhe.it/jacksonpan/jpmongo) 这个项目，我们要开始进行项目的设计、开发。我们取名为 JBMongo，用自顶向下的方法，先设计再实现。

于是我们建立一个单元测试，首先以用户的角度去思考该如何使用 JBMongo，文件 tests/test_jbm.py

    from unittest import TestCase
    import jbmongo
    
    class JBMongoTestCase(TestCase):
        def setUp(self):
            # 我们首先有一个数据库，这个数据库是关联上下文的关键，命名为 Context
            self._dbc = jbmongo.DBContext()
    
        def test_coll_definition(self):
            dbc = self._dbc
    
            # 要使用我们首先需要定义一个模型
            base_document = dbc.base_document()
            class Company(base_document):
                pass
    
            # 新建一个 company
            com = Company()
            com.title = 'JB-Man有限公司'
            id = com.save()
    
            # 测试读取
            com_found = Company.find_one(dict(_id=id))
            self.assertIn('_id', com_found)
            self.assertEqual(com_found['_id'], id)  # 读取方式1
            self.assertEqual(com_found._id, id)     # 读取方式2
            self.assertEqual(com_found.title, 'JB-Man有限公司') # 测试数据一致性

当然，现在程序还跑不动，因为 jbmongo 还不存在。所以当我们再次使用 python setup.py test 命令的时候，就会在这个文件发生错误。接下来我们要做的，就是排除这个单元测试的语法错误，实现 jbmongo/\_\_init\_\_.py 如下：

    class BaseDocument(object):
        def save(self):
            return NotImplemented
    
        @classmethod
        def find_one(cls, *args, **kwargs):
            return dict(_id=1)
    
    class DBContext(object):
        def base_document(self):
            return BaseDocument
            
好了，我们在 setup.py 里面加上 pymongo 的依赖：

    setup(
        ...
        install_requires=[
            'pymongo',
        ],
    )
    
到目前为止，跑一下单元测试 python setup.py test（或者在 IDE 上能够自动识别这个单元测试），现在只剩下 AssertionError。也就是接口设计初步完成，接下来就可以填充具体业务了。

STEP.03
---------

现在来填充具体业务。目前所有的业务功能都集中在 jbmongo/\_\_init\_\_.py，首先把这部分功能分成两个部分 jbmongo/dbcontext.py 和 jbmongo/basedocument.py。然后我们把 jbmongo/\_\_init\_\_.py 重构成只有一行：

    from .dbcontext import DBContext
    
接下来我们只需要集中在 dbcontext 和 basedocument 之中进行重构，把具体业务实现。实现后执行测试：

    $ python3 setup.py test
    
    running test
    Checking .pth file support in .
    /usr/bin/python3 -E -c pass
    Searching for pymongo
    Reading http://pypi.python.org/simple/pymongo/
    Best match: pymongo 2.7.2
    Downloading https://pypi.python.org/packages/source/p/pymongo/pymongo-2.7.2.tar.gz#md5=bbd229fe0ff43ee130eed9ffa9db7353
    Processing pymongo-2.7.2.tar.gz
    Writing /tmp/easy_install-c0hhmc/pymongo-2.7.2/setup.cfg
    Running pymongo-2.7.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-c0hhmc/pymongo-2.7.2/egg-dist-tmp-w52cia
    zip_safe flag not set; analyzing archive contents...
    bson.__pycache__._cbson.cpython-32: module references __file__
    pymongo.__pycache__._cmessage.cpython-32: module references __file__        # 自动安装依赖，无需额外处理
    
    running egg_info
    creating se_seed.egg-info
    writing requirements to se_seed.egg-info/requires.txt
    writing dependency_links to se_seed.egg-info/dependency_links.txt
    writing top-level names to se_seed.egg-info/top_level.txt
    writing se_seed.egg-info/PKG-INFO
    writing manifest file 'se_seed.egg-info/SOURCES.txt'
    reading manifest file 'se_seed.egg-info/SOURCES.txt'
    writing manifest file 'se_seed.egg-info/SOURCES.txt'
    running build_ext
    test_coll_definition (tests.test_jbm.JBMongoTestCase) ... ok        # 测试清单
    
    ----------------------------------------------------------------------
    Ran 1 test in 0.004s        # 这里表示成功跑了 1 个测试函数，全部测试均 Pass
    
    OK
    
如果 setuptools 生成的中间文件太多，可以使用下面命令清除：

    $ python setup.py clean

至此我们已完成一个开发用的框架，其特点如下：

* 测试能在 IDE（PyDev 和 PyCharm）中直接识别运行
* 我们以使用者、测试者的角度，自上而下的设计程序接口
* 测试脚本能帮助接口在开发过程中不会发生“退化”

STEP.04
---------

接下来我们就可以迭代 STEP.02，增加测试的脚本来设计新的 feature。如我们增加一个测试函数：

    class JBMongoTestCase(TestCase):
        ......
        
        def test_find(self):
            dbc = self._dbc
            base_document = dbc.base_document()
    
            class Person(base_document):
                pass
            class MassageStick(base_document):
                pass
    
            _bird = random.randint(1, 1000000)
            for p in (Person(bird_index=_bird, pain=True) for i in range(10)):
                p.save()
            for s in (MassageStick(comfort_index=_bird) for i in range(20)):
                s.save()
    
            persons = Person.find(dict(bird_index=_bird))
            for p in persons:
                self.assertEqual(p.bird_index, _bird)
                self.assertEqual(p.pain, True)
                
            ........
            
通过不断迭代 设计 — 单元测试(STEP.02) — 业务代码(STEP.03) 的过程，完成你想要的系统。 

End for the beginning
----------

项目之路从此就开始。