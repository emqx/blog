Europe’s regulators are reshaping how companies handle data from connected devices. The upcoming EU Data Act, for example, will require all new connected devices to give users direct control over their data. This is a major shift, moving us away from closed, proprietary systems to open, user-centric data ecosystems where individuals, not companies, decide who can access their information.

To help companies adapt, [EMQX and Ecosteer have partnered](https://www.emqx.com/en/news/emq-partners-with-ecosteer-to-advance-iot-data-compliance-across-europe) to turn these compliance requirements into a competitive advantage. By combining MQTT messaging technology with decentralized consent management, we deliver secure, scalable, and cost-effective data sharing under user control.

## **The Changing Landscape of Data Control**

European governments are raising the bar for device data management. The EU Data Act is set to give control back to users. Soon, people will decide who gets access to their device data.

The EU data economy could be worth over €829 billion by 2025. To make this growth fair, the EU has rules like GDPR, the Data Governance Act, and the Data Act. These rules break down old silos and give people a real say in their information.

The Data Act will take effect Sept. 12, 2025. Moreover, starting in September 2026, every new device or application sold in the EU must follow its principles by design. If you use a connected device, you should be able to access, use, and share your data without extra costs or unnecessary steps.

These changes will affect everything from smart home devices and industrial IoT to car manufacturers and transit providers.

This shift also introduces new technical challenges. Many old methods for handling data requests aren’t secure. Scaling up for millions of users can get expensive fast. Centralized consent systems often struggle with complexity and regulatory demands.

## **A Simpler Way to Control Data**

EMQX and Ecosteer work together to help organizations meet these new rules and make things easier for end users.

- **EMQX** connects millions of devices and moves data in real time.
- **Ecosteer’s Data Visibility Control Overlay (DVCO)** lets users decide who can see their data. Strong encryption and key management mean users keep control, and there’s no middleman.

## **What’s Different Now**

- Devices must be built so users can get and share their own data easily.
- No extra costs or unnecessary steps.
- Companies can’t lock up your data or hide it from you.
- You decide who can share your data. It’s not up to a central authority.

## **How the EMQX + Ecosteer Solution Works**

![image.png](https://assets.emqx.com/images/b61aa74878840abdf35e2add0e905108.png)

<center>
How EMQX and Ecosteer combine to deliver secure, user-controlled data sharing and consent management.
</center>

<br>

1. **Locking Data at the Source**
   Ecosteer’s DVCO installs where your data starts—smart car, industrial sensor, or mobile app. The information is locked with encryption before it leaves the device.
2. **Reliable Data Delivery**
   EMQX delivers that locked data to subscribers using MQTT. Your existing infrastructure can stay the same.
3. **You Hold the Keys**
   Users get simple controls to grant or take away access to their data. Sharing sends out a digital key. Taking away access locks things down again. No one can see your data unless you let them.
4. **Direct User Control**
   There’s no need for a central broker or middleman to decide who sees what. The power stays with the person or company generating the data.

This approach scales well, cuts costs, and meets the EU’s latest data regulations.

**If you’re curious about the technology behind the scenes, here’s how it works at a more technical level:**
Ecosteer’s DVCO uses a patented multicast encryption method that integrates directly with MQTT publish/subscribe systems like EMQX. In most setups, anyone with access to the MQTT broker could view device data. DVCO changes this. Only recipients with permission from the data owner can decrypt and see the data, even if they have broker access. This design separates broker access from data visibility. It keeps the system secure and scalable and fits well with EU Data Act requirements.

## **Real-World Examples**

**Connected Vehicles**
A car manufacturer can let you share driving data with your insurer for usage-based insurance. With Ecosteer, you choose who gets access. You can take back access whenever you want. The control stays with you, not the carmaker or insurer.

**Mobility Data**
In Genova, Italy, Ecosteer works with AMT, the city’s public transport authority, to give riders more say over their travel data. Riders can decide if their information is shared and even get rewarded for it.

**Healthcare**
In a healthcare project, Ecosteer’s DVCO supports secure health data sharing. Air quality sensors and smartwatches can keep your health data private until you choose to share it. Only your chosen healthcare providers—like doctors or researchers—can access it, and you can change your mind at any time.

**Industry Collaboration**
The Start 4.0 Competence Center in Genova has selected Ecosteer to allow industrial partners to exchange operational data without giving up control. Companies collaborate more securely and stay compliant with EU rules.

## **Why This Matters**

These changes are about trust and transparency. Data should work for users, not just big companies. With EMQX and Ecosteer, organizations keep up with EU data rules and get more value from IoT data. People and businesses know their information is safe and that their choices matter.

## **Want to Learn More?**

If you’d like to discuss these changes or want to know how EMQ and Ecosteer can help your team, just [reach out](https://www.emqx.com/en/contact). We’re always happy to connect.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
