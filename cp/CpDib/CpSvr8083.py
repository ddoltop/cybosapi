from cp.core.cporm import Cporm


DESCRIPTION = {
    'summary': '종류별 체결강도 8081',
    'point': '''
    - 8081, 8082,8083이 유사해서, 사용을 위해그 차이 정도를  숙지 
  - 8083은 요청하는 최근  몇 개의 분 데이티를 받아오는 것에 특화. 
  -CpSvr8083.GetDataValue가 뱉어내는 값이 일별로 설명되고 있는데,
   원래 취지에 맞게 분 갯수별로 뱉어내는지는 실시간으로 찍어 봐야 함.(가령 5일->5개봉인지? ) 
  
          통신방식        연속여부  특성
    8081 Request/Reply    o   종목별 (실시간) 체결강도 
    8082 Request/Reply    x   종목별/업종별 일별 체결강도 
  - 8083 Request/Reply    x   종목별/업종별 시간대별 체결강도 (최대 360분) 

    통신종류 
        Request/Reply
 
CpSvr8083.SetInputValue(type,value)
  type: 입력 데이터 종류
0 - (string)  종목/업종/선물 코드
1 - (char)  최근분수 구분 
  '1' 30개 최근분/'2' 60개 최근분/'3' 150개 최근분/'4' 360개 최근분
 
value = CpSvr8083.GetHeaderValue(type)
type: 데이터 종류
  0 - (short) 수신개수

value = CpSvr8083.GetDataValue (Type,index)
  type: 데이터 종류
0 - (long) 시간
1 - (float) 체결강도(%) 1일
2 - (float) 체결강도(%) 5일
3 - (float) 체결강도(%) 20일
4 - (float) 체결강도(%) 60일
5 - (long,float) 주가(종목 코드인 경우 long,업종 코드와 선물인 경우 float)
6 - (long,float) 전일대비(종목 코드인 경우 long,업종 코드와 선물인 경우 float)
7 - (float) 전일 대비율
8 - (long) 거래량
''' ,

    'default': [
        '종목업종명', '시간','1체결강도', '5체결강도', '20체결강도', '60체결강도', '주가', '전일대비율','전일대비','거래량'
    ]
}


MODULE_NAME = 'dscbo1.CpSvr8083'


METHODS_INTERFACES = {

    'SetInputValue': {
        'code': {
            'position': 0,
            'type': ['str'],
            'essential': True,
        },
        'recent_minutes': {
            'position': 1,
            'type': ['char'],
            'essential': True,
            'options': {
              ord('1'): '30개의최근분수',
              ord('2'): '60개의최근분수',
              ord('3'): '150개의최근분수',
              ord('4'): '360개의최근분수',
            },
            'default': ord('1'),
        },
    },
    'GetHeaderValue': {
        'type': {
            'position': 0,
            'type': ['long'],
            'essential': True,
            'options': {
                0: '수신개수',
            },
        },
    },
    'GetDataValue': {
        'type': {
            'position': 0,
            'type': ['long'],
            'essential': True,
            'options': {
                0: '시간',
                1: '체결강도(%)1일',
                2: '체결강도(%)5일',
                3: '체결강도(%)20일',
                4: '체결강도(%)60일',
                5: '주가',
                6: '전일대비',
                7: '전일대비율',
                8: '거래량',
            },
        },
        'index': {
            'position': 1,
            'type': ['long'],
            'essential': True,
        },
    },  
}

def get_cpsvr8083(fields, **kwargs):
    '''종목/업종별 일별 체결강도 데이터를 요청하고 수신한다.
    r = get_cpsvr8082(
      code='A093640', # 종목코드 or 업종코드
      recent_days='60개*', # 최근일수 구분:[20*, 60*, 120*]
      fields = ['일자', '체결*', '주가', '전일*', '거래량']
    )
    '''
    crm = Cporm(MODULE_NAME, METHODS_INTERFACES)
    crm.set_inputvalues(**kwargs)
    crm.blockrequest()
    ordered_fields = crm.get_ordered_fields('GetDataValue', option='type', fields=fields)
    records = crm.get_datavalue_table(ordered_fields)
    for row in records:
        row['code'] = kwargs.get('code')
    return records




