Integrating MQTT data streams with AWS S3 Tables enables you to build a scalable and queryable time-series data lakehouse. This guide walks you through best practices for creating an end-to-end pipeline — from IoT data ingestion in EMQX to structured storage in an Iceberg-based S3 Table, ready for analytics via Athena.

## **Part 1. Prepare AWS S3 Tables Resources**

Before setting up the integration in EMQX, you must first create the necessary storage resources in AWS S3 Tables.

### **Step 1. Create a Table Bucket**

1. Log in to the AWS Management Console and open the S3 service.
2. In the left navigation pane, select Table buckets.
3. Click Create table bucket, enter a bucket name (e.g., `mybucket`), and click Create table bucket.
4. Once created, click your bucket name to open the Tables view.

![image.png](https://assets.emqx.com/images/f75d3357d62fb93d69f3a13ae8e6b185.png)

### Step 2. Create a Namespace and Table

1. Click Create table with Athena.
2. When prompted for a namespace, click Create a namespace, provide a name (e.g., `testns`), and confirm.
3. Click Create table with Athena again.

### Step 3.⚠️Complete Dual-Level Authorization (Database + Table)

AWS environment uses Lake Formation to manage the Glue Data Catalog, so you must grant both database-level and table-level permissions before creating or querying Iceberg tables in Athena.

**1.Database-Level Authorization:**

1. Open Lake Formation Console → Data Catalog → Databases.
2. Locate the namespace you just created (e.g., `testns`).
3. Click Actions - Grant permissions.
4. In the pop-up window:
   - Principals: Select your IAM user or role (⚠️ The Root account cannot be granted any permissions).
   - Database: Choose the corresponding namespace (e.g., `testns`).
   - Permissions: Check Super and Grantable Super.
5. Click Grant to save the authorization.
6. Return to the Athena Query Editor and re-run the CREATE TABLE statement — it should now execute successfully.

**2. Table-Level Authorization:**

After the table is created, grant the same Super permissions at the table level:

1. In Lake Formation → Data Catalog → Tables, locate the newly created table (e.g., `testtable`).
2. Click Actions → Grant permissions.
3. Add the same IAM user or role.
4. Check Super and Grantable Super.
5. Click Grant to complete the authorization.

Once both database-level and table-level permissions are granted, your IAM user can fully create, query, and manage Iceberg tables in Athena.

### Step 4. Verify IAM User Policies

Before using Athena and Lake Formation together, make sure your IAM user (for example, `emqx-s3tables-user`) has all required policies attached.

These permissions allow the user to manage S3 Tables, create Iceberg tables, and grant Lake Formation access without restriction.

**Required IAM Policies:**

| Service        | Policy Name                                                  | Description                                                |
| :------------- | :----------------------------------------------------------- | :--------------------------------------------------------- |
| IAM            | `AdministratorAccess` *(optional but recommended for testing)* | Full administrative privileges for setup and debugging     |
| Amazon Athena  | `AmazonAthenaFullAccess`                                     | Allows query and table creation in Athena                  |
| Amazon S3      | `AmazonS3FullAccess`                                         | Enables read/write access to S3 buckets and objects        |
| S3 Tables      | `AmazonS3TablesLakeFormationServiceRole`                     | Required for S3 Tables integration with Lake Formation     |
| Glue           | `AWSGlueConsoleFullAccess`                                   | Enables database and table operations in Glue Data Catalog |
| Lake Formation | `AWSLakeFormationDataAdmin`                                  | Grants management access for database/table permissions    |
| Cross-account  | `AWSLakeFormationCrossAccountManager`                        | For managing cross-account permissions if needed           |

In the AWS IAM console, the **Permissions** tab of `emqx-s3tables-user` should list policies similar to:

```
AdministratorAccess
AmazonAthenaFullAccess
AmazonS3FullAccess
AmazonS3TablesLakeFormationServiceRole
AWSGlueConsoleFullAccess
AWSLakeFormationDataAdmin
LakeFormationAdminCustom
```

![image.png](https://assets.emqx.com/images/0c87d5c72e61d8fb8d19ace4df5f04df.png)

Ensuring your IAM user has these policies, combined with Lake Formation database and table-level “Super” permissions, will prevent all common access errors when integrating EMQX with AWS S3 Tables and Athena.

### Step 5. Verify the Table in Athena

1. Open the Query table with Athena, then select your Catalog (e.g., `s3tablescatalog/mybucket`) and your newly created namespace.

2. Run the following DDL to create an Iceberg table:

   ```sql
   CREATE TABLE `testns`.testtable (
     clientid string,
     topic string,
     payload string,
     publish_received_at timestamp
   )
   TBLPROPERTIES ('table_type' = 'iceberg');
   ```

   ![image.png](https://assets.emqx.com/images/b9b4db2e9d5093cf1ccfa4839bf18099.png)

1. Verify the table creation:

   ```sql
   SELECT * FROM testtable;
   ```

If the query returns no rows, your table is successfully initialized and ready to receive MQTT data.

![image.png](https://assets.emqx.com/images/f4c172da97bc98294fdf0015f7591475.png)

## **Part 2. Configure S3 Tables Integration in EMQX**

Now that your destination is ready, you can configure EMQX to stream MQTT data into S3 Tables.

### **Step 1. Create a Connector**

![image.png](https://assets.emqx.com/images/5d439b88c0c2989044212edc77e6c0e2.png)

![image.png](https://assets.emqx.com/images/6c3ea152a962d20dcfb353a7af755488.png)

### **Step 2. Create Rule and Action**

1. Go to Integration → Rules, click Create.

2. Enter rule ID: `my_rule`.

3. In the SQL editor, add:

   ```
   SELECT
     clientid,
     topic,
     payload,
     publish_received_at * 1000 AS publish_received_at
   FROM
     "t/s3t"
   ```

   > Tip: Ensure the output fields exactly match your Iceberg table schema. A mismatch may prevent data from being written.

1. Under Actions, select S3 Tables from the Action Type dropdown and click Create new action.

2. Configure the action:

   - Name: e.g., `to_s3tables_action`
   - Connector: Select the `my-s3-tables` connector created earlier
   - Namespace**:** e.g., `testns`
   - Table: e.g., `testtable`
   - Max Records: e.g., `500`
   - Time Interval: e.g., `5000` (milliseconds)
   - Data File Format: choose between `avro` (default) or `parquet`

3. Click Create to save the action, then Create again to finalize the rule.

   ![image.png](https://assets.emqx.com/images/fcdf2f95ea23f03823d7dddc2741978e.png)

## Part 3. Test the Pipeline

Now use the MQTTX Client to publish a test message and trigger the pipeline.

1. Open the MQTTX application and connect to your EMQX broker.

   - Client ID: `emqx_c`
   - Topic: `t/s3t`
   - QoS: `0`

2. In the message field, enter:

   ```
   "Bonjour S3 Tables"
   ```

3. Click Publish to send the message.

![image.png](https://assets.emqx.com/images/4519fa9ea23c0e0a9e0bf34a886f0d0d.png)

This message will be processed by EMQX according to the defined rule and written to your S3 Tables destination.

## **Part 4. Verify Data in Athena**

Go back to Athena Query Editor and run:

```sql
SELECT * FROM testtable;
```

You should now see your MQTT message (“Hello S3 Tables”) appear as a record in your Iceberg table.

![image.png](https://assets.emqx.com/images/e8b824014f2577a462e2992b47ec3b15.png)

## **Conclusion**

You have now built a complete time-series data pipeline — streaming MQTT messages from EMQX into AWS S3 Tables as structured Iceberg datasets.

This setup bridges IoT and big data analytics, enabling powerful querying and time-series analysis directly in your data lakehouse.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
