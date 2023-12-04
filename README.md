<div id="top"></div>

<br />
<div align="center">
  <a href="https://github.com/j0naslarss0n/iotCloudSolution">
    <img src="assets/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">IoT and AWS Cloud services</h3>

  <p align="left">
I chose to use the my old trusted Raspberry Pi3 and a tmperature sensor. Since this was more about learning the cloud solutions from AWS, my primary concern wasn't so much the data itself. However I found it intriguing to benchmark the the official temperatures from SMHI(Swedish weather institute) at Bromma airport, not far from where I live, about 6 km. The result was quite fascinating, that the graphs may show. 
    <br />
    
  </p>
</div>


<h2 align="center">Solution and flowchart</h3>
 <div align="center">
  <a>
    <img src="assets/flowchart_jonaslarsson.drawio.png" alt="flowchart, with sensor and API on left trough a AWS solution nad gadgets and presentation on right" width="" height="">
  </a>

</div>


<h2 align="center">Hardware</h3>
<div>
<p align="left">
 <ul>
  <li>Raspberry Pi3</li>
  <li>Temperature sensor DS18B20 </li>
  <li>Cables and breadbord</li>
</ul> 
</div>



<h2 align="center">Software and tools</h3>
<div>
<p align="left">
 <ul>
  <li>AWS</li>
   <ul>
  <li>Lambda</li>
    <li>DynamoDB</li>
    <li>Eventbridge</li>
    <li>IoT Core</li>
    <li>S3</li>
    <li>API Gateway</li>
  </ul>
  <li>Rasbian OS </li>
  <li>Draw.io</li>
  <li>Python</li>
  <li>Node.js</li>

</ul> 
</div>



<h2 align="center">Setup Raspberry Pi3 </h3>
<div>
<p align="left">
  I set up the Raspberry Pi 3B with Rasbian OS, install is quite straight forward with Raspberrys own installation tool and there are several settings for Wifi-connection and SSH from get go. With SSH it was easy to access the Raspberry and prepare it to send data.
  As always update the software on a new install
  
  ``` 
  sudo apt update && sudo apt dist-upgrade
  ```   
  I used python for the script on the Raspberry to publish my data, to do so I needed to install dependenicies to communicate with AWS using MQTT, these are installed with pip so first install that.
  ```
  sudo apt install pip
  ```
  then install dependencies for AWS IoT.
  
  ```
  sudo apt install pip3-AWSIoTPythonSDK
  ```

  I found <a href="https://circuitdigest.com/microcontroller-projects/publish-sensor-data-to-amazon-aws-raspberry-pi-iot">this</a> walkthrough which was handy and had a neat setup for the certificates and access keys. Instead of a 'copy-paste-document' I could use the whole folder from AWS and referens to the documents in the folder. This could be good if there would be many IoThings in a IoT-solution.

  ```
  jonas@raspberrypi:~/aws_temp $ tree
.
├── RPi3_policy
│   ├── f44f4106df9/.../dsa32h8179-certificate.pem.crt
│   ├── 201f44f4106df/.../8134fsasdkk279-private.pem.key
│   ├── 1f44f4106df9/.../esd982dase8928179-public.pem.key
│   ├── AmazonRootCA1.pem
│   └── AmazonRootCA3.pem
└── temp_pub.py

2 directories, 6 files

  ```

</p>

</div>




## Security

Ceritficates
Policys


## Scalability

## Thoughts and prayers.
