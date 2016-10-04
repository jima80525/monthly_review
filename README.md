Monthly Remember The Milk Review
=======
Python script to display the last 30 days of completed tasks from Remember The
Milk.  This is heavily based on an example script provided with the RtmAPI
package.

It requires at least two environment variables to be set:
* API_KEY
* SHARED_SECRET

Optionally (ok, most of the time you want this after the initial setup) you can
set:
* TOKEN

Once the env variables are set, simply run it as
```
./monthly_review.py
```

Note that you might want to pipe it to a file or through less:

```
./monthly_review.py > my_tasks.txt
./monthly_review.py | less
```


Thanks to Michael Gruenewald and Marcin Kasperski for the RtmAPI package!
