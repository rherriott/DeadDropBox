# DeadDropBox
A timelocked safe for data

Important: I removed multihreading, but even if I hadn't, making the thread number the filename isn't trustowrthy

TODO:
 - Take command line arguments (it currently takes host/port but not email)
 - Email retreival (implemented in lib, just needs to be used)
 - Fix pile of security holes
 - Test on different machines
 - Implement delay on resend (implemented in lib, just needs to be used)
 - Device pickup if client thread dies?
 - Sleep
 - Access data in a file, instead of a string literal (I genuinely doubt we're goingto do better than byte arrays)

Notes: Please try to standardize on using bytearrays and not strings to ensure no weirdness happens with formatting. It's probably fine but if it's ever not it will mess with things in wierd ways - all this "latin-1" stuff makes me nervous
