The rapid evolution of Large Language Models (LLMs) is fundamentally reshaping how technology companies operate, from enhancing product capabilities to streamlining internal development workflows. At EMQ, this transformation is not merely observed; it is actively led. The company's commitment to integrating artificial intelligence runs deep, extending beyond just adding "smart features" to its offerings. EMQ believes in harnessing AI to empower its developers, accelerate its innovation cycle, and ultimately deliver a superior experience for users and customers alike. This article offers a glimpse into EMQ's broader AI strategy and then delves into two specific, yet perhaps lesser-known, ways the EMQX team is leveraging LLMs to boost its daily development work.

## A Glimpse into Our Broader Initiatives

EMQ's commitment to AI is comprehensive, extending across various facets of its business to enhance product capabilities and streamline operations. This includes:

- **Community Support**: Deployed an AI bot on the EMQX Discord channel to provide real-time community assistance.
- **Product Enhancements**:
  - **EMQX Rule Engine**: Integrated the `ai_completion` call into the EMQX Rule Engine for intelligent message processing.
  - [**MQTTX Copilot**](https://www.emqx.com/en/blog/mqttx-1-9-7-release-notes): Combines LLMs with MQTT operations to enable automation and streamline development.
  - **NeuronEX IIoT Data Analysis**: Leverages LLMs and RAG for natural language data exploration and automated troubleshooting.
- **Internal Optimization**:
  - Utilizes LLMs to automate knowledge aggregation from Jira and Slack into a RAG database, improving troubleshooting efficiency.
  - Developing an API to feed error logs into LLMs for customer self-service diagnostics.

These initiatives position EMQ as an AI-first company, driving operational efficiency, product innovation, and superior user experiences.

## Boosting EMQX Development with LLMs

Beyond the broad company-wide initiatives, the EMQX core development team is specifically leveraging LLMs to streamline internal processes. These efforts, though perhaps not yet widely known, represent significant advancements in developer productivity and product quality.

### Automated i18n Translation

Internationalization (i18n) translation work for a rapidly evolving technical product like EMQX presents inherent difficulties and can be a tedious, time-consuming process. Traditionally, this consumes valuable developer time, diverting them from core coding and feature development. There is also the risk of inconsistencies or delays in translations, which can negatively impact the global user experience.

EMQX addresses this challenge by using LLMs to automate a significant portion of the translation process. This introduces a fundamental shift in roles: developers can now focus on coding and documenting in English, which serves as the source of truth, while LLMs handle the initial translation. This allows human writers to concentrate on reviewing and refining the AI-generated translations, significantly improving overall efficiency and accuracy. This direct link between AI adoption and increased developer bandwidth means engineers are empowered to concentrate on innovation and complex problem-solving. This commitment to optimizing internal processes directly translates to faster product development cycles and higher quality code, ultimately benefiting the end-user.

The `emqx-i18n` GitHub repository serves as the central hub for these translations. The translation files are structured in HOCON format, which is a superset of JSON, and the `.hocon` suffix is used for specific build processes. 

The workflow for automated translation is systematic: 

1. English documentation is first synchronized from the main EMQX repository. 
2. A three-way comparison is then performed between the current English, existing Chinese, and a base version of the documentation to identify changes. This process flags updated documents, adding a "NEED_TRANSLATION" comment along with old and new English versions, and also marks any content missing in the Chinese file for translation. 
3. The identified differences are then concatenated to the prompt file (`prompt.hocon`) which contains instructions for the LLM, then fed to an LLM for translation.
4. The LLM-generated translations are subsequently concatenated into the main Chinese documentation file, which is then formatted and committed. 
5. Finally, human translators review this newly generated content for any errors before its contents are finalized.  

This systematic approach ensures that translations are kept consistently up-to-date with product changes, minimizing manual overhead and maintaining linguistic consistency. The broader implication of automated i18n is the ability to scale translations more easily and consistently. This allows EMQX to reach a wider global audience with high-quality, localized documentation and product interfaces, effectively breaking down language barriers. AI-driven i18n is therefore not just about saving time; it is a strategic move to accelerate market penetration and user adoption in non-English speaking regions, making EMQX a truly global product.

### LLM-Powered Example Generation

EMQX, as a powerful and flexible [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), offers extensive configuration options. This flexibility, while beneficial, introduces a significant challenge: with over 30 data integrations and numerous parameters (such as TLS settings, batching configurations, and various authentication methods for data Sinks and Sources etc.), writing comprehensive and accurate configuration examples for every possible combination becomes a monumental, if not impossible, task for human documentation teams. This inherent complexity can be a substantial barrier for users attempting to set up EMQX for their specific needs, often leading to errors and an increase in support requests.

To address this, EMQX leverages LLMs, combined with its auto-generated configuration schema, to dynamically generate highly accurate and context-specific configuration examples. The LLM can make a very good educated guess of a making-sense example which almost can be copy-pasted directly into their deployment by intelligently utilizing config field types, descriptions, default values, and even user-provided context. This directly addresses a major pain point for users. By making configuration easier and more intuitive through AI, EMQ significantly lowers the barrier to entry for new users and accelerates product adoption.

Users can browse the EMQX configuration schema and click on a specific configuration path to generate an example for a particular struct. They can then interactively expand deeper into the configuration tree, building examples tailored to their exact requirements. The foundation for this intelligent generation lies in EMQX's well-defined configuration schema, which is based on HOCON (a superset of JSON). This schema provides the structured data—including field types, descriptions, and default values—that the LLM uses as its foundational knowledge. While the specific prompt used to guide the LLM in generating these examples was not directly accessible, its existence ensures that the output adheres to EMQX's configuration syntax and best practices.  

The benefits of this LLM-powered configuration example generation are manifold:

- **User Empowerment:** Users can easily build examples that precisely fit their specific requirements, reducing guesswork and trial-and-error.
- **Reduced Errors:** LLM-generated examples are inherently less prone to human error, leading to smoother and more reliable deployments.
- **Faster Time-to-Value:** Users can quickly get their EMQX deployments configured and running, accelerating their project timelines.
- **Reduced Support Burden:** Fewer configuration-related issues translate directly to less strain on customer support teams.

This approach significantly enhances the overall developer experience (DX) of EMQX, making the product more appealing and reducing the time from installation to successful deployment. Furthermore, manual documentation of all configuration combinations is simply unfeasible. LLM-driven generation scales infinitely with the complexity of the product, ensuring that EMQ can maintain comprehensive, up-to-date, and personalized documentation without a proportional increase in human effort. This represents a fundamental shift in how complex product knowledge is disseminated, transforming documentation from a static artifact into a dynamic, interactive tool that fosters better knowledge transfer from product experts to end-users.

### Automated Documentation Issue Resolution with OpenHands

Maintaining the accuracy and currency of extensive technical documentation, such as that powering the official [EMQX documentation website](https://docs.emqx.com/en/emqx/latest/), is a continuous challenge. To address this, EMQ is pioneering the use of [OpenHands](https://github.com/All-Hands-AI/OpenHands), an autonomous AI agent, to automatically resolve issues within the `emqx/emqx-docs` repository. When a documentation bug or a request for clarification is identified and deemed suitable for AI intervention, developers simply apply the `fix-with-ai` label to the corresponding GitHub issue. This action triggers an automated workflow, empowering OpenHands to understand the problem, navigate the documentation repository, make the necessary modifications, and propose a pull request with the fix. 

This innovative approach not only accelerates the resolution of documentation issues, ensuring users have access to the most reliable information, but also further liberates the EMQ team to focus on developing core product features and tackling more complex documentation challenges. This reinforces EMQ's commitment to leveraging AI for end-to-end development efficiency, extending the AI-driven enhancements from code generation and translation directly into the maintenance and improvement of its vital user-facing documentation.

## EMQ's AI-Powered Future

EMQ's comprehensive commitment to integrating artificial intelligence is transforming every facet of its operations.

The strategic decision to integrate AI deeply across the organization, rather than in isolated projects, solidifies EMQ's brand as an innovative, AI-driven company. This holistic approach ensures that AI is not just a feature but a fundamental enabler of efficiency, product quality, and an exceptional user experience. By sharing its internal AI strategies and inviting community engagement, EMQ is implicitly fostering a collaborative ecosystem. This transparency can lead to a more vibrant community, encourage external contributions, and establish a feedback loop that further accelerates EMQ's AI adoption and innovation.

EMQ is actively building a future where AI empowers both developers and users, making IoT solutions more intelligent, efficient, and accessible for everyone. We invite developers and IoT enthusiasts to explore EMQX and its growing suite of AI-powered features. Join the EMQX Discord community, explore the GitHub repositories, and share your thoughts on how AI is shaping the future of development.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
