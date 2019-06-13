# DeadDropBox
A timelocked safe for data

Important: I removed multihreading, but even if I hadn't, making the thread number the filename isn't trustowrthy

TODO:
 - Take command line arguments (it currently takes host/port but not email)
 - Security checkup
 - Test on additional platforms
 - Check function with long delays
 - Device pickup if client thread dies

Notes: Please try to standardize on using bytearrays and not strings to ensure no weirdness happens with formatting. It's probably fine but if it's ever not it will mess with things in wierd ways - all this "latin-1" stuff makes me nervous
