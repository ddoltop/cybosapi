import fnmatch
from collections import OrderedDict
from itertools import zip_longest

from listorm import Listorm



def expand_field_fnmatch(method_info, method_name, fields):
	if fields is None:
		fields = []
	optsets = method_info[method_name]['type'].get('options')
	if isinstance(fields, str):
		fields = [fields]

	opts = []
	for f in fields:
		for idx, opt in optsets.items():
			if fnmatch.fnmatch(opt, f):
				if opt in opts:
					continue
				if fnmatch.fnmatch(opt, f):
					opts.append(opt)
	return opts


def _encode_options(method_info, method_name, argname, optionvals, many=True):
	optsets = method_info[method_name][argname].get('options')
	if optsets is None:
		return optionvals
	revoptsets = {v: k for k, v in optsets.items()}

	args = []
	if many == True:
		for val in optionvals:
			if val in optsets:
				args.append(val)
			elif val in revoptsets:
				trans = revoptsets[val]
				args.append(trans)
			else:
				args+=[
					idx for opname, idx in revoptsets.items()
					if fnmatch.fnmatch(opname, val)
				]
		args = tuple(sorted((OrderedDict.fromkeys(args))))
	else:
		if isinstance(optionvals, (list, tuple, set)):
			optionvals = optionvals[0]

		if optionvals in optsets:
			args = optionvals
		elif optionvals in revoptsets:
			args = revoptsets[optionvals]
		else:
			try:
				arg, *_ = sorted(
					idx for opname, idx in revoptsets.items()
					if fnmatch.fnmatch(opname, optionvals)  and isinstance(optionvals, str)
				)
			except:
				raise ValueError('Option name mating fault: {}'.format(optionvals))
			else:
				args = arg
	return args


def encode_args(method_info, method_name, indexed=True,  flated=False, **kwargs):
	arginfo = method_info[method_name]

	encoded_args = []
	for argname, info in arginfo.items():
		pos = info['position']
		tp = info['type']
		many = any(t.endswith('[]') for t in tp)
		single = any(not t.endswith('[]') for t in tp)
		essential = info['essential']
		options = info.get('options')
		default = info.get('default')

		if argname not in kwargs:
			if essential == True and default is None:
				raise ValueError('{} is required'.format(argname))
			else:
				continue

		argval = kwargs[argname]

		if argval is None:
			if default:
				argval = default
			else:
				if essential == True:
					raise ValueError('{} is required'.format(argname))
				else:
					continue
		argval = _encode_options(method_info, method_name, argname, argval, many)

		if isinstance(argval, (str, bytes, int)):
			argcount = 1
		else:
			argcount = len(argval)

		if many == False and isinstance(argval, (list, tuple, set)):
			raise ValueError('{} is single argument, might be not in containter'.format(argval))

		tosingle = False
		if many == True:
			if single == True:
				if argcount == 1:
					tosingle = True
		else:
			tosingle = True

		if tosingle:
			if isinstance(argval, (list, tuple, set)):
				argval = argval[0]
			if 'long' in tp:
				val = int(argval)
			else:
				val = argval
			if options:
				if val not in options:
					raise ValueError('{} is invalid options value for {}'.format(argval, argname))
		else:
			if 'long' in tp:
				val = tuple(map(int, argval))
			else:
				val = tuple(argval)
			if options:
				noexists = []
				for v in val:
					if v not in options:
						noexists.append(v)
				if noexists:
					noexists = map(str, noexists)
					noexists = ', '.join((noexists))
					raise ValueError('{} are(is) invalid options value for {}'.format(noexists, argname))
		encoded_args.append((pos, val))

	if indexed:
		if flated == True and len(encoded_args) == 1:
			return encoded_args[0]
		else:
			return tuple(sorted(encoded_args))
	else:
		if flated == True and len(encoded_args) == 1:
			return encoded_args[0][1]
		return tuple(e[1] for e in sorted(encoded_args))


def set_inputvalue(cp, argset, blockrequest=True):
	for idx, arg in argset:
		cp.SetInputValue(idx, arg)
	if blockrequest:
		cp.BlockRequest()
	else:
		# cp.Unsubscribe()
		cp.Subscribe()
	return cp


def decode_options(method_info, method_name, argset):
	arginfo = method_info[method_name]
	kwargset = {}
	for pos, rawarg in argset:
		for argname, info in arginfo.items():
			idx = info['position']
			if pos == idx:
				optionmap = arginfo[argname].get('options')
				if optionmap:
					if isinstance(rawarg, (list, tuple, set)):
						kwargset[argname] = tuple(optionmap[e] for e in rawarg)
					else:
						kwargset[argname] = optionmap[rawarg]
				else:
					kwargset[argname] = rawarg
	return kwargset

