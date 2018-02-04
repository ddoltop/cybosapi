
DESCRIPTION = {
	'summary': '입력한 종목 기관매매누적과 외인순매수',
	'point': '''
	  - 수급분석의 기본 자료로서 중요. 
	    특정 종목을 특정세력이 최대매수하거나 최대매도 했던 누적치를 기준으로 
	    최근 개인 누적치와 비교해서 분산패턴 산출 
	  - 다만 실시간 아닌 장 종료후 만 확정치를 제공하는 데이터임.(장중 3-4회 잠정치. 확정과 오차있음.)  
	  - 가급적 5년이상의 일별 누적데이터를 필요로 함.   
	  - 앞서 CpSvrNew7216은 기관과 외인계의 경향만을 보여줌.   

	통신종류 
 		Request/Reply
 
	CpSvrNew7254.SetInputValue(type,value)
	
		0 - (string) 종목코드
		1 - (short) 기간선택구분 (0:사용자지정 1:1개,월, 2:2개월 3:3개월 4:6개월,5:최근5일 6:일별)
		2 - (long)  시작일자: 기간선택구분을 0이 아닐경우 생략
		3 - (long)  끝일자: 기간선택구분을 0이 아닐경우 생략
		4 - (char)  매매비중구분
			'0' 순매수 /'1'  매매비중
		5 - (short)  투자자
			0 전체, 1 개인,2 외국인,3 기관계,4 금융투자,5 보험,6 투신,7 은행
			8 기타금융,9 연기금,10 국가지자체,11 기타외인,12 사모펀드,13 기타법인
 
value = CpSvrNew7254.GetHeaderValue(type)
       type: 데이터 종류 0 - (string) 종목코드
					  1 - (long)  총데이터건수

	value = CpSvrNew7254.GetDataValue(Type,Index)
        type: 0 전체 투자자별 데이터로..
        Index: 	0 - (long) 일자
				9 - (long) 일별순매수수량
				10 - (long) 일별순매수금액(백만)
		 
''',    
    'default': [
		'종목코드', '일자', '개인', '외국인', '기관계', '금융투자', '보험', '투신', '은행'
		'기타금융', '연기금', '국가지자체', '기타외인', '사모펀드', '기타법인','일별순매수수량','일별순매수금액'
	]

}

