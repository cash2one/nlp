#
# Autogenerated by Thrift Compiler (0.9.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
from ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol

try:
    from thrift.protocol import fastbinary
except:
    fastbinary = None


class Iface:
    def get_sentiment(self, word, mode):
        """
        Parameters:
         - word
         - mode
        """
        pass

    def get_opinion_sentence(self, text, ratio):
        """
        Parameters:
         - text
         - ratio
        """
        pass


class Client(Iface):
    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def get_sentiment(self, word, mode):
        """
        Parameters:
         - word
         - mode
        """
        self.send_get_sentiment(word, mode)
        return self.recv_get_sentiment()

    def send_get_sentiment(self, word, mode):
        self._oprot.writeMessageBegin('get_sentiment', TMessageType.CALL, self._seqid)
        args = get_sentiment_args()
        args.word = word
        args.mode = mode
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_get_sentiment(self):
        (fname, mtype, rseqid) = self._iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(self._iprot)
            self._iprot.readMessageEnd()
            raise x
        result = get_sentiment_result()
        result.read(self._iprot)
        self._iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        raise TApplicationException(TApplicationException.MISSING_RESULT, "get_sentiment failed: unknown result");

    def get_opinion_sentence(self, text, ratio):
        """
        Parameters:
         - text
         - ratio
        """
        self.send_get_opinion_sentence(text, ratio)
        return self.recv_get_opinion_sentence()

    def send_get_opinion_sentence(self, text, ratio):
        self._oprot.writeMessageBegin('get_opinion_sentence', TMessageType.CALL, self._seqid)
        args = get_opinion_sentence_args()
        args.text = text
        args.ratio = ratio
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_get_opinion_sentence(self):
        (fname, mtype, rseqid) = self._iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(self._iprot)
            self._iprot.readMessageEnd()
            raise x
        result = get_opinion_sentence_result()
        result.read(self._iprot)
        self._iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        raise TApplicationException(TApplicationException.MISSING_RESULT,
                                    "get_opinion_sentence failed: unknown result");


class Processor(Iface, TProcessor):
    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap["get_sentiment"] = Processor.process_get_sentiment
        self._processMap["get_opinion_sentence"] = Processor.process_get_opinion_sentence

    def process(self, iprot, oprot):
        (name, type, seqid) = iprot.readMessageBegin()
        if name not in self._processMap:
            iprot.skip(TType.STRUCT)
            iprot.readMessageEnd()
            x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
            oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
            x.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()
            return
        else:
            self._processMap[name](self, seqid, iprot, oprot)
        return True

    def process_get_sentiment(self, seqid, iprot, oprot):
        args = get_sentiment_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = get_sentiment_result()
        result.success = self._handler.get_sentiment(args.word, args.mode)
        oprot.writeMessageBegin("get_sentiment", TMessageType.REPLY, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_get_opinion_sentence(self, seqid, iprot, oprot):
        args = get_opinion_sentence_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = get_opinion_sentence_result()
        result.success = self._handler.get_opinion_sentence(args.text, args.ratio)
        oprot.writeMessageBegin("get_opinion_sentence", TMessageType.REPLY, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()


# HELPER FUNCTIONS AND STRUCTURES

class get_sentiment_args:
    """
    Attributes:
     - word
     - mode
    """

    thrift_spec = (
        None,  # 0
        (1, TType.STRING, 'word', None, None,),  # 1
        (2, TType.STRING, 'mode', None, None,),  # 2
    )

    def __init__(self, word=None, mode=None, ):
        self.word = word
        self.mode = mode

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans,
                                                                                        TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.word = iprot.readString();
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.mode = iprot.readString();
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('get_sentiment_args')
        if self.word is not None:
            oprot.writeFieldBegin('word', TType.STRING, 1)
            oprot.writeString(self.word)
            oprot.writeFieldEnd()
        if self.mode is not None:
            oprot.writeFieldBegin('mode', TType.STRING, 2)
            oprot.writeString(self.mode)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.iteritems()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class get_sentiment_result:
    """
    Attributes:
     - success
    """

    thrift_spec = (
        (0, TType.STRING, 'success', None, None,),  # 0
    )

    def __init__(self, success=None, ):
        self.success = success

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans,
                                                                                        TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRING:
                    self.success = iprot.readString();
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('get_sentiment_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRING, 0)
            oprot.writeString(self.success)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.iteritems()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class get_opinion_sentence_args:
    """
    Attributes:
     - text
     - ratio
    """

    thrift_spec = (
        None,  # 0
        (1, TType.STRING, 'text', None, None,),  # 1
        (2, TType.DOUBLE, 'ratio', None, None,),  # 2
    )

    def __init__(self, text=None, ratio=None, ):
        self.text = text
        self.ratio = ratio

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans,
                                                                                        TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.text = iprot.readString();
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.DOUBLE:
                    self.ratio = iprot.readDouble();
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('get_opinion_sentence_args')
        if self.text is not None:
            oprot.writeFieldBegin('text', TType.STRING, 1)
            oprot.writeString(self.text)
            oprot.writeFieldEnd()
        if self.ratio is not None:
            oprot.writeFieldBegin('ratio', TType.DOUBLE, 2)
            oprot.writeDouble(self.ratio)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.iteritems()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class get_opinion_sentence_result:
    """
    Attributes:
     - success
    """

    thrift_spec = (
        (0, TType.STRING, 'success', None, None,),  # 0
    )

    def __init__(self, success=None, ):
        self.success = success

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans,
                                                                                        TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRING:
                    self.success = iprot.readString();
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('get_opinion_sentence_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRING, 0)
            oprot.writeString(self.success)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.iteritems()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
