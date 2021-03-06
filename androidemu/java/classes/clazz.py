from ..java_class_def import JavaClassDef
from ..java_field_def import JavaFieldDef
from ..java_method_def import java_method_def, JavaMethodDef
from ..constant_values import *
from .string import *
from .method import *

import io

class Class(metaclass=JavaClassDef, jvm_name='java/lang/Class'):
    class_loader = None
    _basic_types = ["Z", "B", "C", "D", "F", "I", "J", "S"]
    def __init__(self, pyclazz):
        self.__pyclazz = pyclazz
        self.__descriptor_represent = pyclazz.jvm_name
    #

    @java_method_def(name='getClassLoader', signature='()Ljava/lang/ClassLoader;', native=False)
    def getClassLoader(self, emu):
        return Class.class_loader
    #

    @java_method_def(name='getName', signature='()Ljava/lang/String;', native=False)
    def getName(self, emu):
        name = self.__descriptor_represent
        assert name != None

        name = name.replace("/", ".")
        return String(name)
    #

    def get_jni_descriptor(self):
        return self.__descriptor_represent
    #


    @java_method_def(name='getDeclaredField', args_list=["jstring"], signature='(Ljava/lang/String;)Ljava/lang/reflect/Field;', native=False)
    def getDeclaredField(self, emu, name):
        raise NotImplementedError()
    #

    @java_method_def(name='getDeclaredMethod', args_list=["jstring", "jobject"], signature='(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;', native=False)
    def getDeclaredMethod(self, emu, name, parameterTypes):
        logger.debug("getDeclaredMethod name:[%r] parameterTypes:[%r]"%(name, parameterTypes))
        sbuf = io.StringIO()
        sbuf.write("(")
        for item in parameterTypes:
            desc = item.get_jni_descriptor()
            if (desc[0] == "[" or desc in Class._basic_types):
                sbuf.write(desc)
            #
            else:
                sbuf.write("L")
                sbuf.write(desc)
                sbuf.write(";")
            #
        #
        sbuf.write(")")

        signature_no_ret = sbuf.getvalue()
        pyname = name.get_py_string()
        pymethod = self.__pyclazz.find_method_sig_with_no_ret(pyname, signature_no_ret)
        if (pymethod == None):
            assert False, "getDeclaredMethod not found..."
            return JAVA_NULL
        #
        reflected_method = Method(self.__pyclazz, pymethod)
        logger.debug("getDeclaredMethod return %r"%reflected_method)
        return reflected_method
    #

    def __repr__(self):
        return "Class(%s)"%self.__descriptor_represent
    #
#
