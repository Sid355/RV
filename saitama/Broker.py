# make a class for upstox and another for kotak. kotak one do it later
xs2kn='eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI4TEFKRzkiLCJqdGkiOiI2N2E3MjY0MDBjYjlmZDY3NWRhYmQ5MTYiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzM5MDA3NTUyLCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzkwNTIwMDB9.szJIcP05vtZrIZDQBbAbPNycIlgFBz2P073-QHtDJ6U'


broker='upstox'     # 'upstox' or 'kotak' 

#TODO make a list of isin and symbol. you only give numbers 1,2,5 to choose and it returns isin_list for fmq_mi




def get_valid_symbols_from_list(isin_list):
    """
    Fetch full market quotes for a list of ISIN symbols from Upstox,
    separating out the valid and invalid symbols based on the API response.

    :param isin_list: List of instrument symbols (e.g., 'NSE_EQ|INE669E01016')
    :param access_token: Your Upstox API access token
    :return: (valid_symbols_data, invalid_symbols_list)
        - valid_symbols_data: List of data dicts for each valid symbol
        - invalid_symbols_list: List of any symbols that returned errors
    """
    
    import upstox_client
    from upstox_client.rest import ApiException
    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn

    # Prepare symbols as a comma-separated string e.g. "NSE_EQ|INE669E01016,NSE_EQ|INE848E01016"
    symbols_str = ",".join(isin_list)

    api_instance = upstox_client.MarketQuoteApi(  upstox_client.ApiClient(configuration)   )

    valid_symbols_data = []
    invalid_symbols_list = []

    api_version = '2.0'

    try:
        api_response = api_instance.get_full_market_quote(symbols_str, api_version)

        if api_response.status == 'success':            # All requested symbols are valid
            valid_symbols_data = api_response.data

        elif api_response.status == 'partial_success':           # Some symbols are valid, others invalid
            if hasattr(api_response, 'data') and api_response.data:
                valid_symbols_data = api_response.data          #valid_symbols_data.extend(api_response.data)
            if hasattr(api_response, 'errors') and api_response.errors:
                for error in api_response.errors:
                    invalid_symbols_list.append(
                        error.get('symbol', 'Unknown Symbol')
                    )

        else:
            # status might be "error" or something else
            error_message = getattr(api_response, 'error', {}).get('message', 'Unknown error')
            print(f"Error fetching quotes: {error_message}")

    except ApiException as e:        # Catch any Upstox client exceptions
        print(f"API Exception occurred: {e}")

    # Return the valid data and list of invalid symbols
    return valid_symbols_data, invalid_symbols_list

    isin_symbols = [        'NSE_EQ|INE669E01016',       # Example valid
                           'NSE_EQ|INVALIDISIN12345'    # Example invalid 
    ]
    valid_data, invalid_symbols = get_valid_symbols_from_list(isin_symbols, access_token)
    print("\n=== Valid Symbols Data ===")
    for quote in valid_data:
        # Each quote is a dictionary with market data fields (symbol, last_price, change, etc.)
        print(f"Symbol: {quote['symbol']}")
        print(f"Last Price: {quote['last_price']}")
        print(f"Change: {quote['change']} ({quote['percent_change']}%)")
        print(f"Volume: {quote['volume']}")
        print("-" * 30)
    if invalid_symbols:
        print("\n=== Invalid Symbols ===")
        for sym in invalid_symbols:
            print(f"Invalid Symbol: {sym}")



#isin for which market quote is available
#fmq_avail_isin=  get_valid_symbols_from_list(isin_list)[0]

#print(get_valid_symbols_from_list( ['NSE_EQ|INE669E01016','NSE_EQ|INE848E01016',' NSE_EQ|INE00H001014']))
    



  


