
DESCRIPTION = {
	'summary': '복수 종목 조회 7059',
	'point': '''
	- 해당 종목들의 현재가 매수도호가 상한 하한 값 등을 미리 계산 해줌
    -다수의 종목코드를 110개까지 입력해 값을 받아 올 수 있습니다. 

	통신종류 
 		Request/Reply
 
	Mstm.SetInputValue(type,value)
	  0 - (string) 다수의 종목코드
      ex) A003540A000060A000010 (MAX:110개)

	value = MstM.GetHeaderValue(type)
	   type에 해당하는 헤더 데이터를 반환합니다
       type: 데이터 종류
       0 - (short) count
       반환값: 데이터 종류에 해당하는 값

	value = MstM.GetDataValue(Type,Index)
		
		 type 설명 
		  
        -예상체결가는 말 그대로 장 시작전 매수매도 추이로 장 개시시 시작가 예측가격임.
         예상체결가는 장 직전 몇초가 실제 장시가로 이어지며,  
          그 자체로 눈속임이 있을 수 있으니 참고 외에 쓰지 않는게 좋음.
        
        -매수 매도에 의한  주가 체결이 없는 경우는 현재가가 없으므로, 
         전일 가격에 비해 매수호가가 높으면 기세상승,
                      매도호가가 낮으면 기세하락, 
         매수하겠다는 가격이 상한가에 있으면 기세상한,
         반대로 매도하겠다는 가격이 하한가에 있으면 기세하한.
         그런데 이런 경우는 거의 없습니다.  

'''    
    'default': [
		'종목코드', '종목명', '대비', '현재가', '매도호가', '매수호가', '거래량'
	]

}

