Today marks a significant milestone in our journey to build the world's most comprehensive MQTT data platform. We are thrilled to announce that **EMQX Tables is officially live in Preview**, available completely for free through November 30, 2025.

At EMQ, we've spent years working alongside our community, listening to your feedback, understanding your challenges, and watching you build remarkable IoT applications. One message has resonated consistently across thousands of conversations: while connecting devices is crucial, managing the data that flows from them shouldn't be a separate engineering nightmare. That's why we built EMQX Tables.

## **Your IoT Data Deserves Better**

Every IoT developer knows the drill. You've successfully connected thousands of devices to EMQX Cloud, data is streaming perfectly, and then reality hits. Where does all this data go? How do you query it? Which database should you choose? Suddenly, you're juggling multiple vendors, wrestling with integration code, and your elegant IoT solution has become an accidental mess of disconnected services.

We've all been there. Managing separate systems for MQTT messaging and data storage means:

- Constant context switching between different management consoles
- Complex integration pipelines that break at the worst possible moments
- Multiple vendor relationships, each with its own billing and support
- Security boundaries that need careful coordination
- Valuable engineering time spent on plumbing instead of innovation

EMQX Tables changes all of this.

## One Platform, Zero Complexity

EMQX Tables is a fully managed, time-series database service built directly into EMQX Cloud. It's not just another database; it's a purpose-built storage solution that understands IoT data patterns and integrates seamlessly with your EMQX broker.

Here's what makes it special:

- **Native MQTT Integration**: Your data flows directly from MQTT topics to storage with just a few clicks. No external APIs, no custom code, no complex ETL pipelines. Just configure your Rule Engine or data sinks, and you're done.
- **Built for IoT Scale**: IoT data is unique: high-frequency writes, predictable patterns, time-series by nature. EMQX Tables is optimized for exactly these patterns, handling millions of data points efficiently while maintaining query performance.
- **Schema-on-the-Fly**: Stop wrestling with rigid database schemas. EMQX Tables automatically infers structure from your JSON payloads, adapting as your data evolves. Your devices can start sending new fields tomorrow, and we'll handle it seamlessly.
- **Powerful Query Options**: Whether you prefer SQL for complex analytics or need PromQL compatibility for existing dashboards, we've got you covered. Plus, full support for the InfluxDB Line Protocol means your existing tools just work.
- **Instant Visualization**: Connect Grafana, Metabase, or your favorite BI tool directly to EMQX Tables. Build real-time dashboards and monitoring systems without any middleware or data transformation.
- **Unified Management**: Everything lives in one console. Manage your MQTT broker and time-series database together, with a single security model, unified billing, and consistent user experience.

## Built for IoT: Our Strategic Partnership with Greptime

We're particularly excited to share that EMQX Tables is built upon GreptimeDB, through a strategic partnership that combines EMQX's IoT expertise with Greptime's cutting-edge time-series database technology.

GreptimeDB isn't just any time-series database, it's cloud-native, purpose-built for the scale and patterns of IoT workloads. This partnership allows us to deliver a storage solution that's specifically optimized for IoT scenarios while maintaining the performance and reliability you expect from EMQX.

## Join Our Public Preview Program - Free for a Limited Time!

Today, we are inviting you to be the first to experience the power and simplicity of EMQX Tables.

The Public Preview will run from **November 1st 2025, to November 30th, 2025**. During this period, **use of EMQX Tables is completely free of charge**.

This is your opportunity to explore its capabilities, simplify your data stack, and provide invaluable feedback that will help us shape the future of our platform. We are building this for you, and we want to hear from you. Getting started is easy: simply log into your EMQX Cloud console and create your first Table.

On December 1, 2025, EMQX Tables will transition to general availability with usage-based pricing. But for now, it's all yours to explore.

## What’s Next?

This announcement is just the beginning. This blog is the first in a series dedicated to EMQX Tables. In the coming weeks, we will publish more posts that take a deeper dive into specific features, provide step-by-step tutorials on integrating with tools like Grafana, and showcase real-world use cases like IIoT analytics and connected vehicle monitoring.

We are incredibly excited to embark on this new chapter with you. Our goal is to provide you with the most powerful and intuitive MQTT data platform for building the next generation of IoT applications.

Thank you for being on this journey with us. We can’t wait to see what you build.



<section class="promotion">
    <div>
        Try EMQX Tables for Free
    </div>
    <a href="https://cloud-intl.emqx.com/console/tables/new" class="button is-gradient">Get Started →</a>
</section>
