# -*- coding: utf-8 -*-
__author__ = 'chinfeng'

from unittest import TestCase
import jbmongo
import random

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
