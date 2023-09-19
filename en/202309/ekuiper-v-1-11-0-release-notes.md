We are thrilled to announce that [eKuiper 1.11.0](https://ekuiper.org/downloads) is now officially released!

This version aims to improve the SQL syntax to offer more powerful rules. Moreover, we have added several features that are specially designed to enhance the management and operation of rules in edge environments. Notably, we present a more flexible and robust Sink cache retransmission policy to reduce the impact of edge network instability.

We received 187 PRs from 22 contributors, showing the spirit of community cooperation. Welcome to upgrade to eKuiper 1.11.0 to unleash more powerful data transformation and analysis capabilities!

> For complete release notes, please see: [Release eKuiper 1.11.0 · lf-edge/ekuiper](https://github.com/lf-edge/ekuiper/releases/tag/1.11.0) 

## Extending SQL Syntax

We've added more data transformation and analysis capabilities by introducing new built-in functions and SQL syntax.

### Extending Built-in Functions

We've added over 50 new functions, including datetime, array manipulation, object manipulation, math, and type conversion functions, significantly enhancing computation and transformation capabilities.

- The new version supports datetime and math functions compatible with relational databases like MySQL, simplifying SQL migration from databases to eKuiper.
- In the case of nested data, which is common in IoT applications, the new version offers a broader range of array and object manipulation functions, providing essential capabilities for common nested data transformations. For instance, the following SQL statement can execute operations like duplicate removal and sorting on an array-type field `arr`: `SELECT ARRAY_DISTINCT(arr1), ARRAY_MAP(abs, arr1), ARRAY_SHUFFLE(arr1), ARRAY_SORT(arr1) FROM funcDemo`

### Extending Syntax

We've broadened the SQL syntax, by extending wildcards and alias referencing, adding support for single-quoted strings and limit clauses, thus enhancing both expressive power and user-friendliness.

The extended wildcards now support Except and Replace clauses. In IoT scenarios, streams can contain far more fields than traditional databases, sometimes even hundreds. The native wildcard `*` is not flexible enough as it selects all fields. To exclude specific fields, you'd typically need to have a long list of fields in a SELECT statement. However, the Except syntax provides a solution. In the following example, we exclude fields `a` and `c`.

```
SELECT * EXCEPT(a, c) FROM demo
```

The new alias referencing feature significantly enhances the simplicity and usability of the SQL syntax. In the following example, the alias `ab` defined in the SELECT clause is referenced within the same clause. This usage is not valid in standard SQL, where users would typically need to employ a subquery or a CTE, resulting in a complex and less readable SQL statement. If the reference is nested, more complex nested subqueries would be required, further reducing readability. The alias referencing feature addresses this issue and, to some extent, reduces the need for repeated calculations, thereby improving performance.

```
SELECT a+b as ab, ab + c as abc FROM demo
```

### Strengthening Analytic Functions

We've added some new functions, including window function row_number, cumulative analysis functions, and rule-level metadata functions like rule_start.

Window functions operate on multiple rows of data within a window, similar to aggregate functions. The key distinction is that aggregate functions combine multiple rows into one result (e.g., `avg` calculates the average of multiple rows), whereas window functions retain multiple rows in their output and base their results on rows. In this version, we introduce window functions for the first time, starting with the row_number() function, which assigns a unique row number to each row within the window, facilitating subsequent calculations.

In this new version, eKuiper introduces rule-level cumulative analysis functions and metadata-related functions. These functions enable calculations over longer data lifecycles, including sum, max, min, and average values, along with tracking the cumulative number of times a rule has been triggered and its start time. Users can leverage these accumulated values to create more advanced filtering and alert scenarios.

## Strengthening Stream Analysis

### Innovative Sliding Window

For the first time, we've introduced a sliding window in stream processing, which gathers data around the trigger time when the trigger condition is met. This simplifies the collection of relevant data, particularly in scenarios that demand flexible data collection before and after an event. In the example below, we use a rule to collect data from one second before and one second after the temperature hits zero.

```
{
  "id": "ruleCollect",
  "name": "sliding window data：collect data from one second before and one second after the temperature hits zero",
  "sql": "SELECT * FROM mockFileStream GROUP BY SLIDINGWINDOW(ss, 1, 1) OVER (WHEN temperature < 0 AND lag(temperature, 1, 0) >=0 )",
  "actions": [
    {
      "mqtt": {
        "topic": "result/rule_2",
        "server": "tcp://127.0.0.1:1883"
      }
    }
  ],
  "options": {
    "isEventTime": true
  }
}
```

### Optimizing Event Time Processing

We have redesigned the watermark algorithm and event time management to enable event time processing in continuous queries and window functions. Using event time in continuous queries allows us to handle out-of-order data, ensuring consistent results across multiple runs on the same dataset.

Using event time only requires two steps:

- When creating a stream, configure the timestamp field in the event with the `timestamp` parameter.
- When creating a rule, set the options parameter `isEventTime=true` and configure the `lateTolerance` parameter.

### Speeding JSON Decoding

For streams with schemas, we have optimized JSON decoding to provide faster performance. If the data source has many fields and the rule uses fewer fields, defining the schema in the stream can greatly improve runtime performance.

## Edge Rule Management

Operating and managing edge-oriented middleware products can pose certain challenges. However, in the new version, we have made significant improvements to address these challenges.

### Advancing the Sink Cache Retransmission Policy

In the new release, we have introduced significant enhancements to the Sink Cache Retransmission Policy, allowing users to manage retransmission data more effectively. These improvements include:

- Configuring retransmission data and real-time data with separate channels that can be sent simultaneously.
- Defining retransmission data with separate destinations, such as different MQTT topics from real-time data, enabling downstream applications to subscribe to distinct topics for handling real-time and retransmission data separately.
- Flexible prioritization settings for retransmission and real-time data.
- The ability to label retransmission data with fields, making it easier for downstream applications to distinguish them.

### Adding Time-Range Support When Running Rules

We've added time-range support to schedule rules, allowing them to be executed within specific time periods.

### Dynamic Configuration Updates

We've introduced the feature of changing the configuration dynamically, which includes setting different levels of logging and debugging for each rule, to make the runtime debugging process easier. Users can use the API to adjust the global logging level at runtime. In the following example, you can switch the logging level to debug at runtime and open the Log file.

```
PATCH http://{{host}}/configs
Content-Type: application/json

{"debug":true,"fileLog":true}
```

In the previous versions, the logs of all rules and eKuiper itself were mixed in the same log file. This made it harder to debug a single rule. In the new version, you can enable debug for a specific rule and output it to a separate log file. As shown in the following example, you can set the logging for each rule separately by using the rule options.

```
{
  "id": "rule_debug",
  "sql": "SELECT * FROM pubdata",
  "actions": [{
    "log": {
    }
  }],
  "options": {
    "debug": true,
    "logFilename": "demo-rule.log"
  }
}
```

## Conclusion

eKuiper 1.11 has improved the expressiveness of the rules and enhanced the data transformation and analysis capabilities. The new version also keeps improving the edge operation and management features. This release has been supported by the community and is a collaborative effort. We are grateful to all the partners who contributed to this release. We invite you to upgrade to eKuiper 1.11.0 and enjoy more data transformation and analysis features!



<section class="promotion">
    <div>
        Try eKuiper for Free
    </div>
    <a href="https://ekuiper.org/downloads" class="button is-gradient px-5">Get Started →</a>
</section>
