# make a class for upstox and another for kotak. kotak one do it later
xs2kn='eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI4TEFKRzkiLCJqdGkiOiI2NzdiMjc3OTk2MGY1NDEwOTY3MDMwZDciLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzM2MTI0MjgxLCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzYyMDA4MDB9.S1t9k9LS0JKTG3OgL5ytJzUepFJsU8G-wMadZC-zatM'



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

print(get_valid_symbols_from_list( ['NSE_EQ|INE669E01016','NSE_EQ|INE848E01016',' NSE_EQ|INE00H001014']))
    





class upstox:

    #isin_list = 'NSE_EQ|INE669E01016,NSE_EQ|INE848E01016'   
    def full_market_quote_multiple_instrument(isin_list):        #fmq_mik
        import upstox_client
        from upstox_client.rest import ApiException

        configuration = upstox_client.Configuration()
        configuration.access_token = xs2kn
        api_version = '2.0'

        
        api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))

        try:
            api_response = api_instance.get_full_market_quote(isin_list, api_version)
            print(api_response)
            
        except ApiException as e:
            print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)



    def ful_mar_quo(xs2kn,isin):            ### return full market quote
        import time
        import upstox_client
        from upstox_client.rest import ApiException

        configuration = upstox_client.Configuration()
        configuration.access_token = xs2kn
        api_version = '2.0'
        api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))
        while True:
            try:
                api_response = api_instance.get_full_market_quote(isin, api_version)
                if api_response.status=='success':
                    return api_response
                #print(type(api_response))
                #print(datetime.datetime.now())
            except Exception as e:
                print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)
            time.sleep(10)

    
    def orderstatus(order):
        import upstox_client
        from upstox_client.rest import ApiException

        configuration = upstox_client.Configuration()
        configuration.access_token = xs2kn
        api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
        try:
            api_response = api_instance.get_order_status(order_id=order)
            return api_response
        except ApiException as e:
            print("Exception when calling OrderApi->get order status: %s\n" % e.body)

    def buy(order_type='I'):        #bring v3 version
        import upstox_client
        from upstox_client.rest import ApiException
        configuration = upstox_client.Configuration()
        configuration.access_token = xs2kn
        api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
        body = upstox_client.PlaceOrderRequest(NOS, order_type, "IOC", 0.0, "string", isin, "MARKET", "BUY", 0, 0.0, False)
        api_version = '2.0'
        try:
            api_response = api_instance.place_order(body, api_version)
            print(api_response)
            if api_response.status=='success':
                os=orderstatus(api_response.data.order_id)
                return (os,os.data.status)
                
        except Exception as e:
            print("Exception %s\n" % e.body)

    def sell(order_type='I'):
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
                os=orderstatus(api_response.data.order_id)
                return (os,os.data.status)
                
        except Exception as e:
            print("Exception %s\n" % e.body)

def buysell(intent,isin,NOS):
    global lastorder,investment_status
    import upstox_client
    from upstox_client.rest import ApiException
    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn
    api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
    if lastorder is not None:
        try:
            api_response = api_instance.get_order_status(order_id=lastorder)
            print(api_response)
            if api_response.status=='success':
                investment_status=lastorder_intent
                lastorder=None
        except ApiException as e:
            print("Exception when calling OrderApi->get order status: %s\n" % e.body)
    if lastorder is None and investment_status!=intent:
        if intent>investment_status:
            body=upstox_client.PlaceOrderRequest((intent-investment_status)*NOS, "I", "IOC", 0.0, "string", isin, "MARKET", "BUY", 0, 0.0, False)
            api_version = '2.0'
            try:
                api_response = api_instance.place_order(body, api_version)
                print(api_response)
                #if(api_response.status=='success'):
                #    lastorder=ap
                if api_response.status=='success':investment_status=intent
            except Exception as e:
                print("Exception when calling OrderApi->get order status: %s\n" % e.body)
        if intent<investment_status:
            body = upstox_client.PlaceOrderRequest((investment_status-intent)*NOS, "I", "IOC", 0.0, "string", isin, "MARKET", "SELL", 0, 0.0, False)
            api_version = '2.0'
            try:
                api_response = api_instance.place_order(body, api_version)
                print(api_response)
                if api_response.status=='success':investment_status=intent
            except Exception as e:
                print("Exception when calling OrderApi->get order status: %s\n" % e.body)

