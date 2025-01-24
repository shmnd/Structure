class ResponseInfo(object):
    def __init__(self,user=None,**args):
        self.response ={
            'status': args.get('status',True),
            'message': args.get('message',''),
            'status_code': args.get('status_code',200),
            'data': args.get('data',{}),
            'erros': args.get('errors',{})
        }
        

