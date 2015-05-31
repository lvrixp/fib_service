# Test Scenario #

## Functional Test on server side##

#### Frontend ####

    1.Test Route, Only fib, fib/ or fib/integer is acceptable.
    2.URI is fib/negativeInteger, should report 400 Bad Request.
  
#### Backend ####
	
	1.Serialize array to Json payload.
    2.Serialize to error payload.
    
## Integration Test ##

	Server's frontend access backend.

    1.Create a task to thread pool. wait for the event to complete. Get correct string.    
    2.More than one task at the same time.
    3.More than the concurrence thread limit. All tasks should be correctly handled.
    
## End To End Test ##
This part is mainly focus on the E2E scenario which means the round from the browser to the server and back to the browser.

**Positive**

        Http://hostname:port/fib
        Http://hostname:port/fib/
        Expected: 200 OK 
        { Hello, world! }

	    Http://hostname:port/fib/0
	    Http://hostname:port/fib/1234
	    http://hostname:port/fib/12344556678
	    http://hostname:port/fib/25?$a=b
	        Note: Query option will be ignored
	    
	    Expected: 200 OK (JSON payload)
	    { N: inputNumber, Result: [expected array] }

**Negative**

        Input: http://hostname:port/fib/1/
	    Input: http://hostname:port/fib/-1
	    Input: http://hostname:port/fib/letter
	    Input: http://hostname:port/fib/+testa
	    Input: http://hostname:port/fib/ space
	    Input: http://hostname:port/fib/escaptedCharaters.
	
	    Expected: 400 Bad Request

### Performance Test ###

    1.Test 10 mins, and given the expected user number (threads) and normal input. Test how long the service handle a request, and how about the memory and CPU
    2.Test 10 mins, and given the expected user number (threads) and very big input. Test how long the service handle a request, and how about the memory and CPU.
    Check whether there is memeory leak.
    
### Stress Test ###
    1. Let the Usage 80%, Run for 5 mins, Test how many request can be handled per second.
    2. Let the Usage 80%, Run for 5 mins, given very big input. Test how many request can be handled per second.
    