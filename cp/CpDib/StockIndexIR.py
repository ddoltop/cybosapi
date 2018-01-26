
DESCRIPTION = {
	'summary': '업종 코드에 관한 데이터(지수,업종명,거래량,거래 대금)을 1분 간격',
	'point': '''

	-업종의 지수 거래대금 등을 보여줌. 
	-업종을 따로 만들어 정리한다면 불필요 할 수도 있으나,
	  전체 업종의 흐름을 파악하는 도구로는 활용 가능 .
		
통신종류 
 	Request/Reply
 
StockIndexIR.SetInputValue(type,value)
	0 - (string) 업종 코드


value = StockIndexIR.GetHeaderValue(type)
	type: 1 - (long) 수신개수  2 - (string) 업종 코드


value = StockIndexIR.GetDataValue (Type,index)
	type: 데이터 종류

0 - (long) 시간
1 - (float) 지수
2 - (float) 전일대비
3 - (long) 거래량. [주의] 단위가 일입니다 
4 - (long) 거래대금. [주의] 단위가 백만입니다



 ''',

'default': [
		'업종명', '지수', '전일대비', '거래량', '거래대금'
	]

    
	
}

