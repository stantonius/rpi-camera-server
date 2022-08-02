# Camera Client

Code that receives the video transmission.

Most of the code examples comes from the awesome [imagezmq package](https://github.com/jeffbass/imagezmq)

## Background and Context

This code sits on my home lab server, which is a Proxmox server. This setup means I have flexibility - I am usuing a Raspberry Pi 4 8GB as the home security camera, which is probably overkill but it means I can do a fair amount of processing on that device. I also have a powerful server that can do heavy-duty image manipulation and inferencing.

## Objective

This code needs to do 3 things:
* Receive images to store
* Be able to process images
* Serve live viewing as a webserver (but only when called upon)

