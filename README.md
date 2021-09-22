# Mounting Containers and Volumes  
This project scrapes data of stocks and feeds them down a pipeline that trains an ML model and displays a dashboard using Streamlit. This application is then containerized using docker and deployed to a virtual machine on AWS using EC2. This instance is then accessed from a custom domain name that is being hosted on a Cloudflare DNS server. The major problem within this project was the complex nature resulting from a high number of composition files. Due to the uniqueness of the deployment I found no insight from research and ultimately performed brute force through experimentation to reach a solution.  

> allowing for data persistence between enviorments 

- CI / CX
- Docker
- Time Series Analysis
- ML Dashboards
- AWS 
