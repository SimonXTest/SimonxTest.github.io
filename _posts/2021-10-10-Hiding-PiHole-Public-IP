# Hiding The IP Address of my Pi-Hole Device

Websites were able to see my dns address, which was the public ip address of my home network (this can be seen in https://www.dnsleaktest.com). This allows anyone to know that I am using a local dns resolver, they would know my address, and my ip address would leak while using a vpn or a proxy from my router. Bad actors would have enough info to consider me a target. Hiding the ip address of my dns is important, I used a vpn to accomplish this. After installing the vpn, I had to circumvent the dns protection provided by my vpn, which forces dns requests to be handled by the vpn servers. This prevents my dns server from running properly. The dns address was being switched constantly between the vpn's and the local dns resolver.

To solve this I found the location of every configuration file, changed them manually, and then made them read only. Because I was not familiar with Linux, I had to browse the internet to find the location of these files.

I knew this was successful, because on my pihole machine I can use the command "curl ifconfig.me" to see that my ip is different from the one given by my isp. I also know this because if I use a device that uses my dns, and go to https://www.dnsleaktest.com, I can see that the ip address of my dns is different and it's on a different location.

I can tell you I don't live in Norway, and I don't have a giant wireless network that goes from the US to Norway.

[Image of DNS leak test results.](/assets/blog image/Successful DNS Leak Result.png)