class upstox:
    
    def margin_details(isin,BoS,quantity=1,product='I'):         ######  BoS= 'BUY' or 'SELL'  
        import upstox_client
        from upstox_client.rest import ApiException

        configuration = upstox_client.Configuration()
        configuration.access_token = xs2kn
        api_instance = upstox_client.ChargeApi(upstox_client.ApiClient(configuration))
        instruments = [upstox_client.Instrument(isin,quantity,product,BoS)]
        margin_body = upstox_client.MarginRequest(instruments)
        try:
            api_response = api_instance.post_margin(margin_body)
            if api_response.status == 'success':
                print(api_response)
                return api_response
            else:
                print("Margin API returned a non-success status:", api_response.status)
                return None
        except ApiException as e:
            print("Exception when calling Margin API: %s\n" % e.body)
            return None

    def quant_purchasable(available_money,isin,BoS): 
        import math
        md= upstox.margin_details(isin,BoS)
        if md == None: return None
        each_share_need = md.data.required_margin
        qp = math.floor(available_money / each_share_need)          
        print(qp)  
        return qp


    def brokerage_details(isin,quantity,BoS,price,product='I'):         
        import upstox_client
        from upstox_client.rest import ApiException
        configuration = upstox_client.Configuration()
        configuration.access_token = xs2kn
        api_version = '2.0'
        api_instance = upstox_client.ChargeApi(upstox_client.ApiClient(configuration))

        try:
            # Brokerage details
            api_response = api_instance.get_brokerage(isin, quantity, product, BoS, price, api_version)
            print(api_response)
            return(api_response)
        except ApiException as e:
            print("Exception when calling ChargeApi->get_brokerage: %s\n" % e)
            return(None)



    
    def full_market_quote_multiple_instrument(isin_list):        #fmq_mik
        #isin_list = 'NSE_EQ|INE669E01016,NSE_EQ|INE848E01016'   
        import upstox_client
        from upstox_client.rest import ApiException

        configuration = upstox_client.Configuration()
        configuration.access_token = xs2kn
        api_version = '2.0'
        api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))

        try:
            api_response = api_instance.get_full_market_quote(isin_list, api_version)
            print(api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)
            return None


    def ful_mar_quo(isin):            ### return full market quote
        import upstox_client
        from upstox_client.rest import ApiException

        configuration = upstox_client.Configuration()
        configuration.access_token = xs2kn
        api_version = '2.0'
        api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))

        try:
            api_response = api_instance.get_full_market_quote(isin, api_version)
            if api_response.status=='success':
                return api_response
            #print(type(api_response))
            #print(datetime.datetime.now())
        except Exception as e:
            print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)
            return None

        
    def name(isin):               ### It will give the name of any given isin but using xs2kn
        import upstox_client
        from upstox_client.rest import ApiException

        configuration = upstox_client.Configuration()
        configuration.access_token = xs2kn
        api_version = '2.0'
        api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))
        try:
            api_response = api_instance.get_full_market_quote(isin, api_version)
            #print(type(api_response))
            #print(datetime.datetime.now())
            return api_response.data[next(iter(api_response.data))].symbol
        except Exception as e:
            print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)
        
    def intraday_candle_data(isin):
        import upstox_client
        from upstox_client.rest import ApiException
        api_version = '2.0'
        api_instance = upstox_client.HistoryApi()
        interval = '1minute'
        try:
            api_response = api_instance.get_intra_day_candle_data(isin,interval,api_version)
            #cleprint(api_response)
            return api_response
        except ApiException as e:
            print(f"Exception when calling HistoryApi->get_intra_day_candle_data for ISIN {isin}: {e}")
            return None

    def orderstatus(order_id):
        import upstox_client
        from upstox_client.rest import ApiException

        configuration = upstox_client.Configuration()
        configuration.access_token = xs2kn
        api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
        try:
            api_response = api_instance.get_order_status(order_id= order_id)
            print(api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling OrderApi->get order status: %s\n" % e.body)
            return None

    def buy(NOS,isin,order_type='I'):        #bring v3 version
        import upstox_client
        from upstox_client.rest import ApiException
        configuration = upstox_client.Configuration()
        configuration.access_token = xs2kn
        api_version = '2.0'
        api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
        
        body = upstox_client.PlaceOrderRequest(NOS, order_type, "IOC", 0.0, "string", isin, "MARKET", "BUY", 0, 0.0, False)
        
        try:
            api_response = api_instance.place_order(body, api_version)
            print(api_response)
            if api_response.status=='success':
                print(f'Pb-Cu-Db-Order Executed.{api_response}')                     ### just to check execution time difference
                os=upstox.orderstatus(api_response.data.order_id)
                print('order_status: ',os)
                if os.data.status == 'complete':
                    return True, 1, os.data.average_price
        except Exception as e:
            print("Exception %s\n" % e.body)
            return False, None, None

    def sell(NOS,isin,order_type='I'):
        import upstox_client
        from upstox_client.rest import ApiException
        configuration = upstox_client.Configuration()
        configuration.access_token = xs2kn
        api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))

        body = upstox_client.PlaceOrderRequest(NOS, order_type, "IOC", 0.0, "string", isin, "MARKET", "SELL", 0, 0.0, False)
        api_version = '2.0'
        try:
            api_response = api_instance.place_order(body, api_version)
            print(api_response)
            if api_response.status=='success':
                print(f'Pb-Cu-Db-Order Executed.{api_response}')                     ### just to check execution time difference
                os=upstox.orderstatus(api_response.data.order_id)
                print('order_status: ',os)
                if os.data.status == 'complete':
                    return True, -1, os.data.average_price    
        except Exception as e:
            print("Exception %s\n" % e.body)
            return False, None, None

    def buysell(inv_status,intent,isin,NOS):             ### execute intent order. If order executed successfully then return True
        import upstox_client
        from upstox_client.rest import ApiException
        configuration = upstox_client.Configuration()
        configuration.access_token = xs2kn
        api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
        api_version = '2.0'

        if intent > inv_status:    
            body=upstox_client.PlaceOrderRequest((intent-inv_status)*NOS, "I", "IOC", 0.0, "string", isin, "MARKET", "BUY", 0, 0.0, False)
            try:
                api_response = api_instance.place_order(body, api_version)
                print(api_response)
                if api_response.status == 'success': 
                    print(f'Pb-Cu-Db-Order Executed.{api_response}')                     ### just to check execution time difference
                    gen=upstox.orderstatus(api_response.data.order_id)
                    print('gen',gen)
                    if gen.data.status == 'complete':
                        return True, gen.data.price     ###   previously inplace of return we were simply making   inv_status = intent
            except Exception as e:
                print("Exception when calling OrderApi->get order status: %s\n" % e.body)
                return None, None

        if intent < inv_status:
            body = upstox_client.PlaceOrderRequest((inv_status-intent)*NOS, "I", "IOC", 0.0, "string", isin, "MARKET", "SELL", 0, 0.0, False)
            try:
                api_response = api_instance.place_order(body, api_version)
                print(api_response)
                if api_response.status == 'success': 
                    print(f'Pb-Cu-Db-Order Executed.{api_response}')                    ### just to check execution time difference
                    gen=upstox.orderstatus(api_response.data.order_id)
                    print('gen',gen)
                    if gen.data.status == 'complete':
                        return True, gen.data.price     ###   previously inplace of return we were simply making   inv_status = intent
            except Exception as e:
                print("Exception when calling OrderApi->get order status: %s\n" % e.body)
                return None, None


