xs2kn='eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI4TEFKRzkiLCJqdGkiOiI2NzU2NTc2NjQ5OTlkYTI5YTMwNDcyZGQiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzMzNzExNzE4LCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzM3ODE2MDB9.m2QP1eoft5HzhlCcn-4POb51lQdMtk8QPSUFc-XGPo4'

isin='NSE_EQ|INE248A01017'

NOS=1


slp_tm=30      #sleep time                                                          ###############################################################################
    

def buy():
    import upstox_client
    from upstox_client.rest import ApiException
    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn
    api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
    body = upstox_client.PlaceOrderRequest(NOS, "I", "IOC", 0.0, "string", isin, "MARKET", "BUY", 0, 0.0, False)
    api_version = '2.0'
    try:
        api_response = api_instance.place_order(body, api_version)
        print(api_response)
        if api_response.status=='success':
            os=orderstatus(api_response.data.order_id)
            return (os,os.data.status)
            
    except Exception as e:
        print("Exception %s\n" % e.body)

def sell():
    import upstox_client
    from upstox_client.rest import ApiException
    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn
    api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
    body = upstox_client.PlaceOrderRequest(NOS, "I", "IOC", 0.0, "string", isin, "MARKET", "SELL", 0, 0.0, False)
    api_version = '2.0'
    try:
        api_response = api_instance.place_order(body, api_version)
        print(api_response)
        if api_response.status=='success':
            os=orderstatus(api_response.data.order_id)
            return (os,os.data.status)
            
    except Exception as e:
        print("Exception %s\n" % e.body)

if __name__ == '__main__':
    #historical_data()
    #data_save()
    #print(name(isin))
    #dadw()
    #alpha_hunt()
    #buy()
    #sell()
    pass
