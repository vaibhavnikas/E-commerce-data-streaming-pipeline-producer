<h1 align="center">Introduction</h1>

<p>This repository is part of <b>Realtime E-commerce BI Dashboard</b> project. This project is divided into 3 repositories :</p>

<ul>
<li><a href="https://github.com/vaibhavnikas/E-commerce-data-streaming-pipeline-producer">E-commerce-data-streaming-pipeline-producer</a></li>
<li><a href="https://github.com/vaibhavnikas/E-commerce-data-streaming-pipeline-consumer">E-commerce-data-streaming-pipeline-consumer</a></li>
<li><a href="https://github.com/vaibhavnikas/Realtime-Ecommerce-BI-Dashboard">Realtime-Ecommerce-BI-Dashboard</a></li>
</ul>

<p>The <a href="https://github.com/vaibhavnikas/E-commerce-data-streaming-pipeline-producer">E-commerce-data-streaming-pipeline-producer</a> repo acts as the source system. It generates e-commerce transaction data and produces it to a Kafka topic: <b>e-commerce-transactions</b>.</p>
<p>The <a href="https://github.com/vaibhavnikas/E-commerce-data-streaming-pipeline-consumer">E-commerce-data-streaming-pipeline-consumer</a> processes transaction data from the Kafka topic and ingests it into the <b>fact_transaction</b> table within the PostgreSQL-based sales data warehouse.</p>
<p>The <a href="https://github.com/vaibhavnikas/Realtime-Ecommerce-BI-Dashboard">Realtime-Ecommerce-BI-Dashboard</a> reads data from the sales datawarehouse and displays realtime business insights onto the BI dashboard.</p>

<h2 align="center">E-commerce-data-streaming-pipeline-producer</h2>
<p>This repo contains 2 scripts : <li>data_generator.py</li> <li>ecommerce_transaction_producer.py</li></p>
<p>The <b>data_generator.py</b> script generates dummy customers, locations, categories and products data for the e-commerce data platform and stores the data in csv format. This data is ingested into the dim_customer, dim_location, dim_category and dim_product dimension tables of the sales data warehouse. This data is used by the ecommerce_transaction_producer.py script to generate e-commerce transactions.</p>
<p>To simulate e-commerce transactions, <b>ecommerce_transaction_producer.py</b> randomly selects a customer, location and products in each iteration to generate e-commerce transaction and produces this transaction data to <b>e-commerce-transactions</b> Kafka topic. This data is consumed by the downstream consumer and ingested into a sales data warehouse.</p>

<h3>Technologies Used</h3>
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
<img src="https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white">
<img src="https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white">

<h3>Installation</h3>
<ol>
<li>Clone this repository on your system.</li>
<li>Create a .env file and add the credentials mentioned in .env.example in .env file.</li>
<li>Run <b>pip install -r requirements.txt</b> to install project dependencies.</li>
<li>Create 2 empty directories at the root of this repo: "data" and "last".</li>
<li>Run <b>python data_generator.py</b> to generate dummy customers, locations, categories and products data.</li>
<li>Create a sales datawarehouse database on a postgres instance and run the <a href="https://github.com/vaibhavnikas/E-commerce-data-streaming-pipeline-consumer/blob/master/warehouse_setup/sales_dw.sql">sales_dw.sql</a> script to setup the sales_dw db.</li>
<li>Import data from customers.csv, locations.csv, categories.csv and products.csv into dim_customer, dim_location, dim_category and dim_product dimension tables respectively.</li>
<li>Start the Kafka server and create a <b>e-commerce-transactions</b> topic.</li>
<li>Run <b>python ecommerce_transaction_producer.py</b> to generate transactions data and produce it into the <b>e-commerce-transactions</b> Kafka topic.</li>
</ol>
