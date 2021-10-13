# Analyzing Traffic With Pi-Hole and Proxifier.

Proxifier showed me the currently active connections that applications were running in the background, and what applications were responsible. It made me learn more about my applications since I looked them up online, and if I didn't need those connections I would block them.

With pihole I had a lot more control to learn about what domains can be commonly found when I am web browsing, and what they were doing. I am familiar with many of these domains now. I purposely implemented a strict policy on my pihole, making it block 5 million domains by default, just so I would be forced to learn what each domain was doing, why they were blocked, and what features would it be breaking.

If you are not familiar with Pi-Hole and Proxifier, here's how they look like:

These are all the addresses that had been resolved by my local dns resolver. It also shows if these addresses have been blocked or allowed

![Pi-Hole Query log](/assets/blog image/Pi-Hole Query Log.png)

Proxifier shows all the active connections on my computer, and also maintains a log of every connection that has been done previously. It's very useful

![Proxifier interface](/assets/blog image/Proxifier Interface.png)