def output_to_records(method_info, cp, argset):
	set_inputvalue_kwargs = decode_options(method_info, 'SetInputValue', argset)
	header = set_inputvalue_kwargs['field']
	ncols_argset = encode_args(method_info, 'GetHeaderValue', flated=True, indexed=False, type='columns')
	nrows_argset = encode_args(method_info, 'GetHeaderValue', flated=True, indexed=False, type='rows')
	ncols = cp.GetHeaderValue(ncols_argset)
	nrows = cp.GetHeaderValue(nrows_argset)
	
	records = []
	for r in range(nrows):
		row = []
		for c in range(ncols):
			getdatavalue_argset = encode_args(method_info, 'GetDataValue', indexed=False, index=r, type=c)
			data = cp.GetDataValue(*getdatavalue_argset)
			row.append(data)
		records.append(dict(zip(header, row)))
	return records





class InterfaceParser:

	def __init__(self, interface):
		records = self._flatten_interface(interface)		
		self.lst = Listorm(records)

	def _flatten_interface(self, interface, levelnames=['method', 'arg', 'prop', 'val', 'opt']):
		def dictraversal(d, path=None):
			path = path or []
			visited = []
			for key, val in d.items():
				if isinstance(val, dict):
					visited += dictraversal(val, path+[key])
				else:
					subpath = path + [key, val]
					visited.append(subpath)
			return visited
		return [dict(zip_longest(levelnames, r)) for r in dictraversal(interface)]


import sys
from PyQt5.QtWidgets import *
import win32com.client


class CpEvent:
    def set_params(self, client):
        self.client = client

    def OnReceived(self):
        code = self.client.GetHeaderValue(0)  # 종목코드
        name = self.client.GetHeaderValue(1)  # 
        timess = self.client.GetHeaderValue(18)  # 초
        exFlag = self.client.GetHeaderValue(19)  # 예상체결 플래그
        cprice = self.client.GetHeaderValue(13)  # 현재가
        diff = self.client.GetHeaderValue(2)  # 대비
        cVol = self.client.GetHeaderValue(17)  # 순간체결수량
        vol = self.client.GetHeaderValue(9)  # 거래량

        if (exFlag == ord('1')):  # 동시호가 시간 (예상체결)
            print("실시간(예상체결)", name, timess, "*", cprice, "대비", diff, "체결량", cVol, "거래량", vol)
        elif (exFlag == ord('2')):  # 장중(체결)
            print("실시간(장중 체결)", name, timess, cprice, "대비", diff, "체결량", cVol, "거래량", vol)


class CpStockCur:
    def Subscribe(self, code):
        self.objStockCur = win32com.client.Dispatch("DsCbo1.StockCur")
        handler = win32com.client.WithEvents(self.objStockCur, CpEvent)
        self.objStockCur.SetInputValue(0, code)
        handler.set_params(self.objStockCur)
        self.objStockCur.Subscribe()

    def Unsubscribe(self):
        self.objStockCur.Unsubscribe()





class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PLUS API TEST")
        self.setGeometry(300, 300, 300, 150)
        self.isSB = False
        self.objStockCur1 = CpStockCur()
        self.objStockCur2 = CpStockCur()
        self.objStockCur3 = CpStockCur()

        btnStart = QPushButton("요청 시작", self)
        btnStart.move(20, 20)
        btnStart.clicked.connect(self.btnStart_clicked)

        btnStop = QPushButton("요청 종료", self)
        btnStop.move(20, 70)
        btnStop.clicked.connect(self.btnStop_clicked)

        btnExit = QPushButton("종료", self)
        btnExit.move(20, 120)
        btnExit.clicked.connect(self.btnExit_clicked)

    def StopSubscribe(self):
        print('요청종료')
        if self.isSB:
            self.objStockCur1.Unsubscribe()
            self.objStockCur2.Unsubscribe()
            self.objStockCur3.Unsubscribe()

        self.isSB = False

    def btnStart_clicked(self):
        self.objStockCur1.Subscribe("A003540") # 대신증권
        self.objStockCur2.Subscribe("A000660") # 하이닉스
        self.objStockCur3.Subscribe("A005930") # 삼성전자

        print("-------------------")
        print("실시간 현재가 요청 시작")
        self.isSB = True

    def btnStop_clicked(self):
        self.StopSubscribe()


    def btnExit_clicked(self):
        self.StopSubscribe()
        exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()