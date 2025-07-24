## Introduction

With the official release of [NeuronEX 3.6.0](https://www.emqx.com/en/blog/neuronex-v-3-6-0-release-notes), the new "Data Insights" feature provides users with a complete, closed-loop workflow from data storage and query analysis to visual monitoring, making data value readily accessible.

As the visualization tool within the NeuronEX Data Insights module, the Dashboard is used for centrally displaying and monitoring critical data. It allows users to create highly customizable views, presenting data stored in the Datalayers time-series database in the form of intuitive charts, stats, or tables. This helps users grasp real-time production status, track core KPIs, and respond quickly to anomalies.

This article will guide you through the Dashboard feature in NeuronEX, enabling you to easily create data visualization dashboards through simple drag-and-drop and configuration.

## Enabling the Feature

Before using the Dashboard feature, you need to start the internal time-series database.

1. After logging into the UI, navigate to: **Administration** > **System Configuration** > **Data Storage Configuration**.

2. Click the **Datalayers** time-series database button to enable it.

   ![image.png](https://assets.emqx.com/images/5d39365986d334f15afa359d783cb4ad.png)

 

Navigate to: **Data Collection** > **North Apps** > **DataStorage**. Click the **Add Subscription** button and select the data you want to store in the time-series database.

![image.png](https://assets.emqx.com/images/9d70b47f30a42b7540098b729b5310c1.png)

## Main Page Management

Navigate to the **Data Insights -> Dashboards** page. You will see a main page that clearly lists all created dashboards, facilitating centralized management as shown below:

![image.png](https://assets.emqx.com/images/9359133557e62150f545655bbab1be76.png)

The main page includes the following information:

- **Name**: The custom name of the dashboard.
- **Description**: A brief description of the dashboard's purpose or content.
- **Created At**: The date and time the dashboard was created.
- **Updated At**: The date and time the dashboard was last modified.
- **Operations**: Actions that can be performed on each dashboard.
  - **Edit**: Click the icon to modify the dashboard's basic information, such as its name and description.
  - **Enter**: Click the icon to open the detailed view of the dashboard.
  - **Copy**: Click the icon to quickly duplicate an existing dashboard as a template for a new one.
  - **Delete**: Click the icon to remove a dashboard that is no longer needed.

## Internal View and Interaction

After entering a specific dashboard, you will see an interactive interface for displaying and configuring data.

This page periodically sends data requests to the backend based on the configuration in the top-right corner and then displays the data in the corresponding Panels.

![image.png](https://assets.emqx.com/images/78c8de1a581e3c90e88fc0728ab9dd9f.png)

Click **Enter Edit Mode** to access the following functions:

- **Add Panel**: Click the **Add Panel** button in the top-left corner to add a new data display unit (Panel) to the current dashboard.
- **Cancel**: If you have made changes to the dashboard's layout or Panels but do not want to save them, click the **Cancel** button to discard the changes.
- **Save Dashboard**: Any modifications to the dashboard (such as adding/deleting Panels, adjusting the layout, or changing Panel configurations) must be saved by clicking the **Save Dashboard** button to take effect.

![image.png](https://assets.emqx.com/images/2c0b4b87722ef84031dfe39638b9fdf5.png)

## Global Time and Refresh Control

Located in the top-right corner of the dashboard, these controls manage the data display range and refresh frequency for the entire dashboard.

**Time Range Selector**:

- **Global Control**: Defines the query time span for data in all Panels.
- **Preset Ranges**: Offers several common preset time ranges (e.g., "Last 1 hour" in the screenshot).
- **Custom Time Period**: Allows users to select precise start and end dates and times.

**Refresh Mechanism**:

- **Auto-Refresh Interval**: Select a preset auto-refresh interval (e.g., "30s" in the screenshot), and the dashboard will automatically update data at this frequency.
- **Manual Refresh**: Click the refresh icon to immediately fetch the latest data and update all Panels.

## Panel Management and Layout

A Panel is the basic unit on a dashboard for displaying a single chart, stat, or table.

- **Drag to Adjust**: You can resize a Panel by dragging its bottom-right corner or move it by dragging its header, allowing for flexible layout customization.
- **Grid Alignment**: The dashboard uses a grid system (shown as dotted lines in the background of the screenshot) to help Panels align automatically, creating a cleaner and more organized layout.
- **Panel Action Menu**: Each Panel typically has a three-dot menu icon in its top-right corner. Clicking it reveals options to edit, copy, or delete the Panel.

## ![image.png](https://assets.emqx.com/images/ca63ac401bdfd04fde22da33c55ea76d.png)Adding and Configuring a Panel

After clicking the **Add Panel** button in the dashboard view, an "Add Panel" dialog will appear for detailed configuration of the new Panel.

![image.png](https://assets.emqx.com/images/55b4475f8f0981b37c0695b5f645c733.png)

The dialog layout is as follows:

1. **Left Side - Query Configuration Area**:
   - **Query Tabs** (e.g., "Query 1"): Allows you to configure multiple data queries for a single Panel (except for the Table type). Each query corresponds to a series in the chart. You can add a new query by clicking **+**.
   - **SQL Input Area**: Enter the SQL query statement for the currently selected Query Tab.
   - **Alias by**: Specify a display alias for the result series of the current query. This is very useful for distinguishing multiple series in a Panel. It typically requires the SQL query result to contain a timestamp and a single value column.

1. **Right Side - Panel Options**:
   - **Panel Title**: Specify a meaningful name for the Panel (required).
   - **Chart Type**: Choose how to display the data. The current version supports:
     - **Line**: Suitable for showing trends in time-series data.
     - **Bar**: Suitable for comparing data volumes across different categories or time points.
     - **Stat**: Displays a single key value in a prominent way.
     - **Table**: Presents detailed data in a tabular format (the Table type supports only one query).
     - **Unit**: For example, °C, RPM, MPa, etc. This information will be displayed on the chart or as a suffix to the value.

1. **Bottom Options**:

   - **Use $timeFilter variable in SQL Query**:

     - **Enable/Disable toggle**: Controls whether to enable the `$timeFilter` variable in the SQL query.
     - **When enabled**: The user's SQL statement **must include** `$timeFilter` (e.g., `WHERE $timeFilter` or `AND $timeFilter`). NeuronEX will replace it with the time range condition selected by the dashboard's global time selector or the Panel's preview time selector.
     - **When disabled**: NeuronEX will automatically append the time range condition to the user's SQL statement.

   - **Dialog Top Controls**:

     This dialog may also contain an independent time range selector and an execute query/refresh button, used for previewing and testing the currently configured query before confirming the Panel addition.

   - **Dialog Action Buttons**:

     - **Cancel**: Closes the "Add Panel" dialog without saving any configuration.
     - **Execute Queries**: (Located at the bottom of the dialog, or possibly at the top) Executes the currently configured SQL queries and previews the results within the dialog, helping the user verify the correctness of the queries.
     - **Confirm**: Saves the Panel configuration and adds it to the dashboard.

![image.png](https://assets.emqx.com/images/cfc89d9fb5cb5d602dff2d0fc6103eb5.png)

## Use Case Examples

- **Production Monitoring Dashboard**: Centrally display key equipment operating parameters (temperature, pressure, speed), output, and energy consumption to understand production line status in real time.
- **KPI Tracking Dashboard**: Create a dedicated dashboard to visualize key performance indicators (KPIs) such as OEE (Overall Equipment Effectiveness), equipment failure rates, and energy consumption metrics.
- **Quality Analysis Report**: Display trend charts and statistical data for critical product quality parameters to help monitor quality fluctuations.
- **Alarm and Event Overview**: In conjunction with data analysis results, display the number, type, and trends of recent important alarms.

## Conclusion

As the core visualization tool of the NeuronEX Data Insights module, the Dashboard transforms massive amounts of data from the time-series database into intuitive, dynamic monitoring views in real time. With its diverse chart displays and flexible configuration options, you can quickly build professional dashboards tailored to your business needs, closing the loop from data presentation to decision support.

Whether it's monitoring the pulse of a production line, accurately tracking core KPIs, deeply analyzing quality fluctuations, or quickly responding to critical alarm events, the Dashboard feature provides a centralized, clear, and real-time data presentation, serving as a powerful assistant to drive decisions, optimize operations, and improve efficiency.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact" class="button is-gradient">Contact Us →</a>
</section>
