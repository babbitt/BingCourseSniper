# BingCourseSniper

(Thanks to [Henry](https://github.com/HenryBurns) for the original inspiration & code [@HenryBurns/CoRE_project](https://github.com/HenryBurns/CoRE_project))

Sometimes a course is full without a waitlist, you know they'll be more spots, but you want to make sure you're the first to get them.

### What it does
CourseSniper polls Binghamton's servers every 30-60 seconds at random to see if the courses you requested are open. If they are, it launches a browser and registers you for them.

### Installation
*Note you must use Python 3.6+ in order for notifications to work*
1. Clone the repo  
```$ git clone https://github.com/babbitt/BingCourseSniper.git``` 
2. `cd` into the repo  
```$ cd BingCourseSniper```
3. install dependencies  
```$ pip3 install -r requirements.txt```
3. run the script  
```$ python3 sniper.py Season CRNs [CRNs ...] PODSuser PODSpass --flags```

##### Help
```
positional arguments:
Season                ["fall", "winter", "spring", "summer"]
CRNs                  A CRN to be registered (int)
PODSuser              Your PODS id / username (str)
PODSpass              Your PODS passsword (str)

optional arguments:
-h, --help                      show this help message and exit
--notify_run                    Use Notify.run for notificaitons (just flag)
--push_bullet PUSH_BULLET       Use PushBullet for notifications - API key (str)
```

##### Examples
This is the simplest form of the program run for the fall semester with CRN 123  
`python3 sniper.py 'fall' 123 'jdoe1' 'password'`

Now with multiple CRNs (123 & 456)  
`python3 sniper.py 'fall' 123 456 'jdoe1' 'password'`

Now with Notify.run notifications (This will allow you to keep up to date on another device with the status)  
`python3 sniper.py 'fall' 123 456 'jdoe1' 'password' --notify_run`

And finally with PushBullet notifications instead of Notify.run  
`python3 sniper.py 'fall' 123 456 'jdoe1' 'password' --push_bullet 'myAPIkey'`