isin_map = {
    1: ("ITI",         "NSE_EQ|INE248A01017"),
    2: ("MOBIKWIK",    "NSE_EQ|INE0HLU01028"),
    3: ("TATAMOTORS",  "NSE_EQ|INE155A01022"),
    4: ("SWIGGY",      "NSE_EQ|INE00H001014"),
    5: ("OLAELEC",     "NSE_EQ|INE0LXG01040"),
    6: ("ADANIGREEN",  "NSE_EQ|INE364U01010"),
    7: ("ADANIPOWER",  "NSE_EQ|INE814H01011"),
    8: ("PAYTM",       "NSE_EQ|INE982J01020"),
    9: ("HAL",         "NSE_EQ|INE066F01020"),
    10:("HINDALCO",    "NSE_EQ|INE038A01020"),
    11:("ITC",         "NSE_EQ|INE154A01025"),
}

isin_quest=6
isin=isin_map.get(isin_quest)[1]


if __name__ == '__main__':
        
    PTR=   4

    if PTR==0:  pass
    if PTR==1:  print(upstox.buy(1,isin))
    if PTR==2:  print(upstox.sell(1,isin_map.get(isin_quest)[1]))
    if PTR==3:  upstox.buysell #fill detail
    if PTR==4:  print(upstox.ful_mar_quo(isin_map.get(9)[1]))
    if PTR==5:  print(upstox.intraday_candle_data(isin_map.get(5)[1]) , isin_map.get(5)[0])
    if PTR==6:  print(upstox.ful_mar_quo( isin_map.get(isin_quest)[1] ) , isin_map.get(isin_quest)[0] )
    if PTR==7:  upstox.brokerage_details(isin,200,'SELL',969)        
    if PTR==8:  upstox.margin_details(isin,'BUY') 
    if PTR==9:  upstox.quant_purchasable(1000,isin,'SELL')
    if PTR==10: upstox.orderstatus(250205025306147)
